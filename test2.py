import numpy as np
import matplotlib.pyplot as plt

# Parameters
G = 1.0          # Gravitational constant
dt = 0.1         # Time step
steps = 100     # Number of simulation steps
N = 3             # Number of bodies
softening = 0.2   # Softening length (epsilon)

# Initial positions (x, y), velocities (vx, vy), and masses
pos = np.random.randn(N, 2) + 3
vel = np.random.randn(N, 2) * 0.1
mass = np.ones(N)

cols = 6 
rows = 5

bin_edges = [np.arange(0, rows+1), np.arange(0, cols+1)]
print(bin_edges)

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

    grid, _,  _ = np.histogram2d(pos[:, 0], pos[:, 1], bin_edges)

    plt.clf()
    plt.imshow(grid, extent=[0, 6, 0, 5], origin='lower')
    plt.scatter(pos[:, 1], pos[:, 0], c='k')
    plt.xlim(0, 6)
    plt.ylim(0, 5)
    plt.pause(1.0)

# plt.show()