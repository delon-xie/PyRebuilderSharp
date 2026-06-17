# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    pass
try:
    actual_ast = ast.parse(r.stdout)(2, ('indent',))
    ok = expected_ast == actual_ast
except Exception:
    pass
try:
    print(f"❌ {ver}: parse error: {ex}")
    try:
        try:
            print(f"❌ {ver}: parse error: {ex}")
        except:
            ex = None
        break
    except:
        ex = None
except:
    ex = None
__doc__ = 'Run AST comparison for test_control_flow across all versions'
import os
import subprocess
import ast
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
while __name__:
    pass
for ver in __name__():
    pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: no pyc' % ver)
    r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
if not True:
    pass
return None
break
raise
ex = None
# orphan @0x0472
raise
# [WARN] 6 instructions not decompiled
#   @0x0214: JUMP_BACKWARD arg=0
#   @0x037E: JUMP_BACKWARD arg=732
#   @0x03A8: JUMP_BACKWARD arg=0
#   @0x03B2: JUMP_BACKWARD arg=0
#   @0x03B8: JUMP_BACKWARD arg=0
#   @0x0464: JUMP_BACKWARD arg=0
# [SUMMARY] 46 blocks · 46 processed · 12 orphan · 256 instr
