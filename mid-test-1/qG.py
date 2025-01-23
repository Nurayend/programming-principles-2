import re
txt = input()
t = input()
s = input()
f = input()
cnt=0
result = re.sub(t,s,txt)
list1 = re.findall(f,result)
#возращает в виде листа все найденные слова
cnt = len(list1)
print(cnt)