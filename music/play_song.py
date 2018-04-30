import RPi.GPIO as GPIO
import pygame
import time
import numpy as np

def read_from_file(path):
    f = open(path, 'r')
    a = np.array([])
    for line in f:
        numb = float(line)
        if(numb <= 0.2):
            numb = 0
        elif(numb > 0.2 and numb <= 0.4):
            numb = 0.3
        elif(numb > 0.4 and numb <= 0.6):
            numb = 0.5
        elif(numb > 0.6 and numb <= 0.8):
            numb = 0.7
        elif(numb > 0.8 and numb < 1):
            numb = 0.9
        a = np.append(a, numb)
    f.close()
    return a


NORM_MUSIC_FILE = "./voice-beatit-normalized.txt"
DURAT_MUSIC_FILE = "./voice-beatit-array_of_time.txt"
MUSIC_PLAY = "./music-beatit.mp3"

pygame.init()

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

norm = read_from_file(NORM_MUSIC_FILE)
durations = read_from_file(DURAT_MUSIC_FILE)

D2A = GPIO.PWM(25,100)
D2A.start(0)

pygame.mixer.music.load(MUSIC_PLAY)

t_start_animation = time.time()
pygame.mixer.music.play(0)

for x,y in zip(norm, durations):
    D2A.ChangeDutyCycle(x*100)
    print (x)
    t_end_animation = time.time()
    animation_time = t_end_animation - t_start_animation

    while(animation_time < y):
        t_end_animation = time.time()
        animation_time = t_end_animation - t_start_animation

    t_start_animation = time.time()


