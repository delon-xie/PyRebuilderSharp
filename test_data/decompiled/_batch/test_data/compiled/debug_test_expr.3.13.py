# Decompiled from: <module>

import struct
import marshal
import dis
open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb')
data = bytearray(f.read())
None(None)
known_types = {[33, 40, 41, 46, 60, 62, 63, 65, 70, 73, 74, 78, 82, 84, 91, 99, 102, 105, 108, 114, 115, 116, 117, 120, 122, 123, 218]}
range(16, len(data))
{}
code = {data[i] & 127 for i in range(16, len(data)) if not stripped in known_types if data[i] != stripped}
if not bytearray:
    pass
raise
instr = {instr.offset(f"4d {instr.opname}20s {instr.arg} {instr.argrepr}") for instr in dis.get_instructions(code)}
