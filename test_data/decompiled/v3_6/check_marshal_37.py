# Decompiled from: <module>

"""Check marshal fields for 3.7 code object"""
import struct
import marshal
code = compile('a1 = None', '<test>', 'exec')
print('Python 3.7 says:')
print(f"  argcount={code.co_argcount} nlocals={code.co_nlocals} stacksize={code.co_stacksize} flags={hex(code.co_flags)}")
m = bytes(marshal.dumps(code))
print(f"\nMarshaled ({len(m)} bytes):")
print(' '.join((b for b in m[:40])))
"""
Byte 0 = """(f"{m[0]}{'02x'}")
range(0, 8)
print
print
vals = struct.unpack_from('<IIII', m, offset)
if (vals[0] == code.co_argcount) and not vals[2] == code.co_stacksize:
    return vals[3] == code.co_flags
