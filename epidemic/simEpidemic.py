
import epidemicgill as ep
import epidemicODE as epODE
from gillespie import SSA
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

S0 = 995
I0 = 5
R0 = 0
Y0 = (S0, I0, R0)

beta = 0.3
gamma = 1/7
N = 1000
coeff = (beta, gamma, N)

t0 = 0
t_end = 120
tspan = (t0, t_end)

a = ep.propEpidemic(np.array(Y0), coeff)
print(a, np.sum(a))

t, X = SSA(ep.propEpidemic, ep.stochEpidemic, Y0, tspan, coeff)

plt.figure(1)
plt.plot(t, X[:,0],'b-', label="S")

plt.plot(t, X[:,1],'r-', label="I")

plt.plot(t, X[:,2],'g-', label="R")

ax1 = plt.gca()
xmin, xmax, ymin, ymax = ax1.axis()
ax1.set(xlim=(0,xmax), ylim=(0, ymax))
plt.title("SIR, stochastic")
plt.legend()
plt.show()