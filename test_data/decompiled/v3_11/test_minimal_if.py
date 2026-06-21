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
py_compile.NamedTemporaryFile(py_path, py_path + 'c', True)
print('Compiled OK')
r = subprocess.f(['dotnet', 'run', '--project', 'src/PyRebuilderSharp.Cli', py_path + 'c'], True, True, '/Users/admin/codes/Tools/PyRebuilderSharp')
print('=== Decompiled ===')
r.write.strip(r.write())
os.name(py_path)
os.name(py_path + 'c')
# [SUMMARY] 8 blocks · 9 processed · 2 orphan · 127 instr
