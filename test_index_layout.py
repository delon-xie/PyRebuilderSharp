import dis
import sys

print(f"Python version: {sys.version}")

def outer(a, b):
    c = 1
    def inner():
        nonlocal c
        c = 2
        return (a, b, c)
    return inner

print("\n=== outer function ===")
print(f"co_varnames: {outer.__code__.co_varnames}")
print(f"co_cellvars: {outer.__code__.co_cellvars}")
print(f"co_freevars: {outer.__code__.co_freevars}")
dis.dis(outer, show_caches=True)

# 查找 inner 函数的代码对象
for const in outer.__code__.co_consts:
    if hasattr(const, 'co_name') and const.co_name == 'inner':
        inner_code = const
        print("\n=== inner function ===")
        print(f"co_varnames: {inner_code.co_varnames}")
        print(f"co_cellvars: {inner_code.co_cellvars}")
        print(f"co_freevars: {inner_code.co_freevars}")
        dis.dis(inner_code, show_caches=True)
        break
