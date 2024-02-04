import RPi.GPIO as GPIO
from time import sleep

led1 = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(led1, GPIO.OUT, initial=GPIO.LOW)

while True:
    GPIO.output(led1, GPIO.LOW)
    sleep(1)
    GPIO.output(led1, GPIO.HIGH)
    sleep(1)
