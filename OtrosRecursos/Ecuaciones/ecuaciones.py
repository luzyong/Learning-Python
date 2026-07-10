import matplotlib.pyplot as plt

def runge_kutta(y, x, dx, f):
    k1 = dx * f(y, t)
    k2 = dx * f(y + 0.5 * k1, x + 0.5 * dx)
    k3 = dx * f(y + 0.5 * k2, x + 0.5 * dx)
    k4 = dx * f(y + k3, x + dx)
    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6.


t = 0. #x inicial
y = 1. #y inicial
dt = .1 # intervalo
ys, ts = [], []

def func(y, t):
    #return t * math.sqrt(y) #aquí se especifica la ecuación a resolver
    return 2*t*y

while t <= 10:
    y = runge_kutta(y, t, dt, func)
    t += dt
    ys.append(y)
    ts.append(t)

plt.plot(ts, ys)
plt.show()
for x,y in zip(ts,ys):
    print(f'X:{x} Y:{y}')

