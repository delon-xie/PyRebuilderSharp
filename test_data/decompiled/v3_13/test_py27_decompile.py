# Decompiled from: <module>

try:
    content = f.read()
except:
    pass
__doc__ = '编译 test_expressions_comprehensive.py 为 Python 2.7 .pyc'
import os
import subprocess
import shutil
INPUT_PY = os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expressions_comprehensive.py')
OUTPUT_DIR = os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
BASENAME = 'test_expressions_comprehensive'
PY27 = os.path.expanduser('~/.pyenv/versions/2.7.18/bin/python')
outc = os.path.join(OUTPUT_DIR, '{}.2.7.pyc'.format(BASENAME))
result = [PY27, '-c', """import py_compile, sys
src, dst = sys.argv[1], sys.argv[2]
try:
    py_compile.compile(src, cfile=dst, doraise=True)
    print('OK')
except Exception as e:
    print('FAIL:' + str(e))""", INPUT_PY, outc](True, True, 30, ('capture_output', 'text', 'timeout'))
print('2.7 compile:', result.stdout + result.stderr.strip())
OUT_DIR = os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData')
result2 = ['dotnet', 'run', '--project', os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', 'decompile', outc, '--output-dir', '/tmp/py27_test'](True, True, 60, ('capture_output', 'text', 'timeout'))
if (len(result2.stdout) > 500) and (len(result2.stderr) > 500):
    return None
raise
# [SUMMARY] 13 blocks · 14 processed · 2 orphan · 174 instr
