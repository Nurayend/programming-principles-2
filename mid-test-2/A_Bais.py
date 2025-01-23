import re
t = input()
#tx = "sdafa234d!sadfa___sdfasdf%A235234z"
pat = r"[A-Z]+[a-z]+"
x = re.search(pat,t)
if x!=None: print("Found a match!")
else: print("Not matched!")
#Write a program to find the sequences of one upper case letter followed by lower case letters.