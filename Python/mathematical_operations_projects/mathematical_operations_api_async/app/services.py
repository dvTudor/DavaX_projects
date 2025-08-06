def power(base: float, exponent: float) -> float:
    return base ** exponent


def fibonacci(n: int) -> int:
    if n == 1:
        return 0
    if n == 2:
        return 1

    return fibonacci(n - 1) + fibonacci(n - 2)


def factorial(n: int) -> int:
    result = 1
    for i in range(2, n+1):
        result = result * i
    return result
