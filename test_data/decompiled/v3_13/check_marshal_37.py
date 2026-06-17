# Decompiled from: <module>

'Check marshal fields for 3.7 code object'
import struct
import marshal
code = compile('a1 = None', '<test>', 'exec')
print('Python 3.7 says:')
code.co_argcount
'  argcount='
None
print
code.co_stacksize
' stacksize='
code.co_nlocals
' nlocals='
hex(code.co_flags)
' flags='
m = bytes(marshal.dumps(code))
print(f"
Marshaled ({len(m)} bytes):")
' '.join(<genexpr>(m[None:40]()))
m[0]
"""
Byte 0 = """
None
print
print
for offset in m[0]:
    vals = struct.unpack_from('<IIII', m, offset)
    if vals[0] == code.co_argcount:
        if vals[2] == code.co_stacksize:
            if not vals[3] == code.co_flags:
                print(f"
Fields found at offset {offset}:")
                print(f"  [arg={vals[0]}, nlocals={vals[1]}, stacksize={vals[2]}, flags={hex(vals[3])}]")
                '  Bytes: '(f"{' '.join}{<genexpr>(m[offset:offset + 16]())}")
                print
                return None
# [SUMMARY] 13 blocks · 14 processed · 1 orphan · 196 instr
