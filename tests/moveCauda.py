import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)

step = 0.005
timeUp = 0.3
timeGotUp = 0
isUp = False

file_object = open("skyfallBeatTimes",'r')
string = file_object.read()
s_times = string.split(", ")

raw_input("Press anything to start")

startTime = time.time() 

for s_time in s_times:
    d_time = float("{0:.2f}".format(float(s_time)))
    while True:
    #do
        sleep(step)
        diffTime = time.time()-startTime
        if isUp:
            #print "."
            upTime = time.time()-timeGotUp
            if(upTime >= timeUp):
                GPIO.output(25,False)
                isUp = False
      #while(not)
        if(diffTime >= d_time):
            break
    #beat
    GPIO.output(25,True)
    timeGotUp = time.time()
    isUp = True
    #print str(d_time) + " | " + str(diffTime)

GPIO.cleanup()

    
        
