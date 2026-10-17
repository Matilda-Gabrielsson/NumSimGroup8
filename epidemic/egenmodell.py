import numpy as np
import matplotlib.pyplot as plt
from gillespie import SSA

def stoch():
    return np.array([
    [-1,  1,  0,  0,  0,  0,  0,  0],  # S -> E
    [ 0, -1,  1,  0,  0,  0,  0,  0],  # E -> I
    [ 0,  0, -1,  1,  0,  0,  0,  0],  # I -> R
    [-1,  0,  0,  0,  0,  1,  0,  0],  # S -> V1
    [ 0,  0,  0,  0,  0, -1,  1,  0],  # V1 -> V2
    [ 0,  0,  0,  0,  0,  0, -1,  1],  # V2 -> M
    [ 0,  1,  0,  0,  0, -1,  0,  0],  # V1 -> E
    [ 0,  1,  0,  0,  0,  0, -1,  0],  # V2 -> E
    [ 0,  0, -1,  0,  1,  0,  0,  0]   # I -> D
])

def prop(X, coeff):
    S, E, I, R, D, V1, V2, M = X

    beta, alpha, gamma, N, v1, v2, omega, k1, k2, mu = coeff

    p1 = beta * S * I / N # p1, p2, p3 är samma som tidigare modeller
    p2 = alpha * E 
    p3 = gamma * I 

    if S > 0: # kollar om det finns mottagliga personer 
        p4 = v1 # antar konstant vaccinationstakt
    else:
        p4 = 0

    p5 = v2 * V1 # dos 2 beror på hur många som redan fått dos 1
    p6 = omega * V2 # beskriver hur snabbt en person blir immun efter dos 2
    p7 = k1 * beta * V1 * I / N # en med dos 1 blir smittad med smittrisk k1
    p8 = k2 * beta * V2 * I / N # en med dos 2 blir smittad med smittrisk k2
    p9 = mu * I # samma som tidigare modell

    return np.array([p1, p2, p3, p4, p5, p6, p7, p8, p9])

N = 1000
beta = 0.3
alpha = 1/5 # antar fem dagar inkubationstid
gamma = 1/7

v1 = 5 # låt fem personer vaccineras per dag
v2 = 1/21 # antar att dos 2 tas tre veckor efter dos 1
omega = 1/7 # antar att det tar sju dagar att bli immun
k1 = 0.5 # låt smittrisken halveras efter dos 1
k2 = 0.1 # låt smittrisken minskar med 90% efter dos 2
mu = 0.01 # antar dödlighetstakt på 0,01

X0 = np.array([995, 0, 5, 0, 0, 0, 0, 0])

t_span = [0, 120]

coeff = [beta, alpha, gamma, N, v1, v2, omega, k1, k2, mu]

t, X = SSA(prop, stoch, X0, t_span, coeff)

plt.step(t, X[:, 0], where="post", label="S")
plt.step(t, X[:, 1], where="post", label="E")
plt.step(t, X[:, 2], where="post", label="I")
plt.step(t, X[:, 3], where="post", label="R")
plt.step(t, X[:, 4], where="post", label="D")
plt.step(t, X[:, 5], where="post", label="V1")
plt.step(t, X[:, 6], where="post", label="V2")
plt.step(t, X[:, 7], where="post", label="M")

plt.xlabel("Tid (dagar)")
plt.ylabel("Antal personer")
plt.title("Smittspridning med vaccination och dödlighet")
plt.legend()
plt.grid()
plt.show()