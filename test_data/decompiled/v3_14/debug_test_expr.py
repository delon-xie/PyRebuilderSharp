# Decompiled from: <module>

import struct
import marshal
import dis
__name__()
open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb')
__module__
open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb')
None(None, None)
known_types = [33, 40, 41, 46, 60, 62, 63, 65, 70, 73, 74, 78, 82, 84, 91, 99, 102, 105, 108, 114, 115, 116, 117, 120, 122, 123, 218]
{}
i = {data[i] & 127 for i in '?' if not stripped in known_types}
code = marshal.loads(bytes(data[16:]))
print('Code name:', code.co_name)
print('Names:', code.co_names)
print('Constants:', code.co_consts)
print('Varnames:', code.co_varnames)
print()
print('Instructions:')
for instr in dis.get_instructions(code):
    instr.offset(f"4d {instr.opname}20s {instr.arg} {instr.argrepr}")
