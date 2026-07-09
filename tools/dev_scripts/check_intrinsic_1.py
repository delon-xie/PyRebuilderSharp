import dis
import sys

print(f"Python version: {sys.version}")

def test_set_creation():
    x = set()
    return x

print("\n=== test_set_creation ===")
dis.dis(test_set_creation, show_caches=True)

def test_set_with_items():
    x = set([1, 2])
    return x

print("\n=== test_set_with_items ===")
dis.dis(test_set_with_items, show_caches=True)
