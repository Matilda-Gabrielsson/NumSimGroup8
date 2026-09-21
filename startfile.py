import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

g = np.array([0, -9.82])
c = 0.05
km = 700

def theta(t):
    return np.pi/2

def mass(t):
    if t <= 10:
        mass = 8 - 0.4 * t
    else:
        mass = 4
    return mass

def massa_derivata(t):
    if t < 10:
        return -0.4
    else:
        return 0
    
def raketbana(t, Y):
    x = Y[0]
    y = Y[1]
    vx = Y[2]
    vy = Y[3]

    m = mass(t)
    m_der = massa_derivata(t)

    u = np.array([
        km * np.cos(theta(t)),
        km * np.sin(theta(t))
    ])

    v = np.array([vx, vy])
    v_norm = np.linalg.norm(v)
    
    luft = c * v_norm * v
    
    F = m * g - luft
    a = F/m + m_der/m * u

    ax = a[0]
    ay = a[1]

    return [vx, vy, ax, ay]


y0 = [0, 0, 0, 0]

t_span = [0, 10]

sol = solve_ivp( raketbana, t_span, y0)

target_x = 80
target_y = 60
sol = solve_ivp(raketbana, tspan, y0, t_eval=t_punkter)
plt.plot(target_x, target_y, 'o')
plt.plot(sol.t, sol.y[0], 'o-g')
plt.show()