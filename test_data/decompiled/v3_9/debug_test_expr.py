# Decompiled from: <module>

import struct
import marshal
import dis
with open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb') as f:
    data = bytearray(f.read())
    for i in i:
        stripped = data[i] & 127
        if (stripped in known_types) and (data[i] != stripped):
            pass
# orphan @0x0092
code = marshal.loads(bytes(data[16:]))
print('Code name:', code.co_name)
print('Names:', code.co_names)
print('Constants:', code.co_consts)
print('Varnames:', code.co_varnames)
print()
print('Instructions:')
# orphan @0x00F0
# orphan @0x00F2
instr.offset(f"{'4d'} {instr.opname}{'20s'} {instr.arg} {instr.argrepr}")
# [SUMMARY] 12 blocks · 8 processed · 4 orphan · 147 instr
