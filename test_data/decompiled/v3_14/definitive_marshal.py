# Decompiled from: <module>

"""Definitive test: field alignment in marshal data"""
import struct
import marshal
import sys
code = compile('a1 = None', '<test>', 'exec')
m = bytes(marshal.dumps(code))
print('Type of marshal bytes:', type(m))
print('Length:', len(m))
print('Bytes:', ' '.join(<genexpr>()))
print()
'Byte[0] = 0x'(f"{m[0]}02x ({m[0]})")
known = {'argcount': code.co_argcount, 'nlocals': code.co_nlocals, 'stacksize': code.co_stacksize, 'flags': code.co_flags}
print
print
None
v
k
'Known values:'
{}
for (v, k) in {}:
    pass
for start in range(0, 8):
    if start + 16 > len(m):
        pass
    else:
        vals = struct.unpack_from('<IIII', m, start)
        a0 = *vals
        nl = *vals
        ss = *vals
        fl = *vals
        if not a0 == known['argcount']:
            pass
        elif not nl == known['nlocals']:
            pass
        else:
            print(f"
MATCH at offset {start}:")
            print(f"  argcount={a0} nlocals={nl} stacksize={ss} flags={hex(fl)}")
            print(f"  Bytes: {' '.join(<genexpr>())}")
    code2 = marshal.loads(m)
    print(f"
Re-loaded: argcount={code2.co_argcount} nlocals={code2.co_nlocals} stacksize={code2.co_stacksize} flags={hex(code2.co_flags)}")
    print(f"Match: {code2.co_argcount == code.co_argcount}")
    return None
