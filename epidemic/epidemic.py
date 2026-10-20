import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def SIR(t, y):
    S, I, R = y

    dSdt = -beta * I/N * S
    dIdt = beta * I/N * S - gamma * I
    dRdt = gamma * I

    return [dSdt, dIdt, dRdt]

N = 1000
beta = 0.3
gamma = 1/7

S0 = 995
I0 = 5
R0 = 0

Y0 = [S0, I0, R0]
t_span = [0, 120]
if __name__ == "__main__":
    sol = solve_ivp(SIR, t_span, [995, 5, 0], t_eval=np.linspace(*t_span, 500))

    plt.plot(sol.t, sol.y[0], label="Mottagliga (S)")
    plt.plot(sol.t, sol.y[1], label="Infekterade (I)")
    plt.plot(sol.t, sol.y[2], label="Tillfrisknade (R)")

    plt.xlabel("Tid (dagar)")
    plt.ylabel("Antal personer")
    plt.title("SIR-modellen")
    plt.legend()
    plt.show()