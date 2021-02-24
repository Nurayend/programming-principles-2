l=list(input().split())
b=int(input())
def f():
    for i in range(len(l)):
        if int(l[i])>b:
            print(int(l[i]))

f()

