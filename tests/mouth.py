import numpy as np
import math
import turtle
import wave
import time
import simpleaudio as sa
import pygame
import threading
from threading import Thread

from audio_analytics import AudioInformation

def main():

    FILE_NAME = "audio-siri/temperature_test.wav"
    test = AudioInformation(FILE_NAME)
    #print (test)
    #test.plot_audio()
    #print (test.normalized)

    ex = abs(test.normalized)

    #ex = np.arange(0, 1.05, 0.05)

    a = []
    b = 100



    for i in range(len(ex)):
        ex[i] = round(ex[i],5)
        a.append(int((ex[i] * b) % (b+1)))
    '''
    for i in range(len(ex)):
        print(round(a[i],2), " ", ex[i])
    '''


    width = 800
    height = 600
    pygame.init()
    y = 0
    linecolor = 255, 0, 0
    linecolor2 = 0, 255, 0

    DISPLAY=pygame.display.set_mode((width,height),0,32)

    WHITE=(255,255,255)
    blue=(0,0,255)

    DISPLAY.fill(WHITE)
    bgcolor = 0, 0, 0
    dir = 1

    ct = 200
    running = 1

    start = time.time()

    aud = wave.open(FILE_NAME, 'r')

    aud_time = test.array_of_time
    print(type(test.array_of_time))
    # aud_time = [1000 * x for x in aud_time]

    print(aud_time[0])


    pygame.mixer.music.load(FILE_NAME)
    pygame.mixer.music.play(0)
    i = 0
    DISPLAY.fill(bgcolor)
    clock = pygame.time.Clock
    # clock.tick_busy_loop(30)
    cnst = 0.2
    while running:

                
        t_start_animation = time.time()
        event = pygame.event.poll()
        DISPLAY.fill([0,0,0])

        if i != len(ex):
            pygame.draw.line(DISPLAY, linecolor, (width/4,  ct * ex[i] + (height/2)), ((3*width)/4, ct * ex[i] + (height/2)))
            pygame.draw.line(DISPLAY, linecolor2, (width/4, -ct * ex[i] + (height/2)), ((3*width)/4, -ct * ex[i] + (height/2)))
            t_end_animation = time.time()
            if (t_end_animation - t_start_animation) < (cnst * aud_time[i]):
                time.sleep(cnst*aud_time[i] - (t_end_animation - t_start_animation))
                #pygame.time.wait()
                i+=1
                 

        hh = time.clock()

        if i >= len(ex):
            print("fffff")
            pygame.mixer.music.stop()
            i = len(ex)-1
            pygame.draw.line(DISPLAY, linecolor, (width/4,  ct * ex[i] + (height/2)), ((3*width)/4, ct * ex[i] + (height/2)))
            pygame.draw.line(DISPLAY, linecolor2, (width/4, -ct * ex[i] + (height/2)), ((3*width)/4, -ct * ex[i] + (height/2)))


        if event.type == pygame.QUIT:
            running = False


        pygame.display.flip()

        hf = time.clock()
        print (hf-hh)            

    pygame.quit() 



if __name__ == "__main__":
    main()
