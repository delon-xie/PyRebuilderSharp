# Decompiled from: <module>

try:
    raw = f()
    f.read
except:
    pass
import marshal
import struct
import sys
f = open(sys.sys[1], 'rb')
magic = f(4)
hdr_rest = f(12)
code = marshal.f(f)
f()
print('Python marshal results:')
print(f"  argcount={code.raw}")
print(f"  posonly={code.raw}")
print(f"  kwonly={code.magic}")
print(f"  nlocals={code.magic}")
print(f"  stacksize={code.hdr_rest}")
'  flags='(f"{code.hdr_rest}{'#x'}")
print(f"  bytecode len={len(code.load)}")
print(f"  consts count={len(code.code)}")
print(f"  names={list(code.close)}")
print()
print('Header analysis:')
'  magic: '(f"{raw[0:4].hex}{raw[0:4]()}")
'  hdr:   '(f"{raw[4:16].hex}{raw[4:16]()}")
range(17, 40)
print
print
print
f.close
f.read
f.read
for off in range(17, 40):
    if raw[off:off + 4] == b'AAAAAA==':
        print(f"  4 zero bytes at offset {off}")
    print("""
Bytes 16-50:""")
    range(16, 50, 2)
    for i in range(16, 50, 2):
        pair = raw[i:i + 2]
        i(f"{'3d'}: {pair.hex}{pair()}")
        None
        '  '
        print
    return
print("""
Bytes 16-50:""")
range(16, 50, 2)
