# Decompiled from: <module>

# orphan @0x015C
length = data[pos]
pos += 1
bcode = data[pos:pos + length]
pos += length
print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
# orphan @0x012E
ref = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
with open(sys.argv[1], 'rb') as f:
    data = f.read()
    pos = 16
    raw = data[pos]
    'pos '(f"{pos}: type=0x{raw}{'02X'}")
    pos = pos + 1
    if raw & 128:
        ref = struct.unpack('<I', data[pos:pos + 4])[0]
        pos = pos + 4
        print(f"  FLAG_REF ref_index={ref}")
# orphan @0x01EE
struct.unpack('<I', data[pos:pos + 4])[0]
# orphan @0x021A
4
# orphan @0x026A
ref = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
flags = f" (ref={ref})"
# orphan @0x02B8
0
# orphan @0x03BA
'  ['(f"{i}] type=0x{raw2}{'02X'} (stripped={t2}){flags} -> skip")
tmp = io.BytesIO(data)
tmp.seek(pos - 1)
val = marshal.load(tmp)
pos = tmp.tell()
print(f"    -> {repr(val)}")
print
# orphan @0x041E
print(f"pos {pos}: after all constants")
print(f"total file: {len(data)}")
# [SUMMARY] 35 blocks · 27 processed · 30 orphan · 534 instr
