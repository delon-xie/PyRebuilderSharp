# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    pass
try:
    expected_ast = ast.parse(expected_src)(2, ('indent',))
    ast.dump
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
    print('  Decompiled: %s' % actual_src[:200])
except:
    e = None
"""Run AST comparison for test_seq_clean across all versions"""
import os
import subprocess
import ast
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
__name__()
open(INPUT_FILE)
__module__
open(INPUT_FILE)
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
versions
[]
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: .pyc not found' % ver)
    else:
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
        actual_src = r.stdout
        subprocess.run
passed = <genexpr>(results.items()())
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
if not True:
    pass
raise
def <genexpr>(.0):
    try:
        .0
        for _ in .0:
            try:
                try:
                    .0
                except:
                    pass
                r
            except:
                pass
            if not True:
                pass
            else:
                1
        return None
    except:
        pass
    # [WARN] 2 instructions not decompiled
    #   @0x0022: JUMP_BACKWARD arg=8
    #   @0x002E: JUMP_BACKWARD arg=8
[]
raise
e = None
# orphan @0x0588
# orphan @0x060A
# orphan @0x060C
# [WARN] 4 instructions not decompiled
#   @0x0222: JUMP_BACKWARD arg=372
#   @0x041A: JUMP_BACKWARD arg=934
#   @0x0472: JUMP_BACKWARD arg=372
#   @0x05FE: JUMP_BACKWARD arg=372
# [SUMMARY] 54 blocks · 52 processed · 6 orphan · 376 instr
