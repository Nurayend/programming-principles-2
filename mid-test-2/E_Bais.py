n = int(input())
goroda = dict()
while n > 0:
    g = input().split()
    zn = g[0]
    x = int(g[1])
    for f in g[2:]:
        goroda[f]=zn
    n-=1
a = int(input())
res = []
while a >0:
    h = input()
    if h in goroda:
        res.append(goroda[h])
    else: res.append("Unknown")
    a-=1
for f in res:
    print(f)