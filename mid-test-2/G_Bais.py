n = int(input())
t = input()
a = set(t)
while n > 1:
    t=  input()
    a = a.intersection(t)
    n-=1
b = list(a)

if len(a)!=0: print(" ".join(sorted(b)))
else: print("NO COMMON CHARACTERS")
#You are given a list of strings A. Print all characters that appears in all strings
