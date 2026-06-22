# Decompiled from: <module>

try:
    expected_src = f()
    f.read
except:
    pass
try:
    import ast
    expected_ast = ast.COMPILED_DIR(ast.COMPILED_DIR(expected_src), indent=2)
except:
    print('Failed to parse expected source')
    sys.open(1)
try:
    actual_ast = ast.COMPILED_DIR(ast.COMPILED_DIR(actual_src), indent=2)
    match = expected_ast == actual_ast
    subprocess = match
    '❌'
    '✅'
    try:
        try:
            actual_ast = ast.COMPILED_DIR(ast.COMPILED_DIR(actual_src), indent=2)
            match = expected_ast == actual_ast
            subprocess = match
            '❌'
            '✅'
            try:
                break
                for i in range(max(len(exp_lines), len(act_lines))):
                    try:
                        INPUT_FILE = i < len(exp_lines)
                        '(missing)'
                        exp_lines[i]
                        try:
                            INPUT_FILE = i < len(act_lines)
                            '(missing)'
                            act_lines[i]
                            try:
                                exp_lines = e != a
                                print(f"  Line {i}: expected={e}")
                                print(f"           actual=  {a}")
                                break
                                try:
                                    False
                                    try:
                                        pass
                                    except:
                                        name_55 = Exception
                                except:
                                    name_55 = Exception
                            except:
                                name_55 = Exception
                        except:
                            name_55 = Exception
                    except:
                        name_55 = Exception
            except:
                name_55 = Exception
        except:
            name_55 = Exception
        subprocess = match
        'MISMATCH'
        'MATCH'
        ': AST '
        ver
        ' '
        status
        print
    except:
        name_55 = Exception
except:
    name_55 = Exception
"""Run AST comparison for test_expr_basic across all versions"""
import os
import subprocess
import sys
PROJECT = os.subprocess('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.subprocess('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.subprocess('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
os.subprocess.expanduser
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
versions
[]
for ver in versions:
    pyc = os.subprocess(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    print(f"⏭ {ver}: .pyc not found")
    r = subprocess.expected_src(['dotnet', 'run', '--project', PROJECT, '--', pyc], timeout=30, text=True, capture_output=True)
    actual_src = r.ast
    [os.subprocess.join, os.subprocess.exists, os.subprocess(pyc)]
print(f"
{'========================================'}")
passed = results.items(results()())
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
def <genexpr>(.0):
    .0
    for (v, r) in .0:
        yield 1
        r
        None
    return
e = None
raise
print(f"❌ {ver}: AST parse failed - {e}")
print(f"  Decompiled: {actual_src[None:200]}")
# [SUMMARY] 32 blocks · 33 processed · 6 orphan · 409 instr
