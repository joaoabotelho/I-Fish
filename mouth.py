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
import RPi.GPIO as GPIO

FILE_NAME = './response.wav'
CLIENT_ACCESS_TOKEN = 'f0edfee5f0964102aac241ce5f13200b'
speechRec = google1.speechRecognition(CLIENT_ACCESS_TOKEN)

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

def main():
    D2A = GPIO.PWM(25,100)
    D2A.start(0)

    norm = []
    const = 200
    running = 1
    i = 0
    while running:
        # NOT END OF ARRAY
        if i != len(norm):
            D2A.ChangeDutyCycle(norm[i] * 100)

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
            D2A.ChangeDutyCycle(0)
            audio = speechRec.record()
            if speechRec.analyze(audio):
                test = AudioInformation(FILE_NAME)
                norm = test.normalized
                durations = test.array_of_time
                t_start_animation = time.time() # in seconds ---------x.x
                pygame.mixer.music.load(FILE_NAME)
                pygame.mixer.music.play(0)
            i = 0

if __name__ == "__main__":
    main()