a= [f for f in input().split()]
m = -1000
i=0
for f in a:
    if len(f)>m:
        m = len(f)
        i = a.index(f)
print(a[i])
print(len(a[i]))