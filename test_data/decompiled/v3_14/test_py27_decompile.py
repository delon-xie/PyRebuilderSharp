# Decompiled from: <module>

"""编译 test_expressions_comprehensive.py 为 Python 2.7 .pyc"""
import os
import subprocess
import shutil
INPUT_PY = os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expressions_comprehensive.py')
OUTPUT_DIR = os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
BASENAME = 'test_expressions_comprehensive'
PY27 = os.path.expanduser('~/.pyenv/versions/2.7.18/bin/python')
__name__()
open(INPUT_PY)
__module__
open(INPUT_PY)
content = f.read()
None(None, None)
outc = os.path.join(OUTPUT_DIR, '{}.2.7.pyc'.format(BASENAME))
result = subprocess.run([PY27, '-c', """import py_compile, sys
src, dst = sys.argv[1], sys.argv[2]
try:
    py_compile.compile(src, cfile=dst, doraise=True)
    print('OK')
except Exception as e:
    print('FAIL:' + str(e))""", INPUT_PY, outc], timeout=30, text=True, capture_output=True)
print('2.7 compile:', result.stdout + result.stderr.strip())
OUT_DIR = os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData')
result2 = subprocess.run(['dotnet', 'run', '--project', os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', 'decompile', outc, '--output-dir', '/tmp/py27_test'], timeout=60, text=True, capture_output=True)
if len(result2.stdout) > 500:
    pass
else:
    result2.stdout
    if len(result2.stderr) > 500:
        result2.stderr[-500:]
    else:
        return result2.stderr
