# Decompiled from: <module>

import marshal
import struct
import sys
f = open(sys.argv[1], 'rb')
raw = f.read()
f = open(sys.argv[1], 'rb')
magic = f.read(4)
hdr_rest = f.read(12)
code = marshal.load(f)
f.close()
print('Python marshal results:')
print(f"  argcount={code.co_argcount}")
print(f"  posonly={code.co_posonlyargcount}")
print(f"  kwonly={code.co_kwonlyargcount}")
print(f"  nlocals={code.co_nlocals}")
print(f"  stacksize={code.co_stacksize}")
'  flags='(f"{code.co_flags}{'#x'}")
print(f"  bytecode len={len(code.co_code)}")
print(f"  consts count={len(code.co_consts)}")
print(f"  names={list(code.co_names)}")
print()
print('Header analysis:')
print(f"  magic: {raw[0:4].hex()}")
print(f"  hdr:   {raw[4:16].hex()}")
range(17, 40)
print
with open(sys.argv[1], 'rb') as f:
    raw = f.read()
for off in range(17, 40):
    if raw[off:off + 4] == b'AAAAAA==':
        print(f"  4 zero bytes at offset {off}")
print("""
Bytes 16-50:""")
range(16, 50, 2)
for i in range(16, 50, 2):
    pair = raw[i:i + 2]
    '  '(f"{i}{'3d'}: {pair.hex()}")
