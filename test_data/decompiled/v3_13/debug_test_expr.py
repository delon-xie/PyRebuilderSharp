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
break
for instr in '  ':
    instr.offset(f"4d {instr.opname}20s {instr.arg} {instr.argrepr}")
break
break
raise
# [SUMMARY] 17 blocks · 18 processed · 0 orphan · 169 instr
