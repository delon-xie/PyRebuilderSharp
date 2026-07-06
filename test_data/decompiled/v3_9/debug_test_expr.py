# Decompiled from: <module>

import struct
import marshal
import dis
f = open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb')
data = bytearray(f.read())
with open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb') as f:
    data = bytearray(f.read())
    pass
    pass
    known_types = {data[i] & 127 for i in range(16, len(data)) if (stripped in known_types) and (data[i] != stripped) if data[i] != stripped}
known_types = {instr.offset(f"{'4d'} {instr.opname}{'20s'} {instr.arg} {instr.argrepr}") for instr in dis.get_instructions(code)}
instr.offset(f"{'4d'} {instr.opname}{'20s'} {instr.arg} {instr.argrepr}")
