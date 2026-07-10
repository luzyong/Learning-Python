#from pylab import *		# para graficas
import matplotlib.pyplot as pl
def rk4_completo(x0, t_final, h, f):
	lista_t  = []
	lista_x = []
	
	x = x0
	t = 0.
	
	while t < t_final+h:		# para incluir t_final
		lista_t.append(t)
		lista_x.append(x)
		
		k1 = f(x,t)
		k2 = f(x + 0.5*h*k1, t+0.5*h)
		k3 = f(x + 0.5*h*k2, t+0.5*h)
		k4 = f(x + h*k3, t+h)
		
		x += h/6. * (k1 + 2.*k2 + 2.*k3 + k4)
		t += h
		
	return lista_t, lista_x
	
def rk4(x, t, h, f):
	k1 = f(x,t)
	k2 = f(x + 0.5*h*k1, t+0.5*h)
	k3 = f(x + 0.5*h*k2, t+0.5*h)
	k4 = f(x + h*k3, t+h)
		
	return (k1 + 2.*k2 + 2.*k3 + k4) / 6.
	

def integrar_1er_orden(x0, t_final, h, f, metodo):		
	# metodo es el metodo que utilizar, que estima la derivada
	lista_t  = []
	lista_x = []
	
	x = x0
	t = 0.
	
	while t < t_final+h:		# para incluir t_final
		lista_t.append(t)
		lista_x.append(x)
	
		derivada = metodo(x, t, h, f)
		
		x += h * derivada
		t += h
	
	return lista_t, lista_x

	
	
	

def logistica(x,t):
	return x*(5. - x)
	


dt = 0.2
t_final = 5
x0 = 0.1


t, x = rk4_completo(x0, t_final, dt, logistica)		
pl.plot(t,x)
pl.show()


