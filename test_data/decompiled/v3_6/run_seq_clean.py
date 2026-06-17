# Decompiled from: <module>

# orphan @0x00A8
def <genexpr>(.0):
    for (v, r) in .0:
        if r:
            pass
        yield
        break
# orphan @0x0086
print('Failed to parse expected source:', e)
sys.exit(1)
# orphan @0x007E
__doc__ = 'Run AST comparison for test_seq_clean across all versions'
import os
import subprocess
import ast
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
with open(INPUT_FILE) as f:
    expected_src = f.read()
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
for ver in match:
    pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: .pyc not found' % ver)
        r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
        actual_src = r.stdout
        try:
            match = expected_ast == actual_ast
            if match:
                pass
            break
            if match:
                pass
            break
            if not match:
                exp_lines = expected_ast.split("""
""")
                act_lines = actual_ast.split("""
""")
            for i in range(max(len(exp_lines), len(act_lines))):
                if i < len(exp_lines):
                    pass
                if i < len(act_lines):
                    pass
                if e != a:
                    print('  Line %d: expected=%s' % (i, e))
                break
        except Exception:
            print('❌ %s: AST parse failed - %s' % (ver, e))
            print('  Decompiled: %s' % actual_src[None:200])
            yield from results
    break
passed = sum(<genexpr>(results.items()))
total = len(results)
# orphan @0x0208
yield from results
# orphan @0x0216
# orphan @0x0220
print('❌ %s: AST parse failed - %s' % (ver, e))
print('  Decompiled: %s' % actual_src[None:200])
yield from results
# orphan @0x025A
e = None
# [SUMMARY] 34 blocks · 28 processed · 8 orphan · 328 instr
