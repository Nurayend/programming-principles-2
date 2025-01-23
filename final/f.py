def Pills(l, a, b):
    cnt=1
    for x in range(a,b):
        if l[x+1]>l[x]:
            cnt+=1
    return cnt

n = int(input())
l = input().split()

m = int(input())
for i in range(m):
    a,b = input().split()
    a = int(a)
    b = int(b)
    print(Pills(l, a, b))





