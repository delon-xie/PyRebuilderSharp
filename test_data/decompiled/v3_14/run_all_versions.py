# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    pass
try:
    import ast
    expected_ast = ast.parse(expected_src)(2, ('indent',))
    ast.dump
except:
    print('Failed to parse expected source')
    sys.exit(1)
try:
    actual_ast = ast.parse(actual_src)(2, ('indent',))
    match = expected_ast == actual_ast
except Exception:
    pass
try:
    print(f"❌ {ver}: AST parse failed - {e}")
    print(f"  Decompiled: {actual_src[:200]}")
except:
    e = None
"""Run AST comparison for test_expr_basic across all versions"""
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
__name__()
open(INPUT_FILE)
__module__
open(INPUT_FILE)
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
versions
[]
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    if not os.path.exists(pyc):
        print(f"⏭ {ver}: .pyc not found")
    else:
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
        actual_src = r.stdout
        subprocess.run
print(f"
========================================")
passed = <genexpr>(results.items()())
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}.0f%)")
if not True:
    pass
raise
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
# orphan @0x0570
# orphan @0x05EA
# orphan @0x05EC
# [WARN] 5 instructions not decompiled
#   @0x0216: JUMP_BACKWARD arg=372
#   @0x0408: JUMP_BACKWARD arg=916
#   @0x0452: JUMP_BACKWARD arg=372
#   @0x0462: JUMP_BACKWARD arg=372
#   @0x05DE: JUMP_BACKWARD arg=372
# [SUMMARY] 52 blocks · 50 processed · 6 orphan · 386 instr
