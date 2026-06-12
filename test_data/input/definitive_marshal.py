#!/usr/bin/env python3
"""Definitive test: field alignment in marshal data"""
import struct, marshal, sys

code = compile('a1 = None', '<test>', 'exec')
m = bytes(marshal.dumps(code))
print('Type of marshal bytes:', type(m))
print('Length:', len(m))
print('Bytes:', ' '.join(f'{b:02x}' for b in m[:60]))
print()

# Position 0: first byte  
print(f'Byte[0] = 0x{m[0]:02x} ({m[0]})')

# FIELD_ORDER for 3.x code object:
# argcount(4), nlocals(4), stacksize(4), flags(4)

# Read fields at different offsets and compare with known values
known = {
    'argcount': code.co_argcount,
    'nlocals': code.co_nlocals,
    'stacksize': code.co_stacksize,
    'flags': code.co_flags,
}
print('Known values:', {k: f'{v} ({hex(v)})' if k == 'flags' else v for k, v in known.items()})

for start in range(0, 8):
    if start + 16 > len(m):
        break
    vals = struct.unpack_from('<IIII', m, start)
    a0, nl, ss, fl = vals
    if a0 == known['argcount'] and nl == known['nlocals']:
        print(f'\nMATCH at offset {start}:')
        print(f'  argcount={a0} nlocals={nl} stacksize={ss} flags={hex(fl)}')
        # Show bytes at this offset
        print(f'  Bytes: {" ".join(f"{b:02x}" for b in m[start:start+16])}')

# Also check what Python's marshal.loads sees
code2 = marshal.loads(m)
print(f'\nRe-loaded: argcount={code2.co_argcount} nlocals={code2.co_nlocals} stacksize={code2.co_stacksize} flags={hex(code2.co_flags)}')
print(f'Match: {code2.co_argcount == code.co_argcount}')
