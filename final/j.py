from collections import Counter  
s = input() 
l = [x for x in s.lower() if x.isalpha()] 
c = Counter(l) 
o = sum(1 for a, cnt in c.items() if cnt%2)
if (o <= 1): 
    print("ZA WARUDO TOKI WO TOMARE") 
else: 
    print("JOJO")