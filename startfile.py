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

#Styrningsfunktion som i varje steg anpassar styrvinkeln baserat på raketens nuvarande avstånd i x- och y-led till målet
def styrning(x, y):
    theta = np.arctan2((target_y-y),(target_x-x))
    return theta

#Styrningsfunktion som har en konstant, optimal vinkel för att skicka raketen mot målet
#Vinkeln funnen mha experiment som finns i testfile.py
def styrning_optimerad():
    return 5.5 * np.pi / 180

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
        # theta = styrning(x,y)
        theta = styrning_optimerad()


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

#Runge-Kutta 3 - lösare
def solver(f, t0, y0, dt):
    interval = round((t0[1]-t0[0])/dt)
    tvec = np.linspace(t0[0], t0[1], interval+1)

    yder = np.zeros((len(y0), len(tvec)))

    i = 0

    yder[:,i] = y0

    for t in tvec[0:len(tvec)-1]:
        k1 = f(t, yder[:,i])
        k2 = f(t + dt/2, yder[:,i] + (dt/2)*k1)
        k3 = f(t + dt, yder[:,i] - dt*k1 + 2*dt*k2)
        k =  (k1 + 4*k2 + k3)/6
        yder[:,i + 1] = yder[:,i] + dt*k
        i+=1

    return tvec, yder

#Funktion som solve_ivp använder för att stoppa beräkningen vid en viss händelse. 
# I vårt fall är händelsen att raketen är inom 1 l.e. från målet
def stoppa(t, Y):
    x = Y[0]
    y = Y[1]

    avstand = np.sqrt((x - target_x)**2 + (y - target_y)**2)

    return avstand - 1 #skapar en toleransradie på 1 l.e. från målet 


stoppa.terminal = True
stoppa.direction = -1

y0 = np.array([0, 0, 0, 0])

t_span = [0, 10]

#With own solver
# t, y = solver(raketbana, t_span, y0, 0.01)
# plt.plot(y[0], y[1],'m')
# plt.plot(target_x, target_y, marker='*', markersize=15, color = 'orange')
# plt.plot(y[0][-1], y[1][-1], marker='^', markersize=8, color = 'm')
# plt.show()

# With solve_ivp
sol = solve_ivp(raketbana, t_span, y0, events=stoppa, max_step = 0.05)
plt.plot(target_x, target_y, marker='*', markersize=15, color = 'orange')
plt.plot(sol.y[0], sol.y[1], 'm')
if sol.status == 1: #Om solve_ivp-event har hittats 
    hit = sol.y_events[0][0]   # tillståndet [x, y, vx, vy] exakt när eventet utlöstes
    plt.plot(hit[0], hit[1], marker='^', markersize=8, color='m')
else:
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