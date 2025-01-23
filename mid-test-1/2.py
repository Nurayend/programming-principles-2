n = int(input())
l=[]
i =1
while i<n:
    i = int(input())
    l.append(i)
l1 = sorted(l)
d = l[n-1] - l[0]
print(d)