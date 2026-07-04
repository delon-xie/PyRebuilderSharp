# Decompiled from: <module>

None(None)
import struct
import marshal
import dis
open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb')
data = bytearray(f.read())
None(None)
known_types = {[33, 40, 41, 46, 60, 62, 63, 65, 70, 73, 74, 78, 82, 84, 91, 99, 102, 105, 108, 114, 115, 116, 117, 120, 122, 123, 218]}
range(16, len(data))
{}
known_types = {{print for instr in dis.get_instructions(code)} for i in range(16, len(data)) if (stripped in known_types) and (data[i] != stripped) if data[i] != stripped}
code = marshal.loads(bytes(data[16:]))
print('Code name:', code.co_name)
print('Names:', code.co_names)
print('Constants:', code.co_consts)
print('Varnames:', code.co_varnames)
print()
print('Instructions:')
dis.get_instructions(code)
if not True:
    pass
