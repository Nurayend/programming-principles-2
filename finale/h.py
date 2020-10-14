w = str(input())
l = len(w)
i = 0
l = l - 1
k = 0
while l - i >= i:
    if w[l - i] == w[i]:
        i += 1
    else:
        k = 1
        break
if k == 1:
  print("NO")
else:
  print("YES")