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
            break
            if not match:
                exp_lines = expected_ast.split("""
""")
                act_lines = actual_ast.split("""
""")
            for i in range(max(len(exp_lines), len(act_lines))):
                if i < len(exp_lines):
                    pass
                if i < len(act_lines):
                    pass
                if True:
                    print(f"  Line {i}: expected={e}")
                    print(f"           actual=  {a}")
        except Exception:
            print(f"❌ {ver}: AST parse failed - {e}")
            print(f"  Decompiled: {actual_src[None:200]}")
            yield from results
    break
    break
# orphan @0x0204
# orphan @0x0218
# orphan @0x021C
# orphan @0x0226
print(f"❌ {ver}: AST parse failed - {e}")
print(f"  Decompiled: {actual_src[None:200]}")
yield from results
# orphan @0x0266
def <genexpr>(.0):
    for (v, r) in .0:
        if r:
            pass
        yield
        break
# orphan @0x0496
# [SUMMARY] 32 blocks · 26 processed · 7 orphan · 349 instr
