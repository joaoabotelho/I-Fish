import numpy as np
import math
import turtle
import wave
import time
import pygame
import threading
import sys
import google1
from threading import Thread
from audio_analytics import AudioInformation

FILE_NAME = './response.wav'
CLIENT_ACCESS_TOKEN = 'f0edfee5f0964102aac241ce5f13200b'
speechRec = google1.speechRecognition(CLIENT_ACCESS_TOKEN)

def main():

    norm = []
    width = 800
    height = 600
    pygame.init()

    linecolor = 255, 0, 0
    linecolor2 = 0, 255, 0

    DISPLAY=pygame.display.set_mode((width,height),0,32)

    WHITE=(255,255,255)
    blue=(0,0,255)

    DISPLAY.fill(WHITE)
    bgcolor = 0, 0, 0
    DISPLAY.fill(bgcolor)

    const = 200
    running = 1

    # durations = test.array_of_time

    i = 0
    while running:
        event = pygame.event.poll()

        DISPLAY.fill([0,0,0]) # CLEAN

        # NOT END OF ARRAY
        if i != len(norm):
            pygame.draw.line(DISPLAY, linecolor, (width/4,  const * norm[i] +
                (height/2)), ((3*width)/4, const * norm[i] + (height/2)))
            pygame.draw.line(DISPLAY, linecolor2, (width/4, -const * norm[i] +
                (height/2)), ((3*width)/4, -const * norm[i] + (height/2)))

            t_end_animation = time.time()
            animation_time = t_end_animation - t_start_animation

            while(animation_time < durations[i]):
                t_end_animation = time.time()
                animation_time = t_end_animation - t_start_animation
            i+=1
            t_start_animation = time.time() # in seconds ---------x.x

        # END OF ARRAY
        if i >= len(norm):
            norm = []
            pygame.mixer.music.stop()

            i = len(norm)-1
            pygame.draw.line(DISPLAY, linecolor, (
                width/4,
                const * 0 +(height/2)),((3*width)/4, const * 0 + (height/2)))
            pygame.draw.line(DISPLAY, linecolor2, (width/4, -const * 0 +
                (height/2)), ((3*width)/4, -const * 0 + (height/2)))
            audio = speechRec.record()
            if speechRec.analyze(audio):
                test = AudioInformation(FILE_NAME)
                norm = test.normalized
                durations = test.array_of_time
                t_start_animation = time.time() # in seconds ---------x.x
                pygame.mixer.music.load(FILE_NAME)
                pygame.mixer.music.play(0)
            i = 0

        if event.type == pygame.QUIT:
            running = False

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
