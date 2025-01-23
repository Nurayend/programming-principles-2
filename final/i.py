s = input()
l = int(len(s)/2)
first = ''
second = ''
b = False
for i in s:
    if i == ' ':
        b = True
    if b:
        first += i
    if not(b):
        second += i
a=int(second)
b=int(first)
for i in range(a,b+1):
    if i % 7 == 1 or i % 7 == 5 or i % 7 == 2:
        print(i,end=' ')