import numpy as np
import matplotlib.pyplot as plt
from gillespie import SSA

def stochSIR():
    M = np.array([[-1, 1, 0], \
                  [0, -1, 1]])
    return M

def propSIR(X, coeff):
    beta = coeff[0]
    gamma = coeff[1]
    N = coeff[2]
    
    p = np.array([beta * X[1] / N * X[0], gamma* X[1]])
    return p

beta = 0.3
gamma = 1/7
N = 1000
coeff = (beta, gamma, N)

S0 = 995
I0 = 5
R0 = 0
X0 = np.array([S0, I0, R0])

t0 = 0
t_end = 120
t_span = (t0, t_end)
if __name__ == "__main__":
    t, X = SSA(propSIR, stochSIR, X0, t_span, coeff)

    plt.figure(1)
    plt.plot(t, X[:,0],'b-', label="S")

    plt.plot(t, X[:,1],'r-', label="I")

    plt.plot(t, X[:,2],'g-', label="R")

    # ax1 = plt.gca()
    # xmin, xmax, ymin, ymax = ax1.axis()
    # ax1.set(xlim=(0,xmax), ylim=(0, ymax))
    plt.title("SIR, stochastic")
    plt.legend()
    plt.show()