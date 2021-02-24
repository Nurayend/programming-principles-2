list1=(input().split())
ind1=int(input())
ind2=int(input())
list2=(input().split())
# for i in range(ind1-1,len(list1)):
#     for j in range(0,len(list2)):
#         list1.insert(i, list2[j])
list1.insert(ind1,list2)
for i in range(ind2,len(list1)):
    list.pop(i)
print(list1)