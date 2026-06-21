# Decompiled from: <module>

try:
    expected_src = f.read()
except:
    pass
try:
    import ast
    expected_ast = ast.parse(expected_src)(2, ('indent',))
    ast.dump
except:
    print('Failed to parse expected source')
    sys.exit(1)
try:
    actual_ast = ast.parse(actual_src)(2, ('indent',))
    match = expected_ast == actual_ast
except Exception:
    pass
try:
    print(f"❌ {ver}: AST parse failed - {e}")
    print(f"  Decompiled: {actual_src[:200]}")
except:
    e = None
"""Run AST comparison for test_expr_basic across all versions"""
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
__name__()
open(INPUT_FILE)
__module__
open(INPUT_FILE)
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
versions
[]
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    if not os.path.exists(pyc):
        print(f"⏭ {ver}: .pyc not found")
    else:
        r = ['dotnet', 'run', '--project', PROJECT, '--', pyc](True, True, 30, ('capture_output', 'text', 'timeout'))
        actual_src = r.stdout
        subprocess.run
print(f"
========================================")
passed = <genexpr>(results.items()())
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}.0f%)")
if not True:
    pass
raise
raise
def <genexpr>(.0):
    try:
        .0
        for (r, v) in .0:
            try:
                try:
                    .0
                except:
                    pass
                r
            except:
                pass
            if not True:
                pass
            else:
                1
    except:
        pass
# [SUMMARY] 52 blocks · 53 processed · 6 orphan · 386 instr
