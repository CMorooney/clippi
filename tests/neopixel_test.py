import time
import board
import neopixel

print('init neopixel')
pixels = neopixel.NeoPixel(board.D18, 12, auto_write=False, pixel_order=neopixel.GRBW)
print('neopixel did init')

time_step = 0.0001

while True:
  for pixel_index in range(12):
    for x in range(1, 255):
      pixels[pixel_index] = (0, 0, 0, x)
      pixels.show()
      time.sleep(time_step)

  for pixel_index in range(12):
    for x in reversed(range(1, 255)):
      pixels[pixel_index] = (0, 0, 0, x)
      pixels.show()
      time.sleep(time_step)
