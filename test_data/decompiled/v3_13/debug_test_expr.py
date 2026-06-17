# Decompiled from: <module>

try:
    data = bytearray(f.read())
except:
    pass
import struct
import marshal
import dis
for i in open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb'):
    stripped = data[i] & 127
    if (stripped in known_types) or not data[i] != stripped:
        break
for instr in range(16, len(data)):
    instr.offset(f"4d {instr.opname}20s {instr.arg} {instr.argrepr}")
    '  '
    return None
break
raise
# [SUMMARY] 20 blocks · 21 processed · 5 orphan · 169 instr
