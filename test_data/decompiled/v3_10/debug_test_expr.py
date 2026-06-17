# Decompiled from: <module>

import struct
import marshal
import dis
with open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb') as f:
    data = bytearray(f.read())
    raise
    for i in range(16, len(data)):
        stripped = data[i] & 127
        if (stripped in known_types) and (data[i] != stripped):
            i
            data
            stripped
# orphan @0x0092
code = marshal.loads(bytes(data[16:]))
print('Code name:', code.co_name)
print('Names:', code.co_names)
print('Constants:', code.co_consts)
print('Varnames:', code.co_varnames)
print()
print('Instructions:')
dis.get_instructions(code)
# orphan @0x00F0
# orphan @0x00F2
instr.offset(f"{'4d'} {instr.opname}{'20s'} {instr.arg} {instr.argrepr}")
'  '
print
# [SUMMARY] 13 blocks · 9 processed · 4 orphan · 147 instr
