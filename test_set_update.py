import dis
import sys

print(f"Python version: {sys.version}")

def test_set():
    s = set()
    s.add(1)
    return s

def test_set_update():
    s = set()
    s.update([1, 2])
    return s

print("\n=== test_set ===")
dis.dis(test_set, show_caches=True)

print("\n=== test_set_update ===")
dis.dis(test_set_update, show_caches=True)
