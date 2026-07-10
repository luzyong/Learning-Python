import math

def etox(x, tolerance):
    #e**x=1+x+x**2/2!+x**3/3!+...
    etx=1+x
    n=2
    term=(x**n)/math.factorial(n)
    
    while(term>tolerance):
        etx+=term
        n+=1
        term=(x**n)/math.factorial(n)
        
    return etx,n
