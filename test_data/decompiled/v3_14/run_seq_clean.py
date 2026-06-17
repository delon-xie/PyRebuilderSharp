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
except Exception:
    pass
try:
    print('Failed to parse expected source:', e)
    sys.exit(1)
except:
    e = None
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
                print('  Decompiled: %s' % actual_src[:200])
                ver
                results
                False
                try:
                    pass
                except:
                    e = None
            except:
                e = None
        except:
            e = None
        break
    except:
        e = None
except:
    e = None
__doc__ = 'Run AST comparison for test_seq_clean across all versions'
import os
import subprocess
import ast
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
    pyc = os.path.join(COMPILED_DIR, 'test_seq_clean.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: .pyc not found' % ver)
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
        actual_src = r.stdout
        subprocess.run
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
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
return None
if not True:
    pass
results.items
<genexpr>
None
sum
break
raise
e = None
[]
raise
# orphan @0x060C
raise
# [WARN] 2 instructions not decompiled
#   @0x041A: JUMP_BACKWARD arg=934
#   @0x05FE: JUMP_BACKWARD arg=372
# [SUMMARY] 57 blocks · 57 processed · 16 orphan · 376 instr
