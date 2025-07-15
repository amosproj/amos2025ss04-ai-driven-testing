"""Simple command-line calculator application."""


def calculate_result(a, b, op):
    """Calculate result of two numbers with given operator.

    Args:
        a: First number
        b: Second number
        op: Operator (+, -, *, /)

    Returns:
        The calculated result

    Raises:
        ValueError: If operator is invalid
    """
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    else:
        raise ValueError(f"Invalid operator: {op}")


def calculator():
    """Run an interactive command-line calculator.

    Prompts the user to input two numbers and an operation (+, -, *, /)
    then computes and displays the result. Handles special cases such as
    division by zero and invalid operators.

    Returns:
        None
    """
    print("Simple Calculator")
    a = float(input("Enter first number: "))
    op = input("Enter operator (+, -, *, /): ")
    b = float(input("Enter second number: "))

    try:
        result = calculate_result(a, b, op)
        print("Result:", result)
    except ValueError as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    calculator()
