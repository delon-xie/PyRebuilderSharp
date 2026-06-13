# Properly trace the marshal structure for abc.3.12.pyc
import struct, io

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/abc.3.12.pyc', 'rb') as f:
    header = f.read(16)
    data = f.read()

def dump_at(stream, start, label=""):
    stream.seek(start)
    raw = stream.read(1)[0]
    t = raw & ~0x80
    names = {
        0x63:"TYPE_CODE", 0x73:"TYPE_STRING/CODE_SIMPLE", 0x7C:"TYPE_BYTES",
        0x28:"TUPLE", 0x29:"SMALL_TUPLE", 0x5B:"LIST",
        0x7A:"SHORT_ASCII", 0x5A:"SHORT_ASCII_INTERNED",
        0x61:"ASCII", 0x74:"ASCII_INTERNED", 0x75:"UNICODE", 116:"INTERNED",
        0x6E:"NONE", 0x69:"INT", 0x70:"INT64",
        0x4E:"TRUE", 0x46:"FALSE",
        0x72:"REF", 0x7B:"DICT"
    }
    type_name = names.get(t, f"0x{t:02X}")
    if label:
        print(f"  {label}: pos={start} type={type_name} (raw=0x{raw:02X})")
    stream.seek(start)

# The top-level code starts at offset 0
# After 1 type byte (0xE3 = TYPE_CODE|FLAG_REF) + 5*4 fields = 21 bytes
# bytecodes at offset 21: TYPE_STRING, length=226, then 226 bytes
# After bytecodes: offset 21 + 1 + 4 + 226 = 252

pos = 252
dump_at(io.BytesIO(data), pos, "co_consts (should be TUPLE)")

# Read the tuple
s = io.BytesIO(data)
s.seek(252)
t_raw = s.read(1)[0]
t = t_raw & ~0x80
if t == 0x28:  # TUPLE
    count = struct.unpack('<i', s.read(4))[0]
    print(f"  tuple count={count}")
elif t == 0x29:  # SMALL_TUPLE
    count = s.read(1)[0]
    print(f"  small tuple count={count}")
else:
    print(f"  NOT A TUPLE! type=0x{t:02X}")

# Walk through tuple elements
for i in range(count):
    elem_start = s.tell()
    raw = s.read(1)[0]
    etype = raw & ~0x80
    flag_ref = raw & 0x80
    
    if etype == 0x6E:  # NONE
        pass
    elif etype == 0x69:  # INT
        s.seek(4, 1)
    elif etype in (0x7A, 0x5A):  # SHORT_ASCII / SHORT_ASCII_INTERNED
        slen = s.read(1)[0]
        s.seek(slen, 1)
    elif etype in (0x73, 0x75, 0x61, 0x74, 116):  # LONG strings
        slen = struct.unpack('<i', s.read(4))[0]
        s.seek(slen, 1)
    elif etype == 0x63:  # TYPE_CODE
        # Skip: 5 int32 + bytecodes + co_consts + names + ... (complex)
        # Just mark the position
        print(f"  [{i}] TYPE_CODE at {elem_start}")
        # Don't try to skip, just note it
        continue
    elif etype == 0x73:  # TYPE_STRING or TYPE_CODE_SIMPLE
        print(f"  [{i}] TYPE_STRING/CODE_SIMPLE at {elem_start}")
        continue
    elif etype == 0x72:  # REF
        ref_idx = struct.unpack('<i', s.read(4))[0]
    else:
        print(f"  [{i}] unknown type 0x{etype:02X} at {elem_start}")
        continue

print(f"\nStream position after {i+1} tuple elements: {s.tell()}")
print(f"Expected: should be at names after co_consts")
