l, r=[int(x) for x in input().split()]
 
def Odds(l,r): 
    while l <= r: 
        if l % 2 != 1: 
            Odds(l+1,r) 
            return 
        else: 
            print(l,end=" ") 
            return Odds(l+1,r) 
Odds(l,r)