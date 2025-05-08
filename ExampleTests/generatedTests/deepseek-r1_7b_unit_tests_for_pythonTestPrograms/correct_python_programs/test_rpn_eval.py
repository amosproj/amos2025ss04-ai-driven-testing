def eval_rpn(rpn):
    stack = []
    tokens = rpn.split()
    for token in tokens:
        try:
            num = float(token)
            stack.append(num)
        except ValueError:
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                res = a + b
            elif token == "-":
                res = a - b
            elif token == "*":
                res = a * b
            elif token == "/":
                res = a / b
            else:
                raise ValueError("Unknown operator: {}".format(token))
            stack.append(res)
    return stack.pop()
