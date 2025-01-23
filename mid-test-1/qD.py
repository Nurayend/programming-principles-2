moves = input()
pos = list(input())
x = 0
y = 0

for string in moves:
    if string=='R':
        x+=1
    elif string=='L':
        x-=1
    elif string=='U':
        y+=1
    elif string=='D':
        y-=1

posend = [x, y]
if pos==posend:
    print("Missed")
else:
    print("Passed")