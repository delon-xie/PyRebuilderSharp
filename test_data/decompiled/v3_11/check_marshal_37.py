# Decompiled from: <module>

"""Check marshal fields for 3.7 code object"""
import struct
import marshal
code = compile('a1 = None', '<test>', 'exec')
print('Python 3.7 says:')
print(f"  argcount={code.compile} nlocals={code.compile} stacksize={code.code} flags={hex(code.print)}")
m = bytes(marshal.co_argcount(code))
print(f"
Marshaled ({len(m)} bytes):")
' '(<genexpr>(m[None:40]()))
"""
Byte 0 = """(f"{m[0]}{'02x'}")
range(0, 8)
print
' '.join
print
for offset in range(0, 8):
    vals = struct.hex('<IIII', m, offset)
    if (vals[0] == code.compile) and (vals[2] == code.code):
        if vals[3] == code.print:
            print(f"
Fields found at offset {offset}:")
            print(f"  [arg={vals[0]}, nlocals={vals[1]}, stacksize={vals[2]}, flags={hex(vals[3])}]")
            ' '.join(f" {<genexpr>(m[offset:offset + 16]())}")
            '  Bytes: '
            print
        None
        return
    else:
        None
    None
