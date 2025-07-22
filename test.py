import numpy as np
import matplotlib.pyplot as plt

# Parameters
G = 1.0           # Gravitational constant
dt = 0.1         # Time step
steps = 1000      # Number of simulation steps
N = 3             # Number of bodies
softening = 0.2   # Softening length (epsilon)

# Initial positions (x, y), velocities (vx, vy), and masses
pos = np.random.randn(N, 2)
vel = np.random.randn(N, 2) * 0.1
mass = np.ones(N)

# Simulation loop
for step in range(steps):
    acc = np.zeros_like(pos)
    for i in range(N):
        for j in range(N):
            if i != j:
                r = pos[j] - pos[i]
                dist2 = np.dot(r, r) + softening**2
                acc[i] += G * mass[j] * r / dist2**1.5
    vel += acc * dt
    pos += vel * dt

    plt.clf()
    plt.scatter(pos[:, 0], pos[:, 1])
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    plt.pause(0.1)

plt.show()