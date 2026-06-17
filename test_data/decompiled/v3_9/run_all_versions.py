# Decompiled from: <module>

# orphan @0x00E8
print(f"⏭ {ver}: .pyc not found")
# orphan @0x00C4
pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
# orphan @0x00C0
# orphan @0x00B0
versions = ('2.7', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
results = {}
__doc__ = 'Run AST comparison for test_expr_basic across all versions'
import os
import subprocess
import sys
PROJECT = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli')
COMPILED_DIR = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled')
INPUT_FILE = os.path.expanduser('~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py')
with open(INPUT_FILE) as f:
    expected_src = f.read()
    try:
        ast = ast
        expected_ast = ast.dump(ast.parse(expected_src), indent=2)
    except print:
        sys.exit(1)
# orphan @0x00FA
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
actual_src = r.stdout
actual_ast = ast.dump(ast.parse(actual_src), indent=2)
match = expected_ast == actual_ast
# orphan @0x0144
# orphan @0x0148
# orphan @0x014A
# orphan @0x0160
# orphan @0x0164
# orphan @0x0166
# orphan @0x0174
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
# orphan @0x019E
# orphan @0x01A0
# orphan @0x01B0
# orphan @0x01B8
# orphan @0x01BA
# orphan @0x01CA
# orphan @0x01D2
# orphan @0x01D4
# orphan @0x01E0
print(f"  Line {i}: expected={e}")
print(f"           actual=  {a}")
# orphan @0x020C
# orphan @0x0216
# orphan @0x021E
# orphan @0x0222
Exception
print(f"❌ {ver}: AST parse failed - {e}")
print(f"  Decompiled: {actual_src[None:200]}")
yield from results
def <genexpr>(.0):
    for (v, r) in r:
        if r:
            yield 1
            break
# orphan @0x0270
e = None
# orphan @0x027C
print(f"
{'========================================'}")
passed = sum(<genexpr>(results.items()))
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
return None
# orphan @0x04A2
# [SUMMARY] 33 blocks · 5 processed · 28 orphan · 350 instr
