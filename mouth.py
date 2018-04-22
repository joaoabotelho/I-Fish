import numpy as np 
import pickle 
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

FILE_NAME = './tests/response.wav' 
CLIENT_ACCESS_TOKEN = 'f0edfee5f0964102aac241ce5f13200b' 
speechRec = google1.speechRecognition(CLIENT_ACCESS_TOKEN)

pygame.init()

GPIO.setmode(GPIO.BCM) 
GPIO.setup(25, GPIO.OUT)

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

def main():
    D2A = GPIO.PWM(25,100)
    D2A.start(0)

    norm = []
    durations = []
    const = 200
    running = 1
    i = 0
    try:
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
                D2A.ChangeDutyCycle(0)

                audio = speechRec.record()
                resp = speechRec.analyze(audio)
                print(resp)
                if resp[0]:
                    if not resp[2]:
                        test = AudioInformation('./responses/' + resp[1] + '.wav')
                        norm = test.normalized
                        durations = test.array_of_time
                        write_to_file('./responses/' + resp[1] + '-test.txt', test.array_of_time)
                        write_to_file('./responses/' + resp[1] + '-norm.txt', norm)
                    else:
                        durations = read_from_file('./responses/' + resp[1] + '-test.txt')
                        norm = read_from_file('./responses/' + resp[1] + '-norm.txt')
                    t_start_animation = time.time() # in seconds ---------x.x
                    pygame.mixer.music.load('./responses/' + resp[1] + '.wav')
                    pygame.mixer.music.play(0)
                i = 0

    except(KeyboardInterrupt, ValueError, Exception) as e:
        print(e)
        D2A.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
