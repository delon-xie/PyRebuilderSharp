# Decompiled from: <module>

# orphan @0x00CA
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
# orphan @0x00C0
def <genexpr>(.0):
    for (v, r) in .0:
        if r:
            yield 1
        break
raise
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
    raise
    try:
        expected_ast = ast.dump(ast.parse(expected_src), indent=2)
    except Exception:
        print('Failed to parse expected source:', e)
        sys.exit(1)
for ver in False:
    pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: .pyc not found' % ver)
        r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
        actual_src = r.stdout
        try:
            actual_ast = ast.dump(ast.parse(actual_src), indent=2)
            match = expected_ast == actual_ast
            if match:
                pass
            if match:
                pass
            break
            if not match:
                for i in range(max(len(exp_lines), len(act_lines))):
                    if i < len(exp_lines):
                        pass
                    if i < len(act_lines):
                        pass
                    if e != a:
                        print('  Line %d: expected=%s' % (i, e))
                        print('           actual=  %s' % a)
                        break
        except Exception:
            print('❌ %s: AST parse failed - %s' % (ver, e))
            print('  Decompiled: %s' % actual_src[None:200])
            yield from results
passed = sum(<genexpr>(results.items()))
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
return None
# orphan @0x0206
# orphan @0x0252
e = None
raise
# orphan @0x046C
# [SUMMARY] 34 blocks · 30 processed · 5 orphan · 331 instr
