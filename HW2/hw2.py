import numpy as np
import math
def mult(a,b,n):
    c=np.array([[0] * n for i in range(n)])
    if n<=2:
        for i in range(n):
            for j in range(n):
                c[i][j]=sum(a[i][k]*b[k][j] for k in range(n))
        return c
    
    v=n//2
    a11=a[0:v,0:v]
    a12=a[0:v,v:n]
    a21=a[v:n,0:v]
    a22=a[v:n,v:n]

    b11=b[0:v,0:v]
    b12=b[0:v,v:n]
    b21=b[v:n,0:v]
    b22=b[v:n,v:n]
    
    
    p1=mult(a11+a22,b11+b22,v)
    p2=mult(a21+a22,b11,v)
    p3=mult(a11,b12-b22,v)
    p4=mult(a22,b21-b11,v)
    p5=mult(a11+a12,b22,v)
    p6=mult(a21-a11,b11+b12,v)
    p7=mult(a12-a22,b21+b22,v)

    c11=p1+p4-p5+p7
    c12=p3+p5
    c21=p2+p4
    c22=p1-p2+p3+p6

    c[0:v,0:v]=c11
    c[0:v,v:n]=c12
    c[v:n,0:v]=c21
    c[v:n,v:n]=c22

    return c
    
n=int(input())
k=1
while k<n:
    k=k*2
    
a1=np.array([[0] * k for i in range(k)])
b1=np.array([[0] * k for i in range(k)])
a=[]
b=[]
for i in range(n):
    a.append(list(map(int, input().split())))
for i in range(n):
    b.append(list(map(int, input().split())))
a1[0:n,0:n]=np.array(a)
b1[0:n,0:n]=np.array(b)
        
c=mult(a1,b1,k)

for i in range(n):
    for j in range(n):
        print(c[i][j],end=' ' )
    print()
