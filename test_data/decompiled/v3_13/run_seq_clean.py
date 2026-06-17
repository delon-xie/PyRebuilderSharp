# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    pass
try:
    while ast.parse(expected_src)(2, ('indent',)):
        for ver in ast.dump:
            pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
            if not os.path.exists(pyc):
                print('⏭ %s: .pyc not found' % ver)
            try:
                try:
                    print('  Line %d: expected=%s' % (i, e))
                except Exception:
                    pass
                break
            except Exception:
                pass
            r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
            actual_src = r.stdout
            break
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
        try:
            print('Failed to parse expected source:', e)
            sys.exit(1)
        except:
            e = None
    except:
        pass
except Exception:
    pass
__doc__ = 'Run AST comparison for test_seq_clean across all versions'
import os
import subprocess
import ast
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
break
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
# orphan @0x0500
e = None
raise
# orphan @0x050A
raise
# orphan @0x0510
# orphan @0x0570
e = None
raise
# orphan @0x057A
raise
# [WARN] 3 instructions not decompiled
#   @0x01FA: JUMP_BACKWARD arg=0
#   @0x0412: JUMP_BACKWARD arg=0
#   @0x056C: JUMP_BACKWARD arg=0
# [SUMMARY] 55 blocks · 51 processed · 12 orphan · 370 instr
