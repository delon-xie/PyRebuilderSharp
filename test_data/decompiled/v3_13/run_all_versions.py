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
    try:
        try:
            actual_ast = ast.parse(actual_src)(2, ('indent',))
            match = expected_ast == actual_ast
            try:
                break
                for i in match:
                    try:
                        try:
                            e = '(missing)'
                            try:
                                a = '(missing)'
                            except Exception:
                                pass
                        except Exception:
                            pass
                    except Exception:
                        pass
                    if not True:
                        pass
                    try:
                        print(f"❌ {ver}: AST parse failed - {e}")
                        try:
                            try:
                                break
                            except:
                                e = None
                        except:
                            e = None
                    except:
                        e = None
                    e = None
                if Exception:
                    pass
            except Exception:
                pass
        except Exception:
            pass
        status = '❌'
    except Exception:
        pass
except Exception:
    pass
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
# orphan @0x051A
# orphan @0x0582
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
    #   @0x0022: JUMP_BACKWARD arg=60
raise
# orphan @0x058C
raise
# [WARN] 3 instructions not decompiled
#   @0x03C8: JUMP_BACKWARD arg=1094
#   @0x0412: JUMP_BACKWARD arg=1426
#   @0x057E: JUMP_BACKWARD arg=1426
# [SUMMARY] 54 blocks · 52 processed · 13 orphan · 380 instr
