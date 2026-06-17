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
    try:
        try:
            try:
                break
            except:
                e = None
        except:
            e = None
    except:
        e = None
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
for _ in ast.dump:
    while True:
        pass
pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
if not os.path.exists(pyc):
    print('⏭ %s: .pyc not found' % ver)
r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
actual_src = r.stdout
if not True:
    pass
passed = <genexpr>(results.items()())
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
return None
raise
def <genexpr>(.0):
    try:
        try:
            for _ in .0:
                pass
            raise
        except:
            pass
    except:
        pass
    if not True:
        pass
    # [WARN] 2 instructions not decompiled
    #   @0x0022: JUMP_BACKWARD arg=0
    #   @0x002E: JUMP_BACKWARD arg=0
raise
e = None
# orphan @0x060C
raise
# [WARN] 4 instructions not decompiled
#   @0x0222: JUMP_BACKWARD arg=0
#   @0x041A: JUMP_BACKWARD arg=676
#   @0x0472: JUMP_BACKWARD arg=0
#   @0x05FE: JUMP_BACKWARD arg=0
# [SUMMARY] 58 blocks · 58 processed · 15 orphan · 376 instr
