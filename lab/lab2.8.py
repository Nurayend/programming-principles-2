# list=input().split()
# maxi=0
# mini=0
# mini=min(list)
# maxi=max(list)
# print(mini,maxi)
k=list(input().split())
def mm():
    a=-1000
    b=1000
    for i in range(0,len(k)):
        if int(k[i])>a:
            b=int(k[i])
        elif int(k[i])<b:
            b=int(k[i])
    print(a,b)

mm()