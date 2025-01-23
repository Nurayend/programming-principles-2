n = int(input())
list1 = list(input().split())
list2 = sorted(set(list1))
for i in range(0,len(list2)):
    print(i+1,list2[i])
