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

def styrning_test(alpha):
    return alpha * np.pi / 180

#Ungefär motsvarande solve_ivp-events. Funtkion som används för att se om vi är max 1 l.e. från målet.
def check_hit(x, y):
    avstand = np.sqrt((x - target_x)**2 + (y - target_y)**2)
    return avstand <= 1

def raketbana(t, Y, alpha):
    x = Y[0]
    y = Y[1]
    vx = Y[2]
    vy = Y[3]

    m = massa(t)
    m_der = massa_derivata(t)

    if y < 20:
        theta = np.pi/2
    else:
        theta = styrning_test(alpha)

    u = np.array([
        km * np.cos(theta),
        km * np.sin(theta)
    ])

    v = np.array([vx, vy])
    v_norm = np.linalg.norm(v)
    
    luft = c * v_norm * v
    
    F = m * g - luft
    a = F/m - m_der/m * u

    ax = a[0]
    ay = a[1]

    return np.array([vx, vy, ax, ay])

#Runge-Kutta 3 - lösare
def solver(f, t0, y0, dt, alpha):
    interval = round((t0[1]-t0[0])/dt)
    tvec = np.linspace(t0[0], t0[1], interval+1)

    yder = np.zeros((len(y0), len(tvec)))

    i = 0

    yder[:,i] = y0

    for t in tvec[0:len(tvec)-1]:
        k1 = f(t, yder[:,i], alpha)
        k2 = f(t + dt/2, yder[:,i] + (dt/2)*k1, alpha)
        k3 = f(t + dt, yder[:,i] - dt*k1 + 2*dt*k2, alpha)
        k =  (k1 + 4*k2 + k3)/6
        yder[:,i + 1] = yder[:,i] + dt*k

        x_nuvarande = yder[0, i]
        y_nuvarande = yder[1, i]

        #Om vi har träffat avslutar vi beräkningen
        if check_hit(x_nuvarande, y_nuvarande):
            break
        
        i+=1
    #Vi returnerar inte hela tvec om inte hela har fyllts. Detta för att indexet -1 ska avse slutpositionen oavsett vad.
    return tvec[:i+1], yder[:, :i+1]

y0 = np.array([0, 0, 0, 0])

t_span = [0, 10]
t_eval= np.linspace(0, 10, 200)

dt = 0.01

alpha = 90

#Loop för att iterera över alpha fr o m 90 grader och hitta den (första) optimala vinkeln för att träffa målet. 
while alpha >= 0:
    t, y = solver(raketbana, t_span, y0, dt, alpha)
    
    x_slut = y[0, -1]
    y_slut = y[1, -1]

    if check_hit(x_slut, y_slut):
        break

    alpha -= 0.5

if alpha > -0.5:
    print(f"{alpha} är den rätta bästa vinkeln!!!")
    
    t, y = solver(raketbana, t_span, y0, dt, alpha)
    plt.plot(y[0], y[1],'m')
    plt.plot(target_x, target_y, marker='*', markersize=15, color = 'orange')
    plt.plot(y[0][-1], y[1][-1], marker='^', markersize=8, color = 'm')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
else:
    print("Ingen träff!")
