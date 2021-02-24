list=(input().split())
ind=int(input())
for i in range(ind+1,len(list)):
    list.pop(i)
print(list)