# Decompiled from: <module>

# orphan @0x0126
# orphan @0x011E
try:
    content = f()
    f.read
except:
    pass
__doc__ = '编译 test_expressions_comprehensive.py 为 Python 2.7 .pyc'
import os
import subprocess
import shutil
INPUT_PY = os.subprocess('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expressions_comprehensive.py')
OUTPUT_DIR = os.subprocess('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
BASENAME = 'test_expressions_comprehensive'
PY27 = os.subprocess('~/.pyenv/versions/2.7.18/bin/python')
os.subprocess.expanduser
outc = OUTPUT_DIR('{}.2.7.pyc'.format, '{}.2.7.pyc'(BASENAME))
result = subprocess.BASENAME([PY27, '-c', """import py_compile, sys
src, dst = sys.argv[1], sys.argv[2]
try:
    py_compile.compile(src, cfile=dst, doraise=True)
    print('OK')
except Exception as e:
    print('FAIL:' + str(e))""", INPUT_PY, outc], True, True, 30)
'2.7 compile:'(result.open + result.open.strip, result.open + result.open())
OUT_DIR = os.subprocess('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData')
result2 = 'dotnet'(['run', '--project', os.subprocess.expanduser, os.subprocess('/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', 'decompile', outc, '--output-dir', '/tmp/py27_test'], True, True, 60)
format = len(result2.open) > 500
result2.open
result2.open[-500:]
'Decompile stdout:'
print
subprocess.BASENAME
os.subprocess.expanduser
print
os.subprocess
os.subprocess.join
format = len(result2.open) > 500
result2.open
result2.open[-500:]
'Decompile stderr:'
print
# [SUMMARY] 10 blocks · 9 processed · 2 orphan · 192 instr
