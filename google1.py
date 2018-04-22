import speech_recognition as sr
import subprocess
import os.path
import json
import sys
from random import randint
from gtts import gTTS
import os
from tempfile import TemporaryFile

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = 'f0edfee5f0964102aac241ce5f13200b'
MAX_INT = 1000000000

class speechRecognition:

    def __init__(self, client_access_token, sample_rate=48000, chunk_size=2048, device_id=0):
        self.mic_name = 'bcm2835 ALSA: - (hw:0,0)'
        self.client_access_token = client_access_token
        self.device_id = 0
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        print('Pause threshold: ', self.recognizer.pause_threshold)
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size

    def record(self):
        with sr.Microphone(sample_rate = self.sample_rate,
                                chunk_size = self.chunk_size) as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Recording...")
            audio = self.recognizer.listen(source)
        return audio

    def analyze(self, audio):
        googleApi = googleApiRequest(self.client_access_token)
        try:
            text = self.recognizer.recognize_google(audio)
            if text == 'exit':
                print('Exiting...')
                quit()
            print("Recognized: " + text)

            response = googleApi.expectResponse(text)

            print(response)
            if not self.find(response+'.wav', './responses'):
                os.system(' gtts-cli.py "' + response + '" -l \'en\' | ffmpeg -i - -ar 22050 -ac 2 -ab 192k -f wav "' + response + '.wav"')
                return True, response, False
            return True, response, True

        except sr.UnknownValueError:
            print('Google Speech Recognition could not understand audio')
            return (False,)

        except sr.RequestError as e:
            print('Could not request results from Google Speech Recognition service; {0}'.format(e))
            return (False,)

    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
        return False

class googleApiRequest:

    def __init__(self, client_access_token):
        self.client_access_token = client_access_token
        self.ai = apiai.ApiAI(self.client_access_token)
        self.session_id = randint(1, MAX_INT)

    def expectResponse(self, query):
        request = self.ai.text_request()
        request.query = query
        request.session_id = self.session_id
        response = request.getresponse()
        parsed = json.loads(response.read().decode())
        print(json.dumps(parsed, indent=4))
        text_response = parsed['result']['fulfillment']['speech']
        score = parsed['result']['score']
        if score == 0.0:
            text_response = 'I didn\'t understand'
        print('Response: ', text_response)
        return text_response

if __name__ == '__main__':
    speechRec = speechRecognition(CLIENT_ACCESS_TOKEN)
    while True:
        audio = speechRec.record()
        speechRec.analyze(audio)
