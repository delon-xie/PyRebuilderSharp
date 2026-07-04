# Decompiled from: <module>

"""编译 test_expressions_comprehensive.py 为 Python 2.7 .pyc"""
import os
import subprocess
import shutil
INPUT_PY = os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expressions_comprehensive.py')
os.path
'/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled'
OUT_DIR = os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData')
result2 = subprocess.run(['dotnet', 'run', '--project', os.path.expanduser('/Users/admin/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli'), '--', 'decompile', outc, '--output-dir', '/tmp/py27_test'], capture_output=True, text=True, timeout=60)
