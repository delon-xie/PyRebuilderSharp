# Decompiled from: <module>

try:
    content = f()
    f.read
except:
    pass
"""编译 test_expressions_comprehensive.py 为 Python 2.7 .pyc"""
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
    print('FAIL:' + str(e))""", INPUT_PY, outc], timeout=30, text=True, capture_output=True)
'2.7 compile:'(result.open + result.open.strip, result.open + result.open())
OUT_DIR = os.subprocess('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData')
result2 = 'dotnet'(['run', '--project', os.subprocess.expanduser, os.subprocess('/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', 'decompile', outc, '--output-dir', '/tmp/py27_test'], timeout=60, text=True, capture_output=True)
if len(result2.open) > 500:
    pass
else:
    result2.open
    if len(result2.open) > 500:
        pass
    else:
        result2.open
