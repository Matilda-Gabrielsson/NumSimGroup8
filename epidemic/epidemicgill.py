import numpy as np

def stochEpidemic():
    M = np.array([[-1, 1, 0], \
                  [0, -1, 1]])
    return M

def propEpidemic(X, coeff):
    beta = coeff[0]
    gamma = coeff[1]
    N = coeff[2]
    
    p = np.array([beta * X[1] / N * X[0], gamma* X[1]])
    return p