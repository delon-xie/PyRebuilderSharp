# Decompiled from: <module>

"""Binary search to find which expression breaks decompilation"""
import os
import subprocess
import sys
PY_MATRIX = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/scripts/compile_pyc_matrix.py')
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
all_exprs = ['a1 = None', 'a2 = True', 'a3 = False', 'a4 = 42', 'a5 = 3.14', 'a6 = \'hello\'', 'b1 = x', 'b2 = obj.attr', 'b3 = items[0]', 'b4 = items[1:10]', 'b5 = items[1:]', 'c1 = not x', 'c2 = ~x', 'c3 = -x', 'd1 = x + y', 'd2 = x - y', 'd3 = x * y', 'd4 = x / y', 'd5 = x // y', 'd6 = x % y', 'd7 = x ** y', 'e1 = x & y', 'e2 = x | y', 'e3 = x ^ y', 'e4 = x << y', 'e5 = x >> y', 'f1 = x < y', 'f2 = x > y', 'f3 = x <= y', 'f4 = x >= y', 'f5 = x == y', 'f6 = x != y', 'f7 = x is y', 'f8 = x is not y', 'f9 = x in y', 'f10 = x not in y', 'i1 = func()', 'i2 = func(x)', 'i3 = func(x, y)', 'o1 = obj.attr.sub', 'o2 = obj.method()', 'n1 = (a + b) * (c - d)', 'n2 = -x ** 2 + y / 3', 'n3 = x + y * z', 'n4 = x * y + z', 'n5 = a + b + c', 'n6 = a * b * c']
def test_until_broken(exprs):
    with open(pyf, 'w') as f:
        f.write(code)
    r2 = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
    out = r2.stdout + r2.stderr.strip()
    if 'Decompilation failed' in out:
        return 'CRASH'
    return 'NO_COMPILE'

def find_breaking_point(exprs, lo, hi):
    while lo < hi:
        mid = (lo + hi) // 2
        result = test_until_broken(exprs[None:mid + 1])
        print(f"  [{lo}-{hi}] mid={mid} ({exprs[mid][None:30]}): {result}")
        if result != 'OK':
            hi = mid
        lo = mid + 1
    return lo
base = all_exprs[None:6]
r = test_until_broken(base)
print(f"Base (6 exprs): {r}")
if r == 'OK':
    bp = find_breaking_point(all_exprs, 6, len(all_exprs) - 1)
    print(f"
Breaking expression: #{bp}: {all_exprs[bp]}")
    print(f"
Verification - up to #{bp}:")
    r = test_until_broken(all_exprs[None:bp + 1])
    print(f"  {r}")
    print(f"
Verification - just #{bp}:")
    r = test_until_broken(all_exprs[None:bp])
    print(f"  {r}")
