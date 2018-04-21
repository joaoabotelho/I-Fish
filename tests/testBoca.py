import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)

step = 0.005

bps = 5
tempo = 1.0/(bps*2.0)
isUp = False

#raw_input("Press anything to start")

startTime = time.time() 
lastDownTime = startTime
lastUpTime = startTime

while True:
#do
    sleep(step)
    if(isUp):
        diffTime = time.time()- lastUpTime
    else:
        diffTime = time.time()- lastDownTime
        
    if(diffTime > tempo):
        if(isUp):
            lastDownTime = time.time()
        else:
            lastUpTime = time.time()
        isUp = not isUp
        GPIO.output(25,isUp)


    
        
