# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    pass
try:
    expected_ast = ast.parse(expected_src)(2, ('indent',))
except Exception:
    pass
try:
    actual_ast = ast.parse(actual_src)(2, ('indent',))
    match = expected_ast == actual_ast
except Exception:
    pass
try:
    print('Failed to parse expected source:', e)
    sys.exit(1)
except:
    e = None
try:
    print(f"❌ {ver}: AST parse failed - {e}")
    print('  Decompiled: %s' % (actual_src + None))
except:
    e = None
__doc__ = 'Run AST comparison for test_seq_clean across all versions'
import os
import subprocess
import ast
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
for ver in []:
    pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: .pyc not found' % ver)
    else:
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
        actual_src = r.stdout
passed = <genexpr>(results.items()())
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
return None
if not True:
    pass
raise
def <genexpr>(.0):
    try:
        for _ in .0:
            try:
                raise
            except:
                pass
            if not True:
                pass
    except:
        pass
raise
e = None
# orphan @0x0586
raise
# orphan @0x0608
raise
# orphan @0x060C
raise
# [WARN] 3 instructions not decompiled
#   @0x0222: JUMP_BACKWARD arg=178
#   @0x041A: JUMP_BACKWARD arg=120
#   @0x0472: JUMP_BACKWARD arg=770
# [SUMMARY] 56 blocks · 54 processed · 3 orphan · 386 instr
