import board
import digitalio
import ulab.numpy as np
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Parameters
G = 1.0          # Gravitational constant
dt = 0.1         # Time step
N = 3             # Number of bodies
softening = 0.2   # Softening length (epsilon)

# Initial positions (x, y), velocities (vx, vy), and masses
pos = np.array([[3,3], [2,2], [1,1]])
vel = np.array([[0,0], [0,0], [0,0]])
mass = np.ones(N)

cols = 6 
rows = 5

bin_edges = [np.arange(0, rows+1), np.arange(0, cols+1)]
print(bin_edges)

while True:
    led.value = True
    acc = np.zeros(pos.shape)
    for i in range(N):
        for j in range(N):
            if i != j:
                r = pos[j] - pos[i]
                dist2 = np.dot(r, r) + softening**2
                acc[i] += G * mass[j] * r / dist2**1.5
    vel += acc * dt
    pos += vel * dt

    led.value = False
    time.sleep(0.5)
