import numpy as np

def epidemicODE(t, Y, coeff):
    S, I, R = Y
    beta, gamma, N = coeff
    yder = [-beta * I / N * S, beta * I / N * S - gamma * I, gamma * I]

    return np.array(yder)