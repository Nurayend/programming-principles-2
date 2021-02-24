n = int(input())
t = input()
x = len(t)
i = 0
while x>0:
    ch  = ord(t[i])+n
    if ch>90: ch-=26
    print(chr(ch),end="")
    i+=1
    x-=1
#We have a string S consisting of uppercase English letters. Additionally, an integer N will be given.
#Shift each character of S by N in alphabetical order (see below), and print the resulting string.
#We assume that A follows Z. For example, shifting A by 2 results in C (A -> B -> C), and shifting X by
#3 results in B (X -> Z -> A -> B).
    