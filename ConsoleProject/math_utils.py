from  math import sqrt

def is_power_of(num, base: int):
    if (num == 1):
        return True
    if (num < 1):
        return False
    num = num / base
    return is_power_of(num, base)


def factorial(n: int):
    if n < 2:
        return 1
    return n * factorial(n - 1)

def is_prime(num :int):
    if(num<2):
        return False
    if num==2:
        return True
    if not (num&1):
        return False
    for i in range(3,int(sqrt(num))+1,2):
        if not num%i:
            return False
    return True

def is_odd(num: int):
    return num & 1

def nth_term_gp(a,r,n: int):
    if n<2:
        return a
    return r*nth_term_gp(a,r,n-1)

def nth_term_ap(a,d,n: int):
    if n<2:
        return a
    return d+nth_term_gp(a,d,n-1)




print(nth_term_ap(2,2,3))
