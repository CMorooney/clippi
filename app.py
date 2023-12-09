import os
import time
import board
import RPi.GPIO as GPIO
import neopixel
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(f'/home/calvin/App/.env')
load_dotenv(dotenv_path=dotenv_path)

APP_PATH = os.getenv('APP_PATH')
BANKS_PATH = os.getenv('BANKS_PATH')
BANK_COUNT = os.getenv('BANK_COUNT')

for x in range(1, int(BANK_COUNT)):
    path = f'{BANKS_PATH}/{str(x).zfill(2)}'
    print(f'create path {path}')
    # Create directory /path/to/nested/directory if it doesn't already exist
    os.makedirs(path, exist_ok=True)

pixels = neopixel.NeoPixel(board.D18, 12, brightness=0.1, auto_write=False, pixel_order=neopixel.GRBW)

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

button1_down = False;
button2_down = False;
button3_down = False;
button4_down = False;
button5_down = False;
button6_down = False;

while 1:
  button1_down = not GPIO.input(button1_pin)
  button2_down = not GPIO.input(button2_pin)
  button3_down = not GPIO.input(button3_pin)
  button4_down = not GPIO.input(button4_pin)
  button5_down = not GPIO.input(button5_pin)
  button6_down = not GPIO.input(button6_pin)

  pc1 = 255 if button1_down else 0
  pixels[0] = (0, 0, 0, pc1)
  pixels[0] = (0, 0, 0, pc1)
  pixels[1] = (0, 0, 0, pc1)
  pixels[1] = (0, 0, 0, pc1)

  pc2 = 255 if button2_down else 0
  pixels[2] = (0, 0, 0, pc2)
  pixels[2] = (0, 0, 0, pc2)
  pixels[3] = (0, 0, 0, pc2)
  pixels[3] = (0, 0, 0, pc2)

  pc3 = 255 if button3_down else 0
  pixels[4] = (0, 0, 0, pc3)
  pixels[4] = (0, 0, 0, pc3)
  pixels[5] = (0, 0, 0, pc3)
  pixels[5] = (0, 0, 0, pc3)

  pc4 = 255 if button4_down else 0
  pixels[6] = (0, 0, 0, pc4)
  pixels[6] = (0, 0, 0, pc4)
  pixels[7] = (0, 0, 0, pc4)
  pixels[7] = (0, 0, 0, pc4)

  pc5 = 255 if button5_down else 0
  pixels[8] = (0, 0, 0, pc5)
  pixels[8] = (0, 0, 0, pc5)
  pixels[9] = (0, 0, 0, pc5)
  pixels[9] = (0, 0, 0, pc5)

  pc6 = 255 if button6_down else 0
  pixels[10] = (0, 0, 0, pc6)
  pixels[10] = (0, 0, 0, pc6)
  pixels[11] = (0, 0, 0, pc6)
  pixels[11] = (0, 0, 0, pc6)

  pixels.show()
