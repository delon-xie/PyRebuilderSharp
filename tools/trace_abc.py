# Python: dump exact marshal field positions for abc.3.12.pyc
# Compare with C# ReadMarshalCodeObject 3.11+ isSimple=false

import struct, marshal, io

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/abc.3.12.pyc', 'rb') as f:
    header = f.read(16)
    data = f.read()

def dump_code(stream, name, indent=0):
    """Trace marshal TYPE_CODE reading and compare with C# 3.11+ layout"""
    start = stream.tell()
    
    # TYPE_CODE type byte
    raw_type = stream.read(1)[0]
    pure_type = raw_type & ~0x80  # strip FLAG_REF
    if pure_type == 0x63:
        kind = "TYPE_CODE"
        fields = 5  # 3.11+: argcount, posonly, kwonly, stacksize, flags
    elif pure_type == 0x73:
        kind = "TYPE_CODE_SIMPLE"
        fields = 4  # 3.11+: argcount, nlocals, stacksize, flags
    else:
        stream.seek(start)
        return None
    
    print(f"{' '*indent}===== {name} [{kind}] at marshal offset {start} =====")
    
    # Read int32 fields
    fvals = []
    for i in range(fields):
        val = struct.unpack('<i', stream.read(4))[0]
        fvals.append(val)
    field_names = ["argcount","posonly","kwonly","nlocals","stacksize","flags"]
    print(f"{' '*indent}  Fields: {dict(zip(field_names[:fields], fvals))}")
    
    # Next: bytecodes — TYPE_STRING or TYPE_BYTES
    bc_start = stream.tell()
    bc_raw_type = stream.read(1)[0]
    bc_type = bc_raw_type & ~0x80
    bc_len = 0
    if bc_type in (0x73, 0x7C, 0x61, 0x74):  # TYPE_STRING/TYPE_BYTES/TYPE_ASCII
        bc_len = struct.unpack('<i', stream.read(4))[0]
        stream.seek(bc_len, 1)
    elif bc_type in (0x7A, 0x5A):  # TYPE_SHORT_ASCII / TYPE_SHORT_ASCII_INTERNED
        bc_len = stream.read(1)[0]
        stream.seek(bc_len, 1)
    else:
        print(f"{' '*indent}  ⚠️ UNKNOWN bytecode type: 0x{bc_type:02X}")
        return None
    
    print(f"{' '*indent}  bytecodes: type=0x{bc_type:02X} len={bc_len} at pos {bc_start} → {stream.tell()}")
    
    # co_consts
    consts_start = stream.tell()
    print(f"{' '*indent}  co_consts at: {consts_start}")
    
    # Now read what Python thinks is at consts_start
    stream.seek(consts_start)
    
    # co_names, co_varnames, co_freevars, co_cellvars
    list_positions = []
    for lst_name in ['names', 'varnames', 'freevars', 'cellvars']:
        pos = stream.tell()
        t = stream.read(1)[0] & ~0x80
        count = struct.unpack('<i' if t != 0x29 else '<B', stream.read(4 if t != 0x29 else 1))[0] if t in (0x28, 0x29) else 0
        # read strings
        for _ in range(count):
            s_raw = stream.read(1)[0]
            s_type = s_raw & ~0x80
            if s_type in (0x7A, 0x5A):
                sl = stream.read(1)[0]
                stream.seek(sl, 1)
            elif s_type in (0x73, 0x75, 0x61, 0x74, 116):
                sl = struct.unpack('<i', stream.read(4))[0]
                stream.seek(sl, 1)
        end = stream.tell()
        print(f"{' '*indent}  {lst_name}: pos={pos} count={count} end={end} (size={end-pos})")
    
    # filename & name
    for fn in ['filename', 'name']:
        fpos = stream.tell()
        print(f"{' '*indent}  {fn} at: {fpos}")
        s_raw = stream.read(1)[0]
        s_type = s_raw & ~0x80
        if s_type in (0x7A, 0x5A):
            sl = stream.read(1)[0]
            stream.seek(sl, 1)
        elif s_type in (0x73, 0x75):
            sl = struct.unpack('<i', stream.read(4))[0]
            stream.seek(sl, 1)
        else:
            print(f"{' '*indent}    type=0x{s_type:02X} UNKNOWN")
    
    # qualname (3.11+)
    qpos = stream.tell()
    print(f"{' '*indent}  qualname at: {qpos}")
    if kind == "TYPE_CODE":  # not simple
        s_raw = stream.read(1)[0]
        s_type = s_raw & ~0x80
        if s_type in (0x7A, 0x5A):
            sl = stream.read(1)[0]
            stream.seek(sl, 1)
        elif s_type in (0x73, 0x75):
            sl = struct.unpack('<i', stream.read(4))[0]
            stream.seek(sl, 1)
    
    # firstlineno (int32)
    flpos = stream.tell()
    fl = struct.unpack('<i', stream.read(4))[0]
    print(f"{' '*indent}  firstlineno at: {flpos} = {fl}")
    
    # lnotab/linetable
    lnotab_start = stream.tell()
    print(f"{' '*indent}  lnotab at: {lnotab_start}")
    
    # exceptiontable (3.11+)
    exc_start = stream.tell()
    if kind == "TYPE_CODE":
        print(f"{' '*indent}  exceptiontable at: {exc_start}")
    
    end = stream.tell()
    print(f"{' '*indent}  END at: {end}")
    print()
    
    return end

stream = io.BytesIO(data)
dump_code(stream, "<module>")

# Check remaining bytes
remaining = len(data) - stream.tell()
print(f"Remaining bytes after top-level code: {remaining}")
print(f"Total marshal data: {len(data)} bytes")
