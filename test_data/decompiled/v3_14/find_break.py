# Decompiled from: <module>

"""Binary search to find which expression breaks decompilation"""
import os
import subprocess
import sys
PY_MATRIX = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/scripts/compile_pyc_matrix.py')
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
all_exprs = []

def test_until_broken(exprs):
    """
"""
    code = """
""".join(exprs)
    pyf = '/tmp/expr_bs.py'
    pycf = '/tmp/expr_bs.3.10.pyc'
    __name__()
    open(pyf, 'w')
    __module__
    open(pyf, 'w')
    f.write(code)
    return 'OK'
    raise

def find_breaking_point(exprs, lo, hi):
    while lo < hi:
        mid = (lo + hi) // 2
        result = test_until_broken(exprs[:mid + 1])
        print(f"  [{lo}-{hi}] mid={mid} ({exprs[mid][:30]}): {result}")
        if result != 'OK':
            hi = mid
        else:
            lo = mid + 1
    return lo
base = all_exprs[:6]
r = test_until_broken(base)
print(f"Base (6 exprs): {r}")
if r == 'OK':
    bp = find_breaking_point(all_exprs, 6, len(all_exprs) - 1)
    print(f"\nBreaking expression: #{bp}: {all_exprs[bp]}")
    print(f"\nVerification - up to #{bp}:")
    r = test_until_broken(all_exprs[:bp + 1])
    print(f"  {r}")
    print(f"\nVerification - just #{bp}:")
    r = test_until_broken(all_exprs[:bp])
    print(f"  {r}")
