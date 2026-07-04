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
__name__()
tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w')
__module__
tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w')
f.write(src)
py_path = f.name
raise
