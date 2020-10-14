m = int(input()) 
student = {} 
for num in range(m): 
    name, day = [s for s in input().split()] 
    if name not in student.keys(): 
        student['{}'.format(name)] = [int(day)] 
    else: 
        if int(day) not in student[name]: student['{}'.format(name)].append(int(day)) 
list = list(student.items()) 
list.sort(key = lambda i: i[0]) 
for i in list: 
    if len(i[1]) >= 3: 
        print(i[0], '+1') 
    else: 
        print(i[0], 'NO BONUS')