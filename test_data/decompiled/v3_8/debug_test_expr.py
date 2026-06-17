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
code = marshal.loads(bytes(data[16:]))
print('Code name:', code.co_name)
print('Names:', code.co_names)
print('Constants:', code.co_consts)
print('Varnames:', code.co_varnames)
print()
print('Instructions:')
dis.get_instructions(code)
for instr in '  ':
    instr.offset(f"{'4d'} {instr.opname}{'20s'} {instr.arg} {instr.argrepr}")
return None
# [SUMMARY] 9 blocks · 10 processed · 0 orphan · 162 instr
