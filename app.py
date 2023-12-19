import os
import time
import board
import RPi.GPIO as GPIO
import neopixel
import subprocess
import keyboard
from pexpect import spawn
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(f'/home/calvin/App/.env')
load_dotenv(dotenv_path=dotenv_path)

APP_PATH = os.getenv('APP_PATH')
BANKS_PATH = os.getenv('BANKS_PATH')
BANK_COUNT = os.getenv('BANK_COUNT')

GPIO.setmode(GPIO.BCM)

# Create bank directories if they don't exist
for x in range(1, int(BANK_COUNT) + 1):
    path = f'{BANKS_PATH}/{str(x).zfill(2)}'
    try:
        original_umask = os.umask(0)
        os.makedirs(path, mode=0o777, exist_ok=True)
    finally:
        os.umask(original_umask)

# init neo pixels
pixels = neopixel.NeoPixel(board.D18, 12, brightness=0.1, auto_write=False, pixel_order=neopixel.GRBW)

# power on GPIO
power_led_pin = 27
GPIO.setup(power_led_pin, GPIO.OUT, initial=GPIO.LOW)

# start playing video (todo, playlist)
mplayer_spawn = spawn('mplayer -fs -vo fbdev2 -nosound -vf scale=720:480 -loop 0 -slave -quiet "/home/calvin/App/__CONTENT/01/03__Carrier Fortress at Sea - Panasonic 3DO - Archive Gameplay 🎮.mp4"')

# set up button GPIO
mode_button_pin = 22;
prev_button_pin = 5;
play_pause_button_pin = 6;
next_button_pin = 13;
hold_button_pin = 19;
shift_button_pin = 26;

GPIO.setup(mode_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(prev_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(play_pause_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(next_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(hold_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(shift_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# clip actions
def change_mode():
    print('change_mode')

def previous_clip():
    print('previous clip')

def play_pause():
    mplayer_spawn.write("pause\n")

def next_clip():
    print('next clip')

def hold_current_clip():
    print('hold current clip')

def shift_button():
    print('shift button')

# set up button GPIO callbacks
button_bounce_time = 200

def button_pushed(button):
        if button == mode_button_pin:
            change_mode()
        elif button == prev_button_pin:
            previous_clip()
        elif button == play_pause_button_pin:
            play_pause()
        elif button == next_button_pin:
            next_clip()
        elif button == hold_button_pin:
            hold_current_clip()
        elif button == shift_button_pin:
            shift_button()

GPIO.add_event_detect(mode_button_pin, GPIO.FALLING, callback=button_pushed, bouncetime=button_bounce_time)
GPIO.add_event_detect(prev_button_pin, GPIO.FALLING, callback=button_pushed, bouncetime=button_bounce_time)
GPIO.add_event_detect(play_pause_button_pin, GPIO.FALLING, callback=button_pushed, bouncetime=button_bounce_time)
GPIO.add_event_detect(next_button_pin, GPIO.FALLING, callback=button_pushed, bouncetime=button_bounce_time)
GPIO.add_event_detect(hold_button_pin, GPIO.FALLING, callback=button_pushed, bouncetime=button_bounce_time)
GPIO.add_event_detect(shift_button_pin, GPIO.FALLING, callback=button_pushed, bouncetime=button_bounce_time)

# show power on
GPIO.output(power_led_pin, GPIO.HIGH)


keyboard.wait()

# show power off
GPIO.output(power_led_pin, GPIO.LOW)
