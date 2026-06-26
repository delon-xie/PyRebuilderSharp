# Decompiled from: <module>

import py_compile
import tempfile
import os
import subprocess
src = """
def test_simple():
    x = 0
    if True:
        x = 1
    else:
        x = 2
    return x
"""
tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w')
None(None)
py_compile.compile(py_path, cfile=py_path + 'c', doraise=True)
print('Compiled OK')
r = subprocess.run(['dotnet', 'run', '--project', 'src/PyRebuilderSharp.Cli', py_path + 'c'], capture_output=True, text=True, cwd='/Users/admin/codes/Tools/PyRebuilderSharp')
print('=== Decompiled ===')
print(r.stdout.strip())
os.unlink(py_path)
os.unlink(py_path + 'c')
