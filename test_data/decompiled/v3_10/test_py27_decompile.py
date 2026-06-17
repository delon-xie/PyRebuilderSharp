# Decompiled from: <module>

'编译 test_expressions_comprehensive.py 为 Python 2.7 .pyc'
import os
import subprocess
import shutil
INPUT_PY = os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expressions_comprehensive.py')
OUTPUT_DIR = os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
BASENAME = 'test_expressions_comprehensive'
PY27 = os.path.expanduser('~/.pyenv/versions/2.7.18/bin/python')
with open(INPUT_PY) as f:
    content = f.read()
    raise
    outc = os.path.join(OUTPUT_DIR, '{}.2.7.pyc'.format(BASENAME))
    result = subprocess.run([PY27, '-c', """import py_compile, sys
src, dst = sys.argv[1], sys.argv[2]
try:
    py_compile.compile(src, cfile=dst, doraise=True)
    print('OK')
except Exception as e:
    print('FAIL:' + str(e))""", INPUT_PY, outc], capture_output=True, text=True, timeout=30)
    print('2.7 compile:', result.stdout + result.stderr.strip())
    OUT_DIR = os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData')
if len(result2.stdout) > 500:
    pass
# orphan @0x0116
# orphan @0x026C
# [SUMMARY] 10 blocks · 7 processed · 4 orphan · 166 instr
