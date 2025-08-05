import numpy as np
import board
import keypad
import neopixel
from time import sleep
from adafruit_seesaw import digitalio, rotaryio, seesaw

ORDER = neopixel.GRB

def rainbow(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in {neopixel.RGB, neopixel.GRB} else (r, g, b, 0)



# Parameters
G = 1.0          # Gravitational constant
dt = 0.1         # Time step
softening = 0.5   # Softening length (epsilon)

pixels = neopixel.NeoPixel(board.D18, 30, brightness=1)

# set all pixels to 0
pixels.fill((0,0,0))

# Initial positions (x, y), velocities (vx, vy), and masses
pos = None
vel = None

cols = 6
rows = 5

bin_edges = [np.arange(0, rows+1), np.arange(0, cols+1)]

keys = keypad.KeyMatrix(
    row_pins=(board.D21, board.D20, board.D16, board.D12, board.D1),
    column_pins=(board.D26, board.D19, board.D13, board.D6, board.D5, board.D0),
    columns_to_anodes=False,
)


def key_to_pixel_map(key_number):
    row = key_number // cols
    column = (key_number % cols)
    return row, column


pixels.fill((0, 0, 0))  # Begin with pixels off.

    
# Simulation loop
while True:

    key_event = keys.events.get()
    if key_event:

        if key_event.pressed:

            # get the row and column
            row, col = key_to_pixel_map(key_event.key_number)

            print('added at', row, col)

            # add a particle to that position...

            if pos is None:
                pos = np.array([[float(row)+0.5, float(col)+0.5]])
                vel = np.array([[0., 0.]])
            else:
                pos = np.append(pos, np.array([[float(row)+0.5, float(col)+0.5]]), axis=0)
                vel = np.append(vel, np.array([[0, 0]]), axis=0)
        
            print(pos)

    if pos is not None:

        N = len(pos)

        acc = np.zeros_like(pos)
        for i in range(N):
            for j in range(N):
                if i != j:
                    r = pos[j] - pos[i]
                    dist2 = np.dot(r, r) + softening**2
                    acc[i] += G * r / dist2**1.5

        vel += acc * dt
        pos += vel * dt
        # print('-----------')
        # print(acc)
        # print(vel)
        # print(pos)

        # make a histogram of the positions
        grid, _,  _ = np.histogram2d(pos[:, 0], pos[:, 1], bin_edges)

        # make a flattened version
        flattened_grid = grid.flatten()

        # loop over the cells and set the pixel value appropriately

        for cell, value in enumerate(flattened_grid):

            # the ordering of the cells is different from the LEDs
            row = cell // cols
            col = cell % cols
            if row % 2 == 1:
                col = cols - col - 1
            pixel = row * cols + col

            # pixels[i] = (255 * value / N, 0, 0)
            if value > 0:
                pixels[pixel] = rainbow(value * 10)
            else:
                pixels[pixel] = (0, 0, 0)

        sleep(0.01)
