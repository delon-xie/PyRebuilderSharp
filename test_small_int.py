import dis
import sys

print(f"Python version: {sys.version}")

def test_set():
    x = set()
    x.add(1)
    return x

print("\n=== test_set 反汇编 ===")
dis.dis(test_set, show_caches=True)

def test_small_int():
    a = 0
    b = 2
    return (a, b)

print("\n=== test_small_int 反汇编 ===")
dis.dis(test_small_int, show_caches=True)
