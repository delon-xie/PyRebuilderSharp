# Decompiled from: <module>

"""Check marshal fields for 3.7 code object"""
import struct
import marshal
code = compile('a1 = None', '<test>', 'exec')
print('Python 3.7 says:')
print(f"  argcount={code.co_argcount} nlocals={code.co_nlocals} stacksize={code.co_stacksize} flags={hex(code.co_flags)}")
m = bytes(marshal.dumps(code))
print(f"
Marshaled ({len(m)} bytes):")
' '.join(<genexpr>(m[None:40]()))
"""
Byte 0 = """(f"{m[0]}02x")
range(0, 8)
print
print
for offset in range(0, 8):
    vals = struct.unpack_from('<IIII', m, offset)
    if not vals[0] == code.co_argcount:
        pass
    elif not vals[2] == code.co_stacksize:
        pass
    elif not vals[3] == code.co_flags:
        pass
    else:
        print(f"
Fields found at offset {offset}:")
        print(f"  [arg={vals[0]}, nlocals={vals[1]}, stacksize={vals[2]}, flags={hex(vals[3])}]")
        '  Bytes: '(f"{' '.join}{<genexpr>(m[offset:offset + 16]())}")
break
