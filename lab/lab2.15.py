l=list(input().split())

def evens():
    for i in range(len(l)):
        if int(l[i]) % 2 == 0:
            print(l[i])

# def primes():
#     for i in range(len(l)):
#         d = 2
#         n = int(l[i])
#         while n % d != 0:
#            d += 1
#         if d == n:
#             print(n)

#evens()
primes()