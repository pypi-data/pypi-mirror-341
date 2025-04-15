def biseccion(f, a, b, tol=1e-10, max_iter=100):
    
  import numpy as np
  if f(a) * f(b) >= 0:
      raise ValueError(" f(a) and f(b) deben tener signos opuestoss")
  for _ in range(max_iter):
      c=(a+b) /2
      
      if abs ( f(c)) < tol or ( b-a) / 2 < tol:
          return c
      
      if f(a) * f(c) < 0:
          b=c
          
      else:
          a=c
          
          return (a+b) /2
      

