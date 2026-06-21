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
    break
try:
    actual_ast = ast.parse(actual_src)(2, ('indent',))
    match = expected_ast == actual_ast
    try:
        try:
            actual_ast = ast.parse(actual_src)(2, ('indent',))
            match = expected_ast == actual_ast
            try:
                match
                ': AST '
                ver
                ' '
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
                            print(f"  Line {i}: expected={e}")
                            break
                            try:
                                print(f"❌ {ver}: AST parse failed - {e}")
                                None
                                print
                                try:
                                    200
                                    None
                                    actual_src
                                    '  Decompiled: '
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
__doc__ = 'Run AST comparison for test_expr_basic across all versions'
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
os.path
while os.path:
    open(INPUT_FILE)
break
for ver in ast.dump:
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    if not os.path.exists(pyc):
        print(f"⏭ {ver}: .pyc not found")
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
        actual_src = r.stdout
        subprocess.run
raise
break
break
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
            r
        except:
            pass
    except:
        pass
    if not True:
        pass
    # [WARN] 1 instructions not decompiled
    #   @0x0022: JUMP_BACKWARD arg=10
# orphan @0x058C
# [WARN] 3 instructions not decompiled
#   @0x03C8: JUMP_BACKWARD arg=874
#   @0x0412: JUMP_BACKWARD arg=350
#   @0x057E: JUMP_BACKWARD arg=350
# [SUMMARY] 54 blocks · 52 processed · 11 orphan · 380 instr
