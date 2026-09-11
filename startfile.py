import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Raketens bana kan beräknas med Newtons rörelselagar i följande differentialekvation
# m(t)¯a(t) = ¯F + m′(t)¯u(t)

def ode_Y(t, y):
    yder=np.zeros(1)
    yder[0]= y[1]
    yder[1]=-0.4
    return yder

v0 = [0]

m0 = [8, -0.4]

t_eval= []

sol = solve_ivp(ode_Y, )

plt.plot(sol.t, sol.y[0])
plt.xlabel("t")
plt.ylabel("m(t)a(t)")
plt.show()


# hejhej

# funkar det nu
