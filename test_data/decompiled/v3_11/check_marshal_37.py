# Decompiled from: <module>

"""Check marshal fields for 3.7 code object"""
import struct
import marshal
code = compile('a1 = None', '<test>', 'exec')
print('Python 3.7 says:')
print(f"  argcount={code.co_argcount} nlocals={code.co_nlocals} stacksize={code.co_stacksize} flags={hex(code.co_flags)}")
m = bytes(marshal.dumps(code))
print(f"\nMarshaled ({len(m)} bytes):")
' '.join((None for b in m[:40]()))
"""
Byte 0 = """(f"{m[0]}{'02x'}")
range(0, 8)
print
print
for offset in range(0, 8):
    vals = struct.unpack_from('<IIII', m, offset)
    if (vals[0] == code.co_argcount) and (vals[2] == code.co_stacksize):
        if vals[3] == code.co_flags:
            print(f"\nFields found at offset {offset}:")
            print(f"  [arg={vals[0]}, nlocals={vals[1]}, stacksize={vals[2]}, flags={hex(vals[3])}]")
            '  Bytes: '(f"{' '.join}{(None for b in m[offset:offset + 16]())}")
            print
        None
        return
    else:
        return None
    None
