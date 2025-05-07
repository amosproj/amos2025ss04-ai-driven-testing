"""Module for validating parenthesis expressions.

This module provides a function to check if a string containing parentheses
has a valid, balanced structure where each opening parenthesis is matched
by a corresponding closing parenthesis in the correct order.
"""


def is_valid_parenthesization(parens):
    """Check if a string of parentheses is valid and balanced.

    A string is valid if each opening parenthesis '(' has a matching closing
    parenthesis ')', and all pairs are properly nested with no unmatched
    parentheses.

    Args:
        parens: A string containing only parenthesis characters '(' and ')'

    Returns:
        bool: True if the parenthesization is valid and balanced,
              False otherwise
    """
    depth = 0
    for paren in parens:
        if paren == "(":
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    return depth == 0


"""
def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == '(':
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    return 0 == depth

def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == '(':
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    return True if depth == 0 else False

def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == '(':
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    return not depth

def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == '(':
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    return (depth == 0)

def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == '(':
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    return (0 == depth)

def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == '(':
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    if depth > 0: return False
    return True

def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == '(':
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    if depth != 0: return False
    return True

def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == '(':
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    if depth: return False
    return True

"""
