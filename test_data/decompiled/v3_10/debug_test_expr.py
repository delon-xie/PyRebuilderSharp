# Decompiled from: <module>

import struct
import marshal
import dis
f = open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb')
data = bytearray(f.read())
with open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb') as f:
    data = bytearray(f.read())
    for i in {}:
        stripped = data[i] & 127
        if (stripped in known_types) and (data[i] != stripped):
            i
            data
            stripped
instr.offset(f"{'4d'} {instr.opname}{'20s'} {instr.arg} {instr.argrepr}")
