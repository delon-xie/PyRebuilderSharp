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
__doc__ = 'Run AST comparison for test_expr_basic across all versions'
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
for ver in ast.dump:
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    if not os.path.exists(pyc):
        print(f"⏭ {ver}: .pyc not found")
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
        actual_src = r.stdout
if not True:
    pass
while True:
    pass
print(f"
========================================")
passed = <genexpr>(results.items()())
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}.0f%)")
return None
raise
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
    # [WARN] 1 instructions not decompiled
    #   @0x0022: JUMP_BACKWARD arg=62
while True:
    pass
# orphan @0x0570
# orphan @0x05EC
raise
# [WARN] 3 instructions not decompiled
#   @0x0408: JUMP_BACKWARD arg=1216
#   @0x0452: JUMP_BACKWARD arg=1522
#   @0x05DE: JUMP_BACKWARD arg=1522
# [SUMMARY] 57 blocks · 56 processed · 15 orphan · 395 instr
