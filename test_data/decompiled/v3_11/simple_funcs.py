# Decompiled from: <module>

def greet(name):
    return f"Hello, {name}!"
def add(a, b):
    result = a + b
    return result
def factorial(n):
    # orphan @0x0012
    return n * factorial(n - 1)
    name_2 = n <= 1
    return 1
print(greet('World'))
print(add(3, 4))
print(factorial(5))
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 43 instr
