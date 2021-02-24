import re
s = input()
b = str.lower(s)
c = str.split(b)
cnt=0
for string in c:
    if re.fullmatch("almaty",string):
        cnt+=1
print(cnt)
