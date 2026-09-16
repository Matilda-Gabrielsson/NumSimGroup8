import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Raketens bana kan beräknas med Newtons rörelselagar i följande differentialekvation

# m(t)a(t) = F + m'(t)u(t)

# F = m(t)g − 0.05||v(t)||v(t)

# u(t)= (ux(t), uy(t)) = (700*cos(-pi/2), 700*sin(-pi/2))


# def ode_Y(t, y):
#     yder=np.zeros(1)
#     yder[0]= y[1]
#     yder[1]=-0.4
#     return yder

# v0 = [0]

# m0 = [8, -0.4]

# y0 = [(0,0)]

# t_eval= [0, 10, 200]
# tspan = [0, 10]

# sol = solve_ivp(ode_Y, tspan, y0,  t_eval=t_eval)

# plt.plot(sol.t, sol.y[0])
# plt.xlabel("t")
# plt.ylabel("m(t)a(t)")
# plt.show()


# hejhej
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
plt.plot(target_x, target_y, 'o')
plt.plot(sol.t, sol.y[0], 'o-g')
plt.show()