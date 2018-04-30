import os
from google_api_request import googleApiRequest
from audio_analytics import AudioInformation

CLIENT_ACCESS_TOKEN = 'f0edfee5f0964102aac241ce5f13200b'

def write_to_file(path, array):
    f = open(path, 'w')
    for item in array:
        f.write(str(item)+'\n')
    f.close()

def read_from_file(path):
    f = open(path, 'r')
    a = np.array([])
    for line in f:
        a = np.append(a, float(line))
    f.close()
    return a

def gen():
    googleApi = googleApiRequest(CLIENT_ACCESS_TOKEN)
    while True:
        inp = input("Input: ")
        response = googleApi.expectResponse(inp)
        if not find_folder(response + '.wav', './responses'):
            os.system(' gtts-cli.py "' + response + '" -l \'en\' | ffmpeg -i - -ar 22050 -ac 2 -ab 192k -f wav "./responses/' + response + '.wav"')
            test = AudioInformation('./responses/' + response + '.wav')
            norm = test.normalized
            write_to_file('./responses/' + response + '-test.txt', test.array_of_time)
            write_to_file('./responses/' + response + '-norm.txt', norm)

def find_folder(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return False

gen()
