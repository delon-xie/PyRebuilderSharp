# Decompiled from: <module>

import struct
import marshal
import dis
with open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb') as f:
    data = bytearray(f.read())
    raise
    known_types = [33, 40, 41, 46, 60, 62, 63, 65, 70, 73, 74, 78, 82, 84, 218, 91, 99, 102, 105, 108, 114, 115, 116, 117, 120, 122, 123]
if True:
    pass
break
for instr in dis.get_instructions(code):
    pass
# orphan @0x0064
# orphan @0x0066
stripped = data[i] & 127
# orphan @0x007C
# orphan @0x0092
code = marshal.loads(bytes(data[16:]))
print('Code name:', code.co_name)
print('Names:', code.co_names)
print('Constants:', code.co_consts)
print('Varnames:', code.co_varnames)
print()
print('Instructions:')
# [SUMMARY] 14 blocks · 11 processed · 4 orphan · 147 instr
