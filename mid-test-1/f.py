nk = list(input().split())
n = nk[0]
k = nk[1]
a = list(input().split())
i =0
j =len(a)-1
cnt = 0
while i==j:
    s = a[i]+a[j]
    if s == k:
        cnt+=1
    i+=1
    j-=1
if cnt>0:
    print("Bon Appetit")
else:
    print("So sad")
