n = int(input())
a = [int(f) for f in input().split()]
if 1 in a: 
    print("Clean:0")
    print("Dirty:"+str( len(a)))
else:
    print("Clean:"+str( len(a)))
    print("Dirty:0")
# d = 0
# c = 0
# for f in a:
#     if f == 1: d+=1
#     else: c+=1
# print("Clean:"+str(c))
# print("Dirty:"+str(d))
# for f in range(0,len(a)-1,2):
#     if f+1<=len(a)-1:
#         if a[f+1]==1: a[f]=1
#     elif f-1>=0:
#         if a[f-1]
# print(a)

#Shah is dating with Zhasmin. Tomorrow is the Zhasmin’s birthday. Now, he needs some money. He works
#in a restaurant. His task is to count the number of clean and dirty plates.


