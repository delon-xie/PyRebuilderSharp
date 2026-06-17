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
try:
    print('Failed to parse expected source:', e)
    sys.exit(1)
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
for ver in ast.dump:
    pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: .pyc not found' % ver)
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
        actual_src = r.stdout
break
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
    # [WARN] 1 instructions not decompiled
    #   @0x0022: JUMP_BACKWARD arg=60
raise
# orphan @0x0570
e = None
raise
# orphan @0x057A
raise
# [WARN] 2 instructions not decompiled
#   @0x03CA: JUMP_BACKWARD arg=1132
#   @0x056C: JUMP_BACKWARD arg=1408
# [SUMMARY] 55 blocks · 54 processed · 13 orphan · 370 instr
