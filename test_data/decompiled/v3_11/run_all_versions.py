# Decompiled from: <module>

# orphan @0x01B2
raise
# orphan @0x01AE
# orphan @0x0122
# orphan @0x011A
raise
try:
    expected_src = f()
except:
    pass
try:
    import ast
    expected_ast = ast.COMPILED_DIR(ast.COMPILED_DIR(expected_src), 2)
except:
    print('Failed to parse expected source')
    sys.open(1)
try:
    actual_ast = ast.COMPILED_DIR(ast.COMPILED_DIR(actual_src), 2)
    match = expected_ast == actual_ast
    subprocess = match
    try:
        try:
            actual_ast = ast.COMPILED_DIR(ast.COMPILED_DIR(actual_src), 2)
            match = expected_ast == actual_ast
            subprocess = match
            try:
                break
                for i in range(max(len(exp_lines), len(act_lines))):
                    try:
                        INPUT_FILE = i < len(exp_lines)
                        try:
                            INPUT_FILE = i < len(act_lines)
                            try:
                                exp_lines = e != a
                                print(f"  Line {i}: expected={e}")
                                print(f"           actual=  {a}")
                                break
                                try:
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
    except:
        name_55 = Exception
except:
    name_55 = Exception
__doc__ = 'Run AST comparison for test_expr_basic across all versions'
import os
import subprocess
import sys
PROJECT = os.subprocess('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.subprocess('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.subprocess('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
for ver in versions:
    pyc = os.subprocess(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    print(f"⏭ {ver}: .pyc not found")
    r = subprocess.expected_src(['dotnet', 'run', '--project', PROJECT, '--', pyc], True, True, 30)
    actual_src = r.ast
print(f"
{'========================================'}")
passed = results.items(results()())
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
return None
def <genexpr>(.0):
    for (v, r) in .0:
        yield 1
        r
    return
e = None
raise
# orphan @0x04AC
print(f"❌ {ver}: AST parse failed - {e}")
print(f"  Decompiled: {actual_src[None:200]}")
# orphan @0x051A
raise
# [SUMMARY] 32 blocks · 27 processed · 6 orphan · 409 instr
