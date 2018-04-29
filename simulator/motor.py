import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)

GPIO.output(25,True)
sleep(1)
GPIO.output(25,False)
sleep(1)

GPIO.output(25,True)
sleep(1)
GPIO.output(25,False)
sleep(1)

GPIO.cleanup()