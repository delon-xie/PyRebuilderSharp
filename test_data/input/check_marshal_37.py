#!/usr/bin/env python3
"""Check marshal fields for 3.7 code object"""
import struct, marshal

code = compile('a1 = None', '<test>', 'exec')
print('Python 3.7 says:')
print(f'  argcount={code.co_argcount} nlocals={code.co_nlocals} stacksize={code.co_stacksize} flags={hex(code.co_flags)}')

m = bytes(marshal.dumps(code))
print(f'\nMarshaled ({len(m)} bytes):')
print(' '.join(f'{b:02x}' for b in m[:40]))

# Position 0 is TYPE_CODE | FLAG_REF
print(f'\nByte 0 = {m[0]:02x}')

# Try reading 4 int32 fields starting from different offsets
for offset in range(0, 8):
    vals = struct.unpack_from('<IIII', m, offset)
    # Check if vals[0]==co_argcount and vals[2]==co_stacksize and vals[3]==co_flags
    if vals[0] == code.co_argcount and vals[2] == code.co_stacksize and vals[3] == code.co_flags:
        print(f'\nFields found at offset {offset}:')
        print(f'  [arg={vals[0]}, nlocals={vals[1]}, stacksize={vals[2]}, flags={hex(vals[3])}]')
        print(f'  Bytes: {" ".join(f"{b:02x}" for b in m[offset:offset+16])}')
