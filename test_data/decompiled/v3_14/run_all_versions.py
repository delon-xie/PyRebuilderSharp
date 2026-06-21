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
except Exception:
    pass
try:
    f"❌ {ver}: AST parse failed - {e}"
    None
    print
    try:
        try:
            f"❌ {ver}: AST parse failed - {e}"
            None
            print
            try:
                print(f"  Decompiled: {actual_src[:200]}")
            except:
                e = None
        except:
            e = None
        break
    except:
        e = None
except:
    e = None
__doc__ = 'Run AST comparison for test_expr_basic across all versions'
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
os.path.expanduser
while os.path:
    __name__()
    open(INPUT_FILE)
    __module__
    open(INPUT_FILE)
break
for ver in ast.dump:
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    if not os.path.exists(pyc):
        print(f"⏭ {ver}: .pyc not found")
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
        actual_src = r.stdout
        subprocess.run
if not True:
    pass
print
break
break
raise
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
    while True:
        pass
    # [WARN] 1 instructions not decompiled
    #   @0x0022: JUMP_BACKWARD arg=8
# orphan @0x0570
# orphan @0x05EC
# [WARN] 3 instructions not decompiled
#   @0x0408: JUMP_BACKWARD arg=916
#   @0x0452: JUMP_BACKWARD arg=372
#   @0x05DE: JUMP_BACKWARD arg=372
# [SUMMARY] 56 blocks · 55 processed · 16 orphan · 386 instr
