import numpy as np
import matplotlib.pyplot as plt
from gillespie import SSA
from scipy.integrate import solve_ivp
from matplotlib.lines import Line2D
# from SIR import propSIR, stochSIR, X0, t_span, coeff
# from epidemic import SIR, Y0
# from SEIRD import propSEIRD, stochSEIRD, X0, t_span, coeff

from SEIRDV import propSEIRDV, stochSEIRDV, X0, t_span, coeff

t_runs = []
X_runs = []

for j in range(10):
    t, X = SSA(propSEIRDV, stochSEIRDV, X0, t_span, coeff)
    t_runs.append(t)
    X_runs.append(X)

# sol = solve_ivp(SIR, t_span, Y0, t_eval=np.linspace(*t_span, 500))

plt.figure()

for i in range(10):
    # plt.plot(t_runs[i], X_runs[i][:,0],'b-', alpha=0.3)
    # plt.plot(t_runs[i], X_runs[i][:,1],'r-', alpha=0.3)
    # plt.plot(t_runs[i], X_runs[i][:,2],'g-', alpha=0.3)

    plt.plot(t_runs[i], X_runs[i][:, 0], color="C0")#, label="S")  # blå
    plt.plot(t_runs[i], X_runs[i][:, 1], color="C1")#, label="E")  # orange
    plt.plot(t_runs[i], X_runs[i][:, 2], color="C2")#, label="I")  # grön
    plt.plot(t_runs[i], X_runs[i][:, 3], color="C3")#, label="R")  # röd
    plt.plot(t_runs[i], X_runs[i][:, 4], color="C4")#, label="D")  # lila
    plt.plot(t_runs[i], X_runs[i][:, 5], color="C5")#, label="D")  # lila

# plt.plot(sol.t, sol.y[0], 'b', lw=3, label="Mottagliga (S)")
# plt.plot(sol.t, sol.y[1], 'r', lw=3, label="Infekterade (I)")
# plt.plot(sol.t, sol.y[2], 'g', lw=3, label="Tillfrisknade (R)")



colors = ["C0", "C1", "C2", "C3", "C4", "C5"]
labels = ["S", "E", "I", "R", "D", "V"]

handles = [Line2D([0], [0], color=c, lw=2, label=l) for c, l in zip(colors, labels)]
plt.xlabel("Tid (dagar)")
plt.ylabel("Antal personer")
plt.title("SEIRDV-modell")
plt.legend(handles=handles)


# plt.legend()
plt.show()