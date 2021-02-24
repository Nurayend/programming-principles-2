n = int(input())
list1 = list(input().split())
k = int(input())
listx = []
listy = []
for item in list1[0:k]:
    listx.append(item)
for item in list1[k:n]:
    listy.append(item)
x = (''.join(listx))
y = (''.join(listy))
print(int(x)*int(y))