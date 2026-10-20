import numpy as np
import matplotlib.pyplot as plt
from gillespie import SSA

def stochSEIR():
    M = np.array([[-1, 1, 0, 0], \
                  [0, -1, 1, 0], \
                  [0, 0, -1, 1]])
    return M

def propSEIR(X, coeff):
    beta, gamma, alfa, N = coeff
    S, E, I, R = X

    p1 = beta * I * S / N
    p2 = alfa * E
    p3 = gamma * I
    
    p = np.array([p1, p2, p3])
    return p

beta = 0.3
gamma = 1/7
alfa = 1/3 #3 dagar
N = 1000
coeff = [beta, gamma, alfa, N]

S0 = 995
E0 = 0
I0 = 5
R0 = 0
X0 = np.array([S0, E0, I0, R0])

t0 = 0
t_end = 120
t_span = (t0, t_end)

if __name__ == "__main__":
    t, X = SSA(propSEIR, stochSEIR, X0, t_span, coeff)

    plt.figure(1)
    plt.plot(t, X[:,0],'b-', label="S")

    plt.plot(t, X[:,1],'c-', label="E")

    plt.plot(t, X[:,2],'r-', label="I")

    plt.plot(t, X[:,3],'g-', label="R")

    # ax1 = plt.gca()
    # xmin, xmax, ymin, ymax = ax1.axis()
    # ax1.set(xlim=(0,xmax), ylim=(0, ymax))
    plt.title("SEIR, stochastic")
    plt.legend()
    plt.show()