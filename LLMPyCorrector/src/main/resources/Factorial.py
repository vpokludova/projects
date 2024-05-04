def factorial(n):
    """
    Calculate the factorial of a given number.

    Parameters:
        n (int): The number whose factorial is to be calculated.

    Returns:
        int: The factorial of the input number.
    """
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

if __name__ == main:
    num = 5
    print(f"The factorial of {num} is: {factorial(num)}")
