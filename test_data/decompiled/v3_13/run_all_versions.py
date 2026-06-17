# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    pass
try:
    import ast
    while ast.parse(expected_src)(2, ('indent',)):
        for ver in ast.dump:
            pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
            if not os.path.exists(pyc):
                print(f"⏭ {ver}: .pyc not found")
            try:
                try:
                    print(f"  Line {i}: expected={e}")
                    print(f"           actual=  {a}")
                except Exception:
                    pass
                break
            except Exception:
                pass
            r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
            actual_src = r.stdout
            actual_ast = ast.parse(actual_src)(2, ('indent',))
            match = expected_ast == actual_ast
            if match:
                status = '❌'
                if match:
                    break
                    if match:
                        pass
                    else:
                        exp_lines = expected_ast.split("""
""")
                        act_lines = actual_ast.split("""
""")
                    if i < len(exp_lines):
                        e = '(missing)'
                        if i < len(act_lines):
                            a = '(missing)'
            try:
                try:
                    print(f"❌ {ver}: AST parse failed - {e}")
                    try:
                        break
                    except:
                        e = None
                except:
                    e = None
            except:
                e = None
            e = None
            if not True:
                pass
    try:
        break
    except:
        pass
except:
    break
__doc__ = 'Run AST comparison for test_expr_basic across all versions'
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
print(f"
========================================")
passed = <genexpr>(results.items()())
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}.0f%)")
return None
raise
# orphan @0x051A
# orphan @0x0520
raise
# orphan @0x0526
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
    # [WARN] 2 instructions not decompiled
    #   @0x0022: JUMP_BACKWARD arg=0
    #   @0x002E: JUMP_BACKWARD arg=0
raise
# orphan @0x058C
raise
# [WARN] 4 instructions not decompiled
#   @0x01FE: JUMP_BACKWARD arg=0
#   @0x0412: JUMP_BACKWARD arg=0
#   @0x0422: JUMP_BACKWARD arg=0
#   @0x057E: JUMP_BACKWARD arg=0
# [SUMMARY] 54 blocks · 50 processed · 11 orphan · 380 instr
