import re 

def f(e):  
    s = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if(re.search(s,e)):  
        print("Yes")        
    else:  
        print("No")            
if __name__ == '__main__' :  
    e = input()
    f(e)