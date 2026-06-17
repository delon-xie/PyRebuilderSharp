# Decompiled from: <module>

try:
    data = bytearray(f.read())
except:
    pass
import struct
import marshal
import dis
known_types = [33, 40, 41, 46, 60, 62, 63, 65, 70, 73, 74, 78, 82, 84, 91, 99, 102, 105, 108, 114, 115, 116, 117, 120, 122, 123, 218]
for i in range(16, len(data)):
    stripped = data[i] & 127
    if not stripped in known_types:
        pass
code = marshal.loads(bytes(data[16:]))
print('Code name:', code.co_name)
print('Names:', code.co_names)
print('Constants:', code.co_consts)
print('Varnames:', code.co_varnames)
print()
print('Instructions:')
for instr in '  ':
    instr.offset(f"4d {instr.opname}20s {instr.arg} {instr.argrepr}")
return None
raise
# [SUMMARY] 18 blocks · 19 processed · 0 orphan · 178 instr
