import numpy as np
import matplotlib.pyplot as plt
from gillespie import SSA

def stochSEIRDV():
    return np.array([
    [-1,  1,  0,  0,  0,  0],  
    [ 0, -1,  1,  0,  0,  0],  
    [ 0,  0, -1,  1,  0,  0],  
    [ 0,  0, -1,  0,  1,  0],  
    [-1,  0,  0,  0,  0,  1]   
])


def propSEIRDV(X, coeff):
    S, E, I, R, D, V = X
    beta, alpha, gamma, mu, v, N = coeff

    p1 = beta * S * I / N
    p2 = alpha * E
    p3 = gamma * I
    p4 = mu * I
    if S > 0:
        p5 = v 
    else: 
        p5 = 0

    return np.array([p1, p2, p3, p4, p5])

beta = 0.3
alpha = 1/5
gamma = 1/7
mu = 0.02
v = 5
N = 1000
coeff = [beta, alpha, gamma, mu, v, N]

X0 = np.array([995, 0, 5, 0, 0, 0])

t_span = [0, 120]

t, X = SSA(propSEIRDV, stochSEIRDV, X0, t_span, coeff)

plt.step(t, X[:, 0], where="post", label="S")
plt.step(t, X[:, 1], where="post", label="E")
plt.step(t, X[:, 2], where="post", label="I")
plt.step(t, X[:, 3], where="post", label="R")
plt.step(t, X[:, 4], where="post", label="D")
plt.step(t, X[:, 5], where="post", label="V")

plt.xlabel("Tid (dagar)")
plt.ylabel("Antal personer")
plt.title("SEIRDV-modell")
plt.legend()
plt.grid()
plt.show()