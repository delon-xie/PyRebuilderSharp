# Decompiled from: <module>

def greet(name):
    """Hello, """
    return f"Hello, {name}!"

def add(a, b):
    result = a + b
    return result

def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
print(greet('World'))
print(add(3, 4))
print(factorial(5))
