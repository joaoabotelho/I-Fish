import numpy as np
import math
import turtle
import wave
import time
import pygame
import threading
from threading import Thread

from audio_analytics import AudioInformation

def main():

    FILE_NAME = "audio-siri/longer_test.wav"
    test = AudioInformation(FILE_NAME)
    print test
    test.plot_audio()

    norm = test.normalized

    """
    intervals = []
    n_intervals = 100
    for i in range(len(norm)):
        norm[i] = round(norm[i],5)
        intervals.append(int((norm[i] * n_intervals) % (n_intervals+1)))
    """

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

    durations = test.array_of_time

    # Start music
    t_start_animation = time.time() # in seconds ---------x.x
    pygame.mixer.music.load(FILE_NAME)
    pygame.mixer.music.play(0)

    i = 0
    while running:
        event = pygame.event.poll()

        DISPLAY.fill([0,0,0]) # CLEAN

        # NOT END OF ARRAY
        if i != norm.size:
            pygame.draw.line(DISPLAY, linecolor, (width/4,  const * norm[i] +
                (height/2)), ((3*width)/4, const * norm[i] + (height/2)))
            pygame.draw.line(DISPLAY, linecolor2, (width/4, -const * norm[i] +
                (height/2)), ((3*width)/4, -const * norm[i] + (height/2)))

            t_end_animation = time.time()
            animation_time = t_end_animation - t_start_animation

            while(animation_time < durations[i]):
                t_end_animation = time.time()
                animation_time = t_end_animation - t_start_animation
            print "____________________________"
            i+=1
            t_start_animation = time.time() # in seconds ---------x.x

        # END OF ARRAY
        if i >= norm.size:
            pygame.mixer.music.stop()
            i = norm.size-1
            pygame.draw.line(DISPLAY, linecolor, (width/4,  const * norm[i] +
                (height/2)), ((3*width)/4, const * norm[i] + (height/2)))
            pygame.draw.line(DISPLAY, linecolor2, (width/4, -const * norm[i] +
                (height/2)), ((3*width)/4, -const * norm[i] + (height/2)))

            print "END"


        if event.type == pygame.QUIT:
            running = False


        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()