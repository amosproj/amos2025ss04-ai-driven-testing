def gcd(a, b):
    if a == 0 and b == 0:
        return None
    a = abs(a)
    b = abs(b)
    while b != 0:
        t = b
        b = a % b
        a = t
    return a