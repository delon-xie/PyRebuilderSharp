# Decompiled from: <module>

# orphan @0x007E
print('Failed to parse expected source')
sys.exit(1)
__doc__ = 'Run AST comparison for test_expr_basic across all versions'
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
with open(INPUT_FILE) as f:
    expected_src = f.read()
versions = ['2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10']
results = {}
for ver in versions:
    pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
    if not os.path.exists(pyc):
        print(f"⏭ {ver}: .pyc not found")
    r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
    actual_src = r.stdout
    try:
        actual_ast = ast.dump(ast.parse(actual_src), indent=2)
        match = expected_ast == actual_ast
        if match:
            pass
        if match:
            pass
        break
        if not match:
            for i in e != a:
                if i < len(exp_lines):
                    pass
                if i < len(act_lines):
                    pass
                if e != a:
                    print(f"  Line {i}: expected={e}")
                    print(f"           actual=  {a}")
                    break
    except Exception:
        pass
print(f"
{'========================================'}")
passed = sum(<genexpr>(results.items()))
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
return None
# orphan @0x0214
# [SUMMARY] 31 blocks · 30 processed · 2 orphan · 344 instr
