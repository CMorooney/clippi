import time
import RPi.GPIO as GPIO

button1_pin = 22;
button2_pin = 5;
button3_pin = 6;
button4_pin = 13;
button5_pin = 19;
button6_pin = 26;

GPIO.setmode(GPIO.BCM)
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button4_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button5_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button6_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while 1:
  if not GPIO.input(button1_pin):
    print(f'button1 press')
  if not GPIO.input(button2_pin):
    print(f'button2 press')
  if not GPIO.input(button3_pin):
    print(f'button3 press')
  if not GPIO.input(button4_pin):
    print(f'button4 press')
  if not GPIO.input(button5_pin):
    print(f'button5 press')
  if not GPIO.input(button6_pin):
    print(f'button6 press')

