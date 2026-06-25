# Decompiled from: <module>

import struct
import marshal
import dis
f = open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb')
data = bytearray(f.read())
known_types = {78, 105, 108, 102, 120, 115, 122, 218, 116, 117, 65, 40, 41, 91, 123, 60, 62, 99, 114, 82, 70, 84, 46, 63, 33, 73, 74}
None
None
with open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb') as f:
    data = bytearray(f.read())
for i in None:
    stripped = data[i] & 127
    if (stripped in known_types) and (data[i] != stripped):
        pass
code = marshal.loads(bytes(data[16:]))
print('Code name:', code.co_name)
print('Names:', code.co_names)
print('Constants:', code.co_consts)
print('Varnames:', code.co_varnames)
print()
print('Instructions:')
for instr in dis.get_instructions(code):
    instr.offset(f"{'4d'} {instr.opname}{'20s'} {instr.arg} {instr.argrepr}")
