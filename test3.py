import numpy as np
import board
import neopixel
from time import sleep

# Parameters
G = 1.0          # Gravitational constant
dt = 0.1         # Time step
N = 3             # Number of bodies
softening = 0.2   # Softening length (epsilon)

pixels = neopixel.NeoPixel(board.D18, 30, brightness=1)
pixels.fill((0,0,0))

# Initial positions (x, y), velocities (vx, vy), and masses
pos = np.random.randn(N, 2) + 3
vel = np.random.randn(N, 2) * 0.1

cols = 6 
rows = 5

bin_edges = [np.arange(0, rows+1), np.arange(0, cols+1)]

# Simulation loop
while True:
    acc = np.zeros_like(pos)
    for i in range(N):
        for j in range(N):
            if i != j:
                r = pos[j] - pos[i]
                dist2 = np.dot(r, r) + softening**2
                acc[i] += G * r / dist2**1.5
    vel += acc * dt
    pos += vel * dt

    grid, _,  _ = np.histogram2d(pos[:, 0], pos[:, 1], bin_edges)

    flattened_grid = grid.flatten()

    print(flattened_grid)

    for i, value in enumerate(flattened_grid):
        pixels[i] = (255 * value / N, 0, 0)

    sleep(1)

