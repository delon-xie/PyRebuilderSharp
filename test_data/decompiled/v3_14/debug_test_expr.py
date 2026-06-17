# Decompiled from: <module>

try:
    data = bytearray(f.read())
except:
    pass
import struct
import marshal
import dis
for i in __name__():
    stripped = data[i] & 127
    if (stripped in known_types) or not data[i] != stripped:
        break
for _ in None:
    pass
raise
# [SUMMARY] 20 blocks · 21 processed · 5 orphan · 178 instr
