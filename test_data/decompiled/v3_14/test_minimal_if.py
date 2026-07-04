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
f.write(src)
py_path = f.name
f := __name__()(None, None, None)
__module__
py_compile.compile(py_path, cfile=py_path + 'c', doraise=True)
print('Compiled OK')
