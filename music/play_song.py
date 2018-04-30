import RPi.GPIO as GPIO
import pygame
import time
import numpy as np

def read_from_file(path, norm=False):
    f = open(path, 'r')
    a = np.array([])
    flag = 1
    for line in f:
        numb = float(line)
        if norm == True:
            if(numb <= 0.3):
                numb = 0
            else:
                numb = round(numb,1)
        elif norm == False and flag == 1:
            flag = 0
            numb += 0.2
        a = np.append(a, numb)
    f.close()
    return a


NORM_MUSIC_FILE = "./nevergonnagiveyouup-normalized.txt"
DURAT_MUSIC_FILE = "./nevergonnagiveyouup-array_of_time.txt"
MUSIC_PLAY = "./music-nevergonnagiveyouup.mp3"

pygame.init()

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

norm = read_from_file(NORM_MUSIC_FILE, norm=True)
durations = read_from_file(DURAT_MUSIC_FILE)

D2A = GPIO.PWM(25,100)
D2A.start(0)

pygame.mixer.music.load(MUSIC_PLAY)

t_start_animation = time.time()
pygame.mixer.music.play(0)

for x,y in zip(norm, durations):
    D2A.ChangeDutyCycle(x*100)
    t_end_animation = time.time()
    animation_time = t_end_animation - t_start_animation

    while(animation_time < y):
        t_end_animation = time.time()
        animation_time = t_end_animation - t_start_animation

    t_start_animation = time.time()


