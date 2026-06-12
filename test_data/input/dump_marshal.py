import marshal, struct, sys

with open(sys.argv[1],'rb') as f:
    data = f.read()

pos = 16
# Module header  
raw = data[pos]; print(f'pos {pos}: type=0x{raw:02X}')
pos += 1
if raw & 0x80:
    ref = struct.unpack('<I', data[pos:pos+4])[0]; pos += 4
    print(f'  FLAG_REF ref_index={ref}')

# 6 int32 code object fields
for name in ['argcount','posonly','kwonly','nlocals','stacksize','flags']:
    val = struct.unpack('<i', data[pos:pos+4])[0]; print(f'  {name}={val}')
    pos += 4

# Bytecode
raw = data[pos]; print(f'pos {pos}: bytecode type=0x{raw:02X}')
pos += 1
t = raw & 0x7F
if raw & 0x80:
    ref = struct.unpack('<I', data[pos:pos+4])[0]; pos += 4
if t in (0x5a, 0x7a):
    length = data[pos]; pos += 1
    bcode = data[pos:pos+length]; pos += length
    print(f'  bytecode ({length}B): {bcode.hex()[-30:]}')

# Constants tuple   
raw = data[pos]; print(f'pos {pos}: consts type=0x{raw:02X}')
pos += 1
t = raw & 0x7F
if t in (0x28, 0x29):
    count = data[pos] if t == 0x29 else struct.unpack('<I', data[pos:pos+4])[0]
    pos += 1 if t == 0x29 else 4
    print(f'  {count} constants')
    for i in range(min(count, 6)):
        raw2 = data[pos]; pos += 1
        t2 = raw2 & 0x7F
        flags = ''
        if raw2 & 0x80:
            ref = struct.unpack('<I', data[pos:pos+4])[0]; pos += 4
            flags = f' (ref={ref})'
        if t2 == 0x63:  # TYPE_CODE/nested
            child_start = pos - 1 - (4 if raw2 & 0x80 else 0)
            print(f'  [{i}] child code at offset {child_start}{flags}')
            # Skip child entirely using marshal
            saved = pos
            tmp = io.BytesIO(data)
            tmp.seek(child_start)
            child = marshal.load(tmp)
            actual_end = tmp.tell()
            print(f'    name={child.co_name} names={child.co_names} varnames={child.co_varnames}')
            print(f'    consts={[repr(c) for c in child.co_consts]}')
            pos = actual_end
        elif t2 == 0x4E:  # None
            print(f'  [{i}] None{flags}')
        elif t2 in (0x7a, 0x5a):
            # Short string
            length = data[pos]; pos += 1
            s = data[pos:pos+length].decode('utf-8', errors='replace'); pos += length
            print(f'  [{i}] {repr(s)}{flags}')
        else:
            print(f'  [{i}] type=0x{raw2:02X} (stripped={t2}){flags} -> skip')
            # Try marshal
            tmp = io.BytesIO(data)
            tmp.seek(pos-1)
            val = marshal.load(tmp)
            pos = tmp.tell()
            print(f'    -> {repr(val)}')

print(f'pos {pos}: after all constants')
print(f'total file: {len(data)}')
