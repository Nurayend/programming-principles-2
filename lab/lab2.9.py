l=tuple(input().split())
def a(l):
    for i in range(0,len(l)):
        if type(i)==list or type(i)==dict or type(i)==set:
            return True
        else:
            return False
print(a(l))