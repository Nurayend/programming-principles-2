n = int(input())
array = list(input())
unique = set(array)
if n==len(unique):
    print('YES')
else:
    print('NO')