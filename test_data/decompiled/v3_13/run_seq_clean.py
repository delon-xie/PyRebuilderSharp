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
    try:
        try:
            actual_ast = ast.parse(actual_src)(2, ('indent',))
            match = expected_ast == actual_ast
            try:
                try:
                    break
                    for i in range(max(len(exp_lines), len(act_lines))):
                        try:
                            try:
                                e = '(missing)'
                                try:
                                    a = '(missing)'
                                    e != a
                                    act_lines[i]
                                except Exception:
                                    pass
                            except Exception:
                                pass
                        except Exception:
                            pass
                        if not True:
                            pass
                        print('  Line %d: expected=%s' % (i, e))
                        break
                        break
                        try:
                            print(f"❌ {ver}: AST parse failed - {e}")
                            actual_src[None:200]
                            '  Decompiled: %s'
                            None
                            print
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
        except Exception:
            pass
        status = '❌'
        status
        None
        print
        '✅'
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
os.path
while os:
    open(INPUT_FILE)
break
for ver in ast.dump:
    pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: .pyc not found' % ver)
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
        actual_src = r.stdout
        subprocess.run
raise
break
raise
def <genexpr>(.0):
    try:
        try:
            for _ in .0:
                pass
            raise
            r
        except:
            pass
    except:
        pass
    if not True:
        pass
    # [WARN] 1 instructions not decompiled
    #   @0x0022: JUMP_BACKWARD arg=10
[]
raise
# orphan @0x0570
e = None
# [WARN] 2 instructions not decompiled
#   @0x03CA: JUMP_BACKWARD arg=876
#   @0x056C: JUMP_BACKWARD arg=350
# [SUMMARY] 53 blocks · 53 processed · 9 orphan · 370 instr
