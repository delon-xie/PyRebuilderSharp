# Decompiled from: <module>

'Binary search to find which expression breaks decompilation'
import os
import subprocess
import sys
PY_MATRIX = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/scripts/compile_pyc_matrix.py')
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
all_exprs = 'n6 = a * b * c'
def test_until_broken(exprs):
    """
"""
    try:
        f.write(code)
    except:
        return 'OK'
    code = """
""".join(exprs)
    pyf = '/tmp/expr_bs.py'
    pycf = '/tmp/expr_bs.3.10.pyc'
    r = ['python3', '/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/scripts/compile_pyc_matrix.py', pyf, '/tmp/expr_compiled2'](True, True, 30, ('capture_output', 'text', 'timeout'))
    pyc = '/tmp/expr_compiled2/expr_bs.3.10.pyc'
    if not stderr.path.exists(pyc):
        pass
    return
    r2 = ['dotnet', 'run', '--project', name_16, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
    out = r2.stdout + r2.stderr.strip()
    return
    return
    raise
def find_breaking_point(exprs, lo, hi):
    while True:
        return lo
    result = test_until_broken(exprs[None:mid + 1])
    if result != 'OK':
        hi = mid
    else:
        lo = mid + 1
    # [WARN] 2 instructions not decompiled
    #   @0x00B6: JUMP_BACKWARD arg=184
    #   @0x00CC: JUMP_BACKWARD arg=206
base = all_exprs[:6]
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
return
# [SUMMARY] 4 blocks · 4 processed · 1 orphan · 232 instr
