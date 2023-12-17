import RPi.GPIO as GPIO
from time import sleep

led1 = 27
led2 = 17
led3 = 23
led4 = 24
led5 = 12
led6 = 16
led7 = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(led1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led4, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led5, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led6, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led7, GPIO.OUT, initial=GPIO.LOW)

while True:
    GPIO.output(led1, GPIO.LOW)
    GPIO.output(led2, GPIO.LOW)
    GPIO.output(led3, GPIO.LOW)
    GPIO.output(led4, GPIO.LOW)
    GPIO.output(led5, GPIO.LOW)
    GPIO.output(led6, GPIO.LOW)
    GPIO.output(led7, GPIO.LOW)

    GPIO.output(led1, GPIO.HIGH)
    sleep(1)
    GPIO.output(led2, GPIO.HIGH)
    sleep(1)
    GPIO.output(led3, GPIO.HIGH)
    sleep(1)
    GPIO.output(led4, GPIO.HIGH)
    sleep(1)
    GPIO.output(led5, GPIO.HIGH)
    sleep(1)
    GPIO.output(led6, GPIO.HIGH)
    sleep(1)
    GPIO.output(led7, GPIO.HIGH)
    sleep(1)