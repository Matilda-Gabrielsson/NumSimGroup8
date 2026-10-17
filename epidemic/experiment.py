import numpy as np
import matplotlib.pyplot as plt
from gillespie import SSA
from scipy.integrate import solve_ivp
from SIR import propSIR, stochSIR, X0, t_span, coeff
from epidemic import SIR, Y0

t_runs = []
X_runs = []

for j in range(10):
    t, X = SSA(propSIR, stochSIR, X0, t_span, coeff)
    t_runs.append(t)
    X_runs.append(X)

sol = solve_ivp(SIR, t_span, Y0, t_eval=np.linspace(*t_span, 500))

plt.figure()

for i in range(10):
    plt.plot(t_runs[i], X_runs[i][:,0],'b-', alpha=0.3)
    plt.plot(t_runs[i], X_runs[i][:,1],'r-', alpha=0.3)
    plt.plot(t_runs[i], X_runs[i][:,2],'g-', alpha=0.3)

plt.plot(sol.t, sol.y[0], 'b', lw=3, label="Mottagliga (S)")
plt.plot(sol.t, sol.y[1], 'r', lw=3, label="Infekterade (I)")
plt.plot(sol.t, sol.y[2], 'g', lw=3, label="Tillfrisknade (R)")

plt.legend()
plt.show()