import re
t = input()
pat1 = r"[A-Z]+"
pat2 = r"[a-z]+"
pat3= r"_+"
pat4 = r"\d+"
x1 = re.search(pat1,t)
x2 = re.search(pat2,t)
x3 = re.search(pat3,t)
x4 = re.search(pat4,t)
if x1!=None and x2!=None and x3!=None and x4!=None: print("Found a match!")
else: print("Not matched!")

# pattern=r'[A-Za-z0-9_]+'
# r=re.search(pattern,s)
#Write a program to match a string that contains 
#only upper and lowercase letters, numbers, and underscores.