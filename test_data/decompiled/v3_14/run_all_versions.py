# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    pass
try:
    import ast
    expected_ast = ast.parse(expected_src)(2, ('indent',))
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
    print(f"  Decompiled: {actual_src + None}")
except:
    e = None
__doc__ = 'Run AST comparison for test_expr_basic across all versions'
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
for ver in []:
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    if not os.path.exists(pyc):
        print(f"⏭ {ver}: .pyc not found")
    else:
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
        actual_src = r.stdout
print(f"
========================================")
passed = <genexpr>(results.items()())
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}.0f%)")
return None
if not True:
    pass
raise
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
# orphan @0x0570
# orphan @0x05E8
raise
# orphan @0x05EC
raise
# [WARN] 4 instructions not decompiled
#   @0x0216: JUMP_BACKWARD arg=166
#   @0x0408: JUMP_BACKWARD arg=120
#   @0x0452: JUMP_BACKWARD arg=738
#   @0x0462: JUMP_BACKWARD arg=754
# [SUMMARY] 54 blocks · 52 processed · 4 orphan · 395 instr
