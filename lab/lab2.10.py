l=list(input().split())
l2=[]
def n(a):
    return a-1,a+1
for i in range(0,len(l)):
    a=int(l[i])
    l2.append(n(a))
print(l2)

# a=set(input().split())
# def f():
#     b=set()
#     for i in a:
#         b.add(int(i)-1)
#         b.add(int(i)+1)
#     print(b)

# f()