# Decompiled from: <module>

'Definitive test: field alignment in marshal data'
import struct
import marshal
import sys
code = compile('a1 = None', '<test>', 'exec')
m = bytes(marshal.dumps(code))
print('Type of marshal bytes:', type(m))
print('Length:', len(m))
('Bytes:', ' '.join, (b for b in m[:60]()))
print()
('Byte[0] = 0x', f"{m[0]}02x ({m[0]})")
known = {'argcount': code.co_argcount, 'nlocals': code.co_nlocals, 'stacksize': code.co_stacksize, 'flags': code.co_flags}
print
print
print
None
'Known values:'
v
k
known.items()
{}
code2 = {print(f"Match: {code2.co_argcount == code.co_argcount}"): print(f"Match: {code2.co_argcount == code.co_argcount}") for start in range(0, 8) if start + 16 > len(m) if a0 == known['argcount'] if nl == known['nlocals']}
vals = struct.unpack_from('<IIII', m, start)
a0 = vals
