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
    print('  Output: %s' % r.stdout[:200])
except:
    ex = None
__doc__ = 'Run AST comparison for test_control_flow across all versions'
import os
import subprocess
import ast
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_control_flow.py')
expected_ast = ast.parse(expected_src)(2, ('indent',))
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
for ver in []:
    pyc = os.path.join(COMPILED_DIR, 'test_control_flow.%s.pyc' % ver)
    if not os.path.exists(pyc):
        print('⏭ %s: no pyc' % ver)
    else:
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
return None
if not True:
    pass
raise
ex = None
# orphan @0x046E
raise
# orphan @0x0472
raise
# [WARN] 5 instructions not decompiled
#   @0x0214: JUMP_BACKWARD arg=178
#   @0x037E: JUMP_BACKWARD arg=36
#   @0x03A8: JUMP_BACKWARD arg=582
#   @0x03B2: JUMP_BACKWARD arg=592
#   @0x03B8: JUMP_BACKWARD arg=598
# [SUMMARY] 41 blocks · 40 processed · 2 orphan · 263 instr
