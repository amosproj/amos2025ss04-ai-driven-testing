def to_base(num, base):
    if num < 0 or base <= 1:
        raise ValueError("Base must be greater than 1")

    if num == 0:
        return "0"

    digits = []
    while num > 0:
        rem = num % base
        digits.append(str(rem))
        num = num // base

    # The digits are collected in reverse order, so we need to reverse them.
    return "".join(reversed(digits))
