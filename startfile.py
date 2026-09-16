import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def theta(t):
    return 1

def mass(t):
    if t <= 10:
        mass = 8 - 0.4 * t
    else:
        mass = 4
    return mass


def raketbana(t, y):
    return 0

km = 700

u = np.array([
    km * np.cos(theta(t)),
    km * np.sin(theta(t))
])

tspan = [0, 10]

target_x = 80
target_y = 60
plt.plot(target_x, target_y, 'o')
plt.show()