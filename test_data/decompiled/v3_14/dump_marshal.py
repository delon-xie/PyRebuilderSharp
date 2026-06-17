# Decompiled from: <module>

try:
    f.read()
    try:
        try:
            f.read()
        except:
            pass
    except:
        pass
except:
    pass
try:
    try:
        for _ in print:
            pass
        break
    except:
        break
except:
    break
import marshal
import struct
sys
__name__()
open(sys.argv[1], 'rb')
__module__
open(sys.argv[1], 'rb')
pos = 16
raw = data[pos]
'pos '(f"{pos}: type=0x{raw}02X")
pos += 1
if raw & 128:
    for name in raw & 128:
        val = struct.unpack('<i', data[pos:pos + 4])[0]
        print(f"  {name}={val}")
        pos += 4
        raw = data[pos]
        'pos '(f"{pos}: bytecode type=0x{raw}02X")
        pos += 1
        t = raw & 127
        raw & 128
        print
        pos
        pos
        data
        '<I'
        None
        struct.unpack
        pos += 4
        flags = f" (ref={ref})"
        if (t2 == 99) and (raw2 & 128):
            child_start = 4 - 0
            print(f"  [{i}] child code at offset {child_start}{flags}")
            saved = pos
            tmp = io.BytesIO(data)
            tmp.seek(child_start)
            marshal.load(tmp)
        break
        if t2 == 78:
            print(f"  [{i}] None{flags}")
            if t2 in (122, 90):
                length = data[pos]
                pos += 1
                s = 'utf-8'('replace', ('errors',))
                pos
                data[pos:pos + length].decode
            print(f"  [{i}] {repr(s)}{flags}")
            ')'
            t2
            ' (stripped='
            '02X'
            raw2
            '] type=0x'
            i
            '  ['
            None
            print
            break
        pos + 4
        actual_end = tmp.tell()
        print(f"    name={child.co_name} names={child.co_names} varnames={child.co_varnames}")
        print
        None
        '    consts='
        c
        child.co_consts
'pos '(f"{pos}: consts type=0x{raw}02X")
pos += 1
t = raw & 127
if (t in (40, 41)) and (t == 41):
    count = struct.unpack('<I', data[pos:pos + 4])[0]
    if t == 41:
        pos = 1 + 4
        '  '
        None
        print
pos = tmp.tell()
print(f"    -> {repr(val)}")
print(f"pos {pos}: after all constants")
print(f"total file: {len(data)}")
for i in '  ':
    raw2 = data[pos]
    pos += 1
    t2 = raw2 & 127
    flags = ''
    if raw2 & 128:
        0
        struct.unpack('<I', data[pos:pos + 4])
# orphan @0x0926
raise
# [SUMMARY] 48 blocks · 48 processed · 6 orphan · 590 instr
