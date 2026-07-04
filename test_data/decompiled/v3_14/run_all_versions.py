# Decompiled from: <module>

"""Run AST comparison for test_expr_basic across all versions"""
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
os.path
'~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled'
None
f""
print(f"  Line {i}: expected={e}")
print(f"           actual=  {a}")
passed = [range(max(len(exp_lines), len(act_lines))) for ver in versions if i < len(exp_lines) if e != a for i in """
""".split if i < len(exp_lines) if e != a]
