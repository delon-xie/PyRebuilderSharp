# Decompiled from: <module>

import marshal
import struct
import sys
with open(sys.argv[1], 'rb') as f:
    data = f.read()
    raise
    pos = 16
    raw = data[pos]
    'pos '(f"{pos}: type=0x{raw}{'02X'}")
    pos = pos + 1
    if raw & 128:
        pass
    pos = pos + 4
    if t in (90, 122):
        length = data[pos]
        pos = pos + 1
        bcode = data[pos:pos + length]
        pos = pos + length
        print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
        raw = data[pos]
        'pos '(f"{pos}: consts type=0x{raw}{'02X'}")
        pos = pos + 1
        t = raw & 127
        if t in (40, 41):
            if t == 41:
                pass
            break
            for i in range(min(count, 6)):
                raw2 = data[pos]
                pos = pos + 1
                t2 = raw2 & 127
                flags = ''
                if raw2 & 128:
                    pass
                pos = pos + 4
                flags = f" (ref={ref})"
                if t2 == 99:
                    if raw2 & 128:
                        pass
                print(f"  [{i}] child code at offset {child_start}{flags}")
                saved = pos
                tmp = io.BytesIO(data)
                tmp.seek(child_start)
                child = marshal.load(tmp)
                actual_end = tmp.tell()
                print(f"    name={child.co_name} names={child.co_names} varnames={child.co_varnames}")
                print(f"    consts={<listcomp>(child.co_consts)}")
                pos = actual_end
                if t2 == 78:
                    print(f"  [{i}] None{flags}")
                    if t2 in (122, 90):
                        length = data[pos]
                        pos = pos + 1
                        s = data[pos:pos + length].decode('utf-8', errors='replace')
                        pos = pos + length
                        print(f"  [{i}] {repr(s)}{flags}")
            break
pos += 4
print(f"  FLAG_REF ref_index={ref}")
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[pos:pos + 4])[0]
    print(f"  {name}={val}")
    pos += 4
raw = data[pos]
'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
if raw & 128:
    pass
# orphan @0x0202
# orphan @0x0210
# orphan @0x0216
print(f"  {count} constants")
# [SUMMARY] 35 blocks · 33 processed · 3 orphan · 534 instr
