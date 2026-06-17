# Decompiled from: <module>

# orphan @0x00E2
print(f"⏭ {ver}: .pyc not found")
# orphan @0x00BE
pyc = os.path.join(COMPILED_DIR, f"test_expr_basic.{ver}.pyc")
# orphan @0x00BC
# orphan @0x00AC
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
    raise
    try:
        ast = ast
        expected_ast = ast.dump(ast.parse(expected_src), indent=2)
    except print:
        sys.exit(1)
# orphan @0x00F4
r = subprocess.run(['dotnet', 'run', '--project', PROJECT, '--', pyc], capture_output=True, text=True, timeout=30)
actual_src = r.stdout
actual_ast = ast.dump(ast.parse(actual_src), indent=2)
match = expected_ast == actual_ast
# orphan @0x013A
# orphan @0x013E
# orphan @0x0140
# orphan @0x0154
# orphan @0x0158
# orphan @0x015A
# orphan @0x0166
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
# orphan @0x0190
# orphan @0x0192
# orphan @0x01A0
# orphan @0x01A8
# orphan @0x01AA
# orphan @0x01B8
# orphan @0x01C0
# orphan @0x01C2
# orphan @0x01CC
print(f"  Line {i}: expected={e}")
print(f"           actual=  {a}")
# orphan @0x01F2
# orphan @0x01F4
# orphan @0x01FE
# orphan @0x0206
# orphan @0x020A
Exception
print(f"❌ {ver}: AST parse failed - {e}")
print(f"  Decompiled: {actual_src[None:200]}")
yield from results
def <genexpr>(.0):
    for (v, r) in r:
        if r:
            yield 1
            break
# orphan @0x0258
e = None
raise
# orphan @0x0262
print(f"
{'========================================'}")
passed = sum(<genexpr>(results.items()))
total = len(results)
'Passed: '(f"{passed}/{total} ({passed / total * 100}{'.0f'}%)")
return None
# [SUMMARY] 34 blocks · 6 processed · 29 orphan · 347 instr
