import dis
import sys

print(f"Python version: {sys.version}")

def outer(x):
    def inner():
        nonlocal x
        x = 2
        return x
    return inner

print("\n=== outer function ===")
dis.dis(outer, show_caches=True)

print("\n=== outer co_varnames:", outer.__code__.co_varnames)
print("=== outer co_cellvars:", outer.__code__.co_cellvars)
print("=== outer co_freevars:", outer.__code__.co_freevars)

# 测试 localsplus 布局
def test_localsplus(a, b):
    c = 1
    def inner():
        nonlocal c
        d = 2
        return c + d
    return inner

print("\n=== test_localsplus ===")
dis.dis(test_localsplus, show_caches=True)
print("\n=== test_localsplus co_varnames:", test_localsplus.__code__.co_varnames)
print("=== test_localsplus co_cellvars:", test_localsplus.__code__.co_cellvars)
print("=== test_localsplus co_freevars:", test_localsplus.__code__.co_freevars)
