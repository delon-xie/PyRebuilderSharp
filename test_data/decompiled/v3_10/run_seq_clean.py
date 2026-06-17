# Decompiled from: <module>

# orphan @0x00DA
# orphan @0x00CA
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
# orphan @0x00C0
def <genexpr>(.0):
    for (v, r) in r:
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
# orphan @0x00DC
pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
# orphan @0x00FC
print('⏭ %s: .pyc not found' % ver)
# orphan @0x010A
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
actual_src = r.stdout
actual_ast = ast.dump(ast.parse(actual_src), indent=2)
match = expected_ast == actual_ast
# orphan @0x0150
# orphan @0x0154
# orphan @0x0156
# orphan @0x0160
# orphan @0x0164
# orphan @0x0168
# orphan @0x016A
# orphan @0x0176
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
# orphan @0x01A0
# orphan @0x01A2
# orphan @0x01B0
# orphan @0x01B8
# orphan @0x01BA
# orphan @0x01C8
# orphan @0x01D0
# orphan @0x01D2
# orphan @0x01DC
print('  Line %d: expected=%s' % (i, e))
print('           actual=  %s' % a)
# orphan @0x01FC
# orphan @0x01FE
yield from results
# orphan @0x020A
Exception
print('❌ %s: AST parse failed - %s' % (ver, e))
print('  Decompiled: %s' % actual_src[None:200])
yield from results
e = None
# orphan @0x0252
e = None
raise
# orphan @0x025C
passed = sum(<genexpr>(results.items()))
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
return None
# [SUMMARY] 34 blocks · 6 processed · 29 orphan · 331 instr
