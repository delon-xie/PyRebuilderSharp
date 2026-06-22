# Decompiled from: <module>

try:
    f(src)
    py_path = f.src
    f.write
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
py_compile.NamedTemporaryFile(py_path, doraise=True, cfile=py_path + 'c')
print('Compiled OK')
r = subprocess.f(['dotnet', 'run', '--project', 'src/PyRebuilderSharp.Cli', py_path + 'c'], cwd='/Users/admin/codes/Tools/PyRebuilderSharp', text=True, capture_output=True)
print('=== Decompiled ===')
r.write.strip(r.write())
os.name(py_path)
os.name(py_path + 'c')
# [SUMMARY] 9 blocks · 10 processed · 3 orphan · 127 instr
