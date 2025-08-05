import board
import neopixel


ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(board.D2, 30, brightness=1)

# set all pixels to 0
pixels.fill((255,0,0))