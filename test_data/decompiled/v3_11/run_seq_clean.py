# Decompiled from: <module>

"""Run AST comparison for test_seq_clean across all versions"""
import os
import subprocess
import ast
import sys
PROJECT = os.path('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_seq_clean.py')
os.path.expanduser
expected_src = f()
f.read
None(None)
expected_ast = ast.dump(ast.parse(expected_src), indent=2)
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
[]
passed = [None for ver in '?' if not os.path(pyc)]
passed = (None for (v, r) in .0)
total = len(results)
print("""
Passed: %d/%d (%d%%)""" % (passed, total, passed * 100 // total))
def <genexpr>(.0):
    .0
    for (v, r) in .0:
        yield 1
        r
        None
    return
