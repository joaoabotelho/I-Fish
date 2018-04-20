import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)    # set GPIO 25 as output for the PWM signal
D2A = GPIO.PWM(25, 1000)    # create object D2A for PWM on port 25 at 1KHz
D2A.start(0)                # start the PWM with a 0 percent duty cycle (off)

try:

    while True:
        dutycycle = input('Enter a duty cycle percentage from 0-100 : ')
        print "Duty Cycle is : {0}%".format(dutycycle)
        D2A.ChangeDutyCycle(dutycycle)
        sleep(2)

except (KeyboardInterrupt, ValueError, Exception) as e:
    print(e)
    D2A.stop()     # stop the PWM output
    GPIO.cleanup() # clean up GPIO on CTRL+C exit

