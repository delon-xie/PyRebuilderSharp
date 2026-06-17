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
with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as f:
    f.write(src)
    py_path = f.name
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 95 instr
