list1 = list(input())
list2 = []
for i in range(0,len(list1)):
    if i%2==0:
        list2.append(list1[i])
print(sorted(list2))