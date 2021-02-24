n = int(input())
a = [int(f) for f in input().split()]
b = sorted(a)
t = True
x = len(a)
i=0
while x>0:
    if a[i]!=b[i]: 
        t = False
        break
    x-=1
    i+=1
 
if t: print("Interesting")
else: print("Not interesting")
#Muratbek is fond of interesting arrays. He has an array a1, a2, ..., an of n integers. Your task is to check
#whether his array is interesting or not.
#An array is called interesting if all elements of the array are sorted in non-decreasing order. Formally, for
#each pair of indexes i and j, such that 1 ≤ i < j ≤ n, following inequality holds: ai ≤ aj .