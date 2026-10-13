import numpy as np
import random
import matplotlib.pyplot as plt

def stoch():
    return np.array([
    [-1,  1,  0,  0,  0,  0],  
    [ 0, -1,  1,  0,  0,  0],  
    [ 0,  0, -1,  1,  0,  0],  
    [ 0,  0, -1,  0,  1,  0],  
    [-1,  0,  0,  0,  0,  1]   
])

def prop(X, coeff):
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

N = 1000
beta = 0.3
alpha = 1/5
gamma = 1/7
mu = 0.02
v = 5

X0 = np.array([995, 0, 5, 0, 0, 0])
t_span = [0, 120]

coeff = [beta, alpha, gamma, mu, v, N]

def SSA(prop,stoch,X0,tspan,coeff):
    tvec=np.zeros(1)
    tvec[0]=tspan[0]
    Xarr=np.zeros([1,len(X0)])
    Xarr[0,:]=X0
    t=tvec[0]
    X=X0
    sMat=stoch()
    while t<tspan[1]:
        re=prop(X,coeff)
        a0=sum(re)
        if a0>1e-10:
            # Bestäm reaktionstid
            r1=random.random()
            tau=-np.log(r1)/a0
            t+=tau
            tvec=np.append(tvec,t)
            # Bestäm vilken reaktion
            r2=random.random()
            cre=np.cumsum(re)
            cre=cre/cre[-1]
            r=0
            while cre[r]<r2:
                r+=1
            X=X+sMat[r,:]
            Xarr=np.vstack([Xarr,X])
        else: # Alla reaktionshastigheter 0
            print('Simuleringen avslutad vid t=', t)
            return tvec, Xarr
    return tvec, Xarr

t, X = SSA(prop, stoch, X0, t_span, coeff)

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

