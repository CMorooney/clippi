import os
import time
import board
import RPi.GPIO as GPIO
import neopixel
import subprocess
import keyboard
import queue
from threading import Thread
from pexpect import spawn
from dotenv import load_dotenv
from pathlib import Path
from os import listdir

dotenv_path = Path(f'/home/calvin/App/.env')
load_dotenv(dotenv_path=dotenv_path)

APP_PATH = os.getenv('APP_PATH')
BANKS_PATH = os.getenv('BANKS_PATH')
BANK_COUNT = os.getenv('BANK_COUNT')

total_pixels = 12

GPIO.setmode(GPIO.BCM)

# using a queue to issue commands to the mplayer slave in a thread
mplayer_command_queue = queue.Queue()

# Create bank directories if they don't exist
for x in range(1, int(BANK_COUNT) + 1):
    path = f'{BANKS_PATH}/{str(x).zfill(2)}'
    try:
        original_umask = os.umask(0)
        os.makedirs(path, mode=0o777, exist_ok=True)
    finally:
        os.umask(original_umask)

# init neo pixels
pixels = neopixel.NeoPixel(board.D18, 12, auto_write=False, pixel_order=neopixel.GRBW)

# power on GPIO
power_led_pin = 27
GPIO.setup(power_led_pin, GPIO.OUT, initial=GPIO.LOW)

# get videos in bank directory as a single string
videos_string = ' '.join(sorted(map(lambda f: BANKS_PATH + '/' + '01/' + f.replace(' ', '\ '), os.listdir(BANKS_PATH + '/' + '01/'))))
# start playing playlist
mplayer_spawn = spawn('/usr/bin/mplayer -fs -vo fbdev2 -nosound -vf scale=720:480 -loop 0 -slave -quiet ' + videos_string)

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
    mplayer_command_queue.put("pt_step -1\n")

def play_pause():
    mplayer_command_queue.put("pause\n")

def next_clip():
    mplayer_command_queue.put("pt_step 1\n")

def hold_current_clip():
    print('hold current clip')

def shift_button():
    print('shift button')

# set up button GPIO callbacks
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
button_bounce_time = 200
GPIO.add_event_detect(mode_button_pin, GPIO.FALLING, callback=button_pushed, bouncetime=button_bounce_time)
GPIO.add_event_detect(prev_button_pin, GPIO.FALLING, callback=button_pushed, bouncetime=button_bounce_time)
GPIO.add_event_detect(play_pause_button_pin, GPIO.FALLING, callback=button_pushed, bouncetime=button_bounce_time)
GPIO.add_event_detect(next_button_pin, GPIO.FALLING, callback=button_pushed, bouncetime=button_bounce_time)
GPIO.add_event_detect(hold_button_pin, GPIO.FALLING, callback=button_pushed, bouncetime=button_bounce_time)
GPIO.add_event_detect(shift_button_pin, GPIO.FALLING, callback=button_pushed, bouncetime=button_bounce_time)

# show power on
GPIO.output(power_led_pin, GPIO.HIGH)

def neopixel_update(percent):
  # can be 0-255
  max_brightness = 150;

  # pixel_step is what each whole pixel represents in %
  pixel_step = 100/total_pixels

  # numPixels is the number of pixels starting from 0 to light up fully
  num_pixels = percent//pixel_step

  # remainder is how much to dimly light the next pixel
  remainder = percent % pixel_step

  brightness_step = max_brightness/pixel_step

  for pixel_index in range(total_pixels):
    if pixel_index == num_pixels:
      pixels[pixel_index] = (0, 0, 0, remainder * brightness_step)
    elif pixel_index > num_pixels:
      pixels[pixel_index] = (0, 0, 0, 0)
    else:
      pixels[pixel_index] = (0, 0, 0, max_brightness)

  pixels.show()


def mplayer_command_thread_execute():
  while True:
      # dump the command queue into the stdin
      while not mplayer_command_queue.empty():
          command = mplayer_command_queue.get()
          mplayer_spawn.write(command)
          time.sleep(0.1)

      # request current percent_pos from mplayer
      mplayer_spawn.write("pausing_keep_force get_percent_pos\n")

      # wait for proper response
      mplayer_spawn.expect_exact(["ANS_PERCENT_POSITION="])

      # parse response to int 1-100
      percent = int(mplayer_spawn.readline().rstrip())

      # update neopixel progress indication
      neopixel_update(percent)

      time.sleep(0.1)

mplayer_command_thread = Thread(target = mplayer_command_thread_execute)
mplayer_command_thread.daemon=True
mplayer_command_thread.start()

keyboard.wait()

# show power off
GPIO.output(power_led_pin, GPIO.LOW)
