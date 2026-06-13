"""Use Python's marshal to dump code structure.
Use marshal.load to compare with C# reader positions."""

import marshal, struct, io

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/abc.3.12.pyc', 'rb') as f:
    header = f.read(16)
    data = f.read()

# Python's marshal correctly parses all 8823 bytes
code_obj = marshal.loads(data)

# Dump the code tree
def dump_code(co, indent="", path=""):
    print(f"{indent}{path} code {co.co_name!r}: {len(co.co_code)}B bytecode, "
          f"{len(co.co_consts)} consts, {len(co.co_varnames)} vars, "
          f"flags={co.co_flags}, argcount={co.co_argcount}")
    for i, c in enumerate(co.co_consts):
        if hasattr(c, 'co_code'):  # nested code object
            dump_code(c, indent + "  ", f"consts[{i}]")
        elif isinstance(c, str) and len(c) > 80:
            print(f"{indent}  consts[{i}] = {c[:50]}... ({len(c)}B)")
        else:
            print(f"{indent}  consts[{i}] = {repr(c)[:60]}")

dump_code(code_obj)

# Count total code objects
count = [0]
def count_codes(co):
    count[0] += 1
    for c in co.co_consts:
        if hasattr(c, 'co_code'):
            count_codes(c)
count_codes(code_obj)
print(f"\nTotal nested code objects: {count[0]}")
print(f"Total marshal data: {len(data)} bytes")
