# Decompiled from: <module>

# orphan @0x0000
__doc__ = 'Check marshal fields for 3.7 code object'
import struct
import marshal
code = compile('a1 = None', '<test>', 'exec')
print('Python 3.7 says:')
print(f"  argcount={code.co_argcount} nlocals={code.co_nlocals} stacksize={code.co_stacksize} flags={hex(code.co_flags)}")
m = bytes(marshal.dumps(code))
print(f"
Marshaled ({len(m)} bytes):")
' '.join(<genexpr>(m[:40]()))
"""
Byte 0 = """(f"{m[0]}02x")
# orphan @0x0198
vals = struct.unpack_from('<IIII', m, offset)
# orphan @0x01F0
# orphan @0x0224
# orphan @0x0258
print(f"
Fields found at offset {offset}:")
print(f"  [arg={vals[0]}, nlocals={vals[1]}, stacksize={vals[2]}, flags={hex(vals[3])}]")
'  Bytes: '(f"{' '.join}{<genexpr>(m[offset:offset + 16]())}")
return None
# [SUMMARY] 13 blocks · 9 processed · 12 orphan · 199 instr
