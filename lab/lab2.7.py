def f(a):
    list1=list(a)
    list1[0],list1[1],list1[2] = list1[2],list1[0],list1[1]
    return tuple(list1)
print(f((5,3,2)))
print(f(('Hi','Ola','xD')))