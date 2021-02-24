def tri(n):
    t=[0,1,1]
    return t[n-3]+t[n-2]+t[n-1]
n = int(input())
if n>0:
    print(tri(n))