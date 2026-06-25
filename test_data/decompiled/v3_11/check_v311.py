# Decompiled from: <module>

import marshal
import struct
import sys
raw = f()
f.read
None(None)
f = open(sys.argv[1], 'rb')
magic = f(4)
hdr_rest = f(12)
code = marshal.load(f)
f()
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
'  magic: '(f"{raw[0:4].hex}{raw[0:4]()}")
'  hdr:   '(f"{raw[4:16].hex}{raw[4:16]()}")
print
print
print
f.close
f.read
f.read
for off in print:
    if raw[off:off + 4] == b'AAAAAA==':
        print(f"  4 zero bytes at offset {off}")
    print("""
Bytes 16-50:""")
    for i in range(16, 50, 2):
        pair = raw[i:i + 2]
        i(f"{'3d'}: {pair.hex}{pair()}")
        None
        '  '
        print
    return
print("""
Bytes 16-50:""")
