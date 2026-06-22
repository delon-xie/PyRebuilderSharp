# Decompiled from: <module>

try:
    f.write(src)
    py_path = f.name
except:
    pass
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
py_compile.compile(py_path, doraise=True, cfile=py_path + 'c')
print('Compiled OK')
r = subprocess.run(['dotnet', 'run', '--project', 'src/PyRebuilderSharp.Cli', py_path + 'c'], cwd='/Users/admin/codes/Tools/PyRebuilderSharp', text=True, capture_output=True)
print('=== Decompiled ===')
print(r.stdout.strip())
os.unlink(py_path)
os.unlink(py_path + 'c')
# [SUMMARY] 9 blocks · 9 processed · 1 orphan · 115 instr
