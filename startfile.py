import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Raketens bana kan beräknas med Newtons rörelselagar i följande differentialekvation

# m(t)a(t) = F + m'(t)u(t)

# F = m(t)g − 0.05||v(t)||v(t)

# u(t)= (ux(t), uy(t)) = (700*cos(-pi/2), 700*sin(-pi/2))


def ode_Y(t, y):
    yder=np.zeros(1)
    yder[0]= y[1]
    yder[1]=-0.4
    return yder

v0 = [0]

m0 = [8, -0.4]

y0 = [(0,0)]

t_eval= [0, 10, 200]
tspan = [0, 10]

sol = solve_ivp(ode_Y, tspan, y0,  t_eval=t_eval)

plt.plot(sol.t, sol.y[0])
plt.xlabel("t")
plt.ylabel("m(t)a(t)")
plt.show()


# hejhej

# funkar det nu


tspan = [0, 10]