import re
s = input()
s1 = "KBTU best"
s2 = "kbtu best"
match = re.search(s1, s)
match1= re.search(s2,s)
if match or match1:
    print("Found a match!")
else:
    print("Not matched!")