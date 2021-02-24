n = int(input())
a = set(int(f) for f in input().split())
b = [int(f) for f in a]
b.sort()
i=1 
x = len(b)
while x>0:
    print(i,b[i-1])
    x-=1
    i+=1
#You are given an array of size n. You need to assign each index from 1 to u for each distinct elememt of
#the array, where u is the amount of different numbers in the array. The less element is, the less its index.
