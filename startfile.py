import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

g = np.array([0, -9.82])
c = 0.05
km = 700
target_x = 80
target_y = 60
    
def massa(t):
    if t <= 10:
        massa = 8 - 0.4 * t
    else:
        massa = 4
    return massa

def massa_derivata(t):
    if t < 10:
        return -0.4
    else:
        return 0
    
def styrning(x, y):
    theta = np.arctan2((target_y-y),(target_x-x))
    return theta

def reglering(x, y, m, vx, vy):
    theta = np.arctan2((target_y-y),(target_x-x))
    hastighet = np.arctan2((vy),(vx)) * -0.1 # o.5 hittepånummer 
    gravitation = np.pi/2 * 0.1 # 0.2 hittepånummer
    styrning = theta + hastighet + gravitation
    return styrning

def raketbana(t, Y):
    x = Y[0]
    y = Y[1]
    vx = Y[2]
    vy = Y[3]

    # print("x = ", x)
    # print("y = ", y)
    # print("vx = ", vx)
    # print("vy = ", vy)

    m = massa(t)
    m_der = massa_derivata(t)

    if y < 20:
        theta = np.pi/2
    else:
        theta = reglering(x, y, m, vx, vy)
        #theta = styrning(x, y)
        # print("theta = ", theta)


    v = np.array([vx, vy])
    # print("v = ", v)

    v_norm = np.linalg.norm(v)
    # print("v_norm = ", v_norm)
    
    luft = c * v_norm * v
    # print("luft = ", luft)
    
    F = m * g - luft
    # print("F = ", F)

    u = np.array([
            km * np.cos(theta),
            km * np.sin(theta)
        ])
    # print("u = ", u)

    a = F/m - m_der/m * u

    ax = a[0]
    ay = a[1]

    return np.array([vx, vy, ax, ay])

def stoppa(t, Y):
    x = Y[0]
    y = Y[1]

    avstand = np.sqrt((x - target_x)**2 + (y - target_y)**2)

    return avstand - 3

stoppa.terminal = True
stoppa.direction = -1

y0 = [0, 0, 0, 0]

t_span = [0, 10]
t_eval= np.linspace(0, 10, 200)

sol = solve_ivp( raketbana, t_span, y0, t_eval = t_eval, events=stoppa)

plt.plot(target_x, target_y, marker='*', markersize=15, color = 'orange')
plt.plot(sol.y[0], sol.y[1], 'm')
plt.plot(sol.y[0][-1], sol.y[1][-1], marker='^', markersize=8, color = 'm')
plt.show()


def runge_raket(f, tspan, u0, dt):
    interval = round((tspan[1]-tspan[0])/dt)
    tvec=np.linspace(tspan[0], tspan[1], interval +1)
    u=np.zeros((len(tvec),len(u0)))
    i=0
    u[i, :] = u0
    for t in tvec[0:len(tvec)-1]:
        k1 = f(t, u[i,:])
        k2 = f(t+dt/2, u[i,:]+(dt/2)*k1)
        k3 = f(t+dt, u[i,:]- dt*k1 + 2*dt*k2)
        k = (k1+4*k2+k3)/6
        u[i+1,:]=u[i,:]+dt*k
        i=i+1
    return tvec, u

t, u = runge_raket(raketbana, [0,10], y0, 0.01)


# plt.plot(u[:,1],u[:,0], "b", label="runge_kutta")
# plt.show()