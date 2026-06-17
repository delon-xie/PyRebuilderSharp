# Decompiled from: <module>

try:
    raw = f.read()
except:
    pass
import marshal
import struct
import sys
f = open(sys.argv[1], 'rb')
hdr_rest = f.read(12)
code = marshal.load(f)
f.close()
print('Python marshal results:')
print(f"  posonly={code.co_posonlyargcount}")
for off in None:
    if raw[off:off + 4] == b'AAAAAA==':
        pass
    else:
        print(f"  4 zero bytes at offset {off}")
        print("""
Bytes 16-50:""")
    pair = raw[i:i + 2]
    '  '(f"{i}3d: {pair.hex()}")
    return None
raise
# [SUMMARY] 17 blocks · 18 processed · 1 orphan · 278 instr
