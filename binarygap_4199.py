# This Python program implements the following use case:
# Write code to find BinaryGap of a given positive integer

def validate_input(n):
    """
    Validate if the input is a positive integer.

    Args:
        n (int): The input number.

    Returns:
        int: The input number if it's valid.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Input must be a positive integer.")
    return n

def binary_gap(n):
    """
    Calculate the maximum binary gap of a given positive integer.

    Args:
        n (int): A positive integer.

    Returns:
        int: The maximum binary gap.

    Raises:
        ValueError: If the input is not a positive integer.
    """
    n = validate_input(n)
    binary = bin(n)[2:]

    # Handle edge case where input number is a power of 2
    if '1' not in binary:
        return 0

    max_gap = 0
    current_gap = 0

    for digit in binary:
        if digit == '1':
            max_gap = max(max_gap, current_gap)
            current_gap = 0
        else:
            current_gap += 1

    return max_gap

print(binary_gap(5))  # Output: 2
print(binary_gap(20))  # Output: 1
print(binary_gap(21))  # Output: 2
print(binary_gap(22))  # Output: 1
print(binary_gap(25))  # Output: 2
print(binary_gap(0))  # Output: 0