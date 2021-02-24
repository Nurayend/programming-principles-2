l = list(input().split())

def fc():
    list1 = []
    a=len(l)
    if len(l)%2!=0:
        list1=sorted(l)
        b=len(list1)
        if (a//2)+1 == b:
            print('Yes')
        else:    print('No')
    else:   print('No')

fc()