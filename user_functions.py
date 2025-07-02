def calculate_sum(numbers):
    """Calculate the sum of all numbers in a list.
    
    Args:
        numbers: List of numbers to sum
        
    Returns:
        int/float: The sum of all numbers
    """
    total = 0
    for num in numbers:
        total += num
    return total


def find_max(numbers):
    """Find the maximum value in a list of numbers.
    
    Args:
        numbers: List of numbers to find maximum from
        
    Returns:
        int/float/None: The maximum value, or None if list is empty
    """
    if not numbers:
        return None
    return max(numbers)
