import numpy as np
import time
import pygame
import google_speech_api
import google_api_request
from threading import Thread
from audio_analytics import AudioInformation

CLIENT_ACCESS_TOKEN = 'f0edfee5f0964102aac241ce5f13200b'

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (0, 255, 0)

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class Simulator:
    def __init__(self, w, h):
        self.audio_analysed = []
        self.norm = []
        self.dimensions = (w, h)
        self.speechRec = google_speech_api.speechRecognition(CLIENT_ACCESS_TOKEN)

    def animation_loop(self):
        self.setup()

        while self.running:
            event = pygame.event.poll()
            self.display.fill(BLACK)

            if self.asked:
                self.awnser_question(self.i)
                self.i += 1
                if self.i == len(self.norm):
                    self.asked = False
            else:
                self.ask_question()
                self.i = 0

            if event.type == pygame.QUIT:
                self.running = False

            pygame.display.flip()

    def setup(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.dimensions, 0, 32)
        self.running = True
        self.asked = False
        self.display.fill(BLACK)
        self.const = 200
        self.i = 0
        self.ask_question()

    def awnser_question(self, i):
        print(i)
        width = self.dimensions[0]
        height = self.dimensions[1]
        pygame.draw.line(self.display, RED, (width/4,  self.const * self.norm[i] +
            (height/2)), ((3*width)/4, self.const * self.norm[i] + (height/2)))
        pygame.draw.line(self.display, YELLOW, (width/4, -self.const * self.norm[i] +
            (height/2)), ((3*width)/4, -self.const * self.norm[i] + (height/2)))

        t_end_animation = time.time()
        animation_time = t_end_animation - self.t_start_animation

        while(animation_time < self.durations[i]):
            t_end_animation = time.time()
            animation_time = t_end_animation - self.t_start_animation
        self.t_start_animation = time.time() # in seconds ---------x.x

    def ask_question(self):
        print('Recording...')
        audio = self.speechRec.record()
        resp = self.speechRec.analyze(audio)
        print(resp)
        if resp[0]:
            if not resp[2]:
                test = AudioInformation('./responses/' + resp[1] + '.wav')
                self.norm = test.normalized
                self.durations = test.array_of_time
                self.write_to_file('./responses/' + resp[1] + '-test.txt', test.array_of_time)
                self.write_to_file('./responses/' + resp[1] + '-norm.txt',
                                   self.norm)
            else:
                self.durations = self.read_from_file('./responses/' + resp[1] + '-test.txt')
                self.norm = self.read_from_file('./responses/' + resp[1] + '-norm.txt')
            t_start_animation = time.time() # in seconds ---------x.x
            pygame.mixer.music.load('./responses/' + resp[1] + '.wav')
            pygame.mixer.music.play(0)
        self.t_start_animation = time.time()
        self.asked = True

    def write_to_file(self, path, array):
        f = open(path, 'w')
        for item in array:
            f.write(str(item)+'\n')
        f.close()

    def read_from_file(self, path):
        f = open(path, 'r')
        a = np.array([])
        for line in f:
            a = np.append(a, float(line))
        f.close()
        return a

# def main():
    # FILE_NAME = "audio-siri/longer_test.wav"
    # test = AudioInformation(FILE_NAME)
    # print test
    # test.plot_audio()

    # norm = test.normalized

    # width = 800
    # height = 600
    # pygame.init()

    # linecolor =
    # linecolor2 =

    # DISPLAY=pygame.display.set_mode((width,height),0,32)

    # DISPLAY.fill(WHITE)
    # bgcolor = 0, 0, 0
    # DISPLAY.fill(bgcolor)

    # durations = test.array_of_time

    # # Start music
    # t_start_animation = time.time() # in seconds ---------x.x
    # pygame.mixer.music.load(FILE_NAME)
    # pygame.mixer.music.play(0)

    # i = 0
    # while running:
        # event = pygame.event.poll()

        # DISPLAY.fill([0,0,0]) # CLEAN

        # # NOT END OF ARRAY
        # if i != norm.size:
            # pygame.draw.line(DISPLAY, linecolor, (width/4,  const * norm[i] +
                # (height/2)), ((3*width)/4, const * norm[i] + (height/2)))
            # pygame.draw.line(DISPLAY, linecolor2, (width/4, -const * norm[i] +
                # (height/2)), ((3*width)/4, -const * norm[i] + (height/2)))

            # t_end_animation = time.time()
            # animation_time = t_end_animation - t_start_animation

            # while(animation_time < durations[i]):
                # t_end_animation = time.time()
                # animation_time = t_end_animation - t_start_animation
            # print "____________________________"
            # i+=1
            # t_start_animation = time.time() # in seconds ---------x.x

        # # END OF ARRAY
        # if i >= norm.size:
            # pygame.mixer.music.stop()
            # i = norm.size-1
            # pygame.draw.line(DISPLAY, linecolor, (width/4,  const * 0 +
                # (height/2)), ((3*width)/4, const * 0 + (height/2)))
            # pygame.draw.line(DISPLAY, linecolor2, (width/4, -const * 0 +
                # (height/2)), ((3*width)/4, 0 * norm[i] + (height/2)))

            # print("END")

        # if event.type == pygame.QUIT:
            # running = False

        # pygame.display.flip()

    # pygame.quit()


if __name__ == '__main__':
    s = Simulator(800, 600)
    s.animation_loop()
