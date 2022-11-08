from math import sqrt
def quadratic(a, b, c):
    discriminant=b * b - 4 * a * c
    if discriminant >= 0:
        root=round(sqrt(discriminant),4)
        return (-b + root) / (2 * a), (-b - root) / (2 * a)
    else:
        root = round(sqrt(-discriminant),4)
        return complex(-b/(2 * a) ,(root / (2 * a))), complex(-b/(2 * a) ,-(root / (2 * a)))


print(quadratic(4,6,4)[0].real)
print(quadratic(4,6,4)[0].imag)
