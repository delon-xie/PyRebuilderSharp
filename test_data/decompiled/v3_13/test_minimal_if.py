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
'.py'(False, 'w', ('suffix', 'delete', 'mode'))
tempfile.NamedTemporaryFile
py_path(py_path + 'c', True, ('cfile', 'doraise'))
print('Compiled OK')
r = ['dotnet', 'run', '--project', 'src/PyRebuilderSharp.Cli', py_path + 'c'](True, True, '/Users/admin/codes/Tools/PyRebuilderSharp', ('capture_output', 'text', 'cwd'))
print('=== Decompiled ===')
print(r.stdout.strip())
os.unlink(py_path)
os.unlink(py_path + 'c')
return None
raise
# [SUMMARY] 8 blocks · 9 processed · 0 orphan · 116 instr
