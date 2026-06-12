import ast, subprocess, os

# Check what Python 2.7 bytecode looks like for items[0]
# The .pyc for 2.7 should have different opcodes or patterns

COMPILED_DIR = os.path.expanduser("~/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled")
PROJECT = os.path.expanduser("~/codes/Tools/PyRebuilderSharp/src/PyRebuilderSharp.Cli")

pyc = os.path.join(COMPILED_DIR, "test_expr_basic.2.7.pyc")
r = subprocess.run(["dotnet", "run", "--project", PROJECT, "--", pyc], capture_output=True, text=True, timeout=30)

# Print the decompiled output around the items[0] and items[1:10] lines
lines = r.stdout.split('\n')
for i, line in enumerate(lines):
    if 'items[' in line:
        print(f"Line {i}: {line}")

# Print AST for items[0] specifically
print("\n--- ACTUAL AST ---")
actual_ast = ast.dump(ast.parse(r.stdout), indent=2)
print(actual_ast)
