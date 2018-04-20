import numpy as np
import math
import turtle
import time
import simpleaudio as sa
import pygame

from tests.audio_analytics import AudioInformation

def main():

    FILE_NAME = "tests/audio-siri/audio_es.wav"
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

    for i in range(len(ex)):
        print(round(a[i],2), " ", ex[i])


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
    i = 0

    start = time.time()


    while running:

        event = pygame.event.poll()

        DISPLAY.fill(bgcolor)
        if i != len(ex):
            pygame.draw.line(DISPLAY, linecolor, (width/4,  ct * ex[i] + (height/2)), ((3*width)/4, ct * ex[i] + (height/2)))
            pygame.draw.line(DISPLAY, linecolor2, (width/4, -ct * ex[i] + (height/2)), ((3*width)/4, -ct * ex[i] + (height/2)))
            i+=1

        if i >= len(ex):
            print(time.time() - start)
            i = len(ex)-1
            pygame.draw.line(DISPLAY, linecolor, (width/4,  ct * ex[i] + (height/2)), ((3*width)/4, ct * ex[i] + (height/2)))
            pygame.draw.line(DISPLAY, linecolor2, (width/4, -ct * ex[i] + (height/2)), ((3*width)/4, -ct * ex[i] + (height/2)))

        pygame.display.flip()

        if event.type == pygame.QUIT:
            running = False
            

    pygame.quit() 



if __name__ == "__main__":
    main()
