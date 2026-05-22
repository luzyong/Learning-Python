import math

def etox(x, tolerance):
    #e**x=1+x+x**2/2!+x**3/3!+...
    etx=1+x
    n=2
    term=(x**n)/math.factorial(n)
    #print(term,n)
    while(term>tolerance):
        #print(term,n)
        etx+=term
        n+=1
        term=(x**n)/math.factorial(n)
        #print(term,n)
        #break
    return etx,n

value,terms = etox(1,0.01)

print(value,terms)