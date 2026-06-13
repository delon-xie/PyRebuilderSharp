import marshal, struct, io, sys

# Open abc.3.12.pyc and trace marshal structure carefully
with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/abc.3.12.pyc', 'rb') as f:
    header = f.read(16)
    data = f.read()  # marshal data starts here

stream = io.BytesIO(data)
offset = 0  # relative to marshal data start

def read_int(stream):
    """Read a 4-byte little-endian int"""
    b = stream.read(4)
    return struct.unpack('<i', b)[0]

def peek(stream):
    """Peek at the next byte without consuming it"""
    pos = stream.tell()
    b = stream.read(1)
    stream.seek(pos)
    return b[0] if b else None

def trace_type_code(stream, name_override=None, depth=0):
    """Trace a TYPE_CODE structure, step by step"""
    indent = "  " * depth
    start = stream.tell()
    
    t_raw = stream.read(1)[0]
    t = t_raw & ~0x80  # strip FLAG_REF
    if t != 0x63:
        print(f"{indent}NOT TYPE_CODE (raw=0x{t_raw:02x} pure=0x{t:02x}) at {start}")
        stream.seek(start)
        return
    
    print(f"{indent}TYPE_CODE at marshal offset {start}: (raw=0x{t_raw:02x})")
    
    # 5 int32 fields for 3.12
    argcount = read_int(stream)
    posonly = read_int(stream)
    kwonly = read_int(stream)
    stacksize = read_int(stream)
    flags = read_int(stream)
    print(f"{indent}  fields: argcount={argcount} posonly={posonly} kwonly={kwonly} stacksize={stacksize} flags=0x{flags:04x}")
    
    # bytecodes - should be TYPE_STRING
    bt_pos = stream.tell()
    bt = stream.read(1)[0]
    print(f"{indent}  bytecode type byte: 0x{bt:02x} at {bt_pos}")
    
    if bt == 0x73:  # TYPE_STRING
        blen = read_int(stream)
        bc = stream.read(blen)
        print(f"{indent}  bytecodes: {blen} bytes, starts with 0x{bc[0]:02x}")
        print(f"{indent}    raw: {' '.join(f'{b:02x}' for b in bc[:16])}...")
    else:
        print(f"{indent}  UNEXPECTED bytecode type: 0x{bt:02x}")
        return
    
    # co_consts - should be TUPLE
    ct_pos = stream.tell()
    ct = stream.read(1)[0]
    print(f"{indent}  co_consts type: 0x{ct:02x} at {ct_pos}")
    
    if ct == 0x28:  # TUPLE
        cn = read_int(stream)
        print(f"{indent}  co_consts tuple: {cn} items")
        for i in range(cn):
            ci_pos = stream.tell()
            ci_t_raw = stream.read(1)[0]
            ci_t = ci_t_raw & ~0x80
            ci_t_str = {0x63: 'CODE', 0x73: 'STR/SIMPLE', 0x6e: 'NONE', 
                       0x61: 'ASCII', 0x74: 'ASCII_INTERNED', 0x7a: 'SHORT_ASCII',
                       0x5a: 'SHORT_ASCII_INTERNED', 0x28: 'TUPLE', 0x29: 'SMALL_TUPLE',
                       0x75: 'UNICODE', 0x7c: 'BYTES', 0x69: 'INT', 0x70: 'TRUE',
                       0x71: 'FALSE'}.get(ci_t, f'?{ci_t:02x}')
            
            if ci_t == 0x63:
                print(f"{indent}    [{i}] CODE at {ci_pos} (nested)")
                trace_type_code(stream, depth=depth+1)
            else:
                # Skip to next item
                stream.read(1)
                if ci_t in (0x6e, 0x70, 0x71):  # None, True, False
                    pass
                elif ci_t in (0x7a, 0x5a):  # short string
                    l = stream.read(1)[0]
                    s = stream.read(l).decode('ascii', errors='replace')
                    print(f"{indent}    [{i}] {ci_t_str} at {ci_pos}: {s[:40]}")
                elif ci_t in (0x61, 0x74, 0x75, 0x73):  # long string
                    l = read_int(stream)
                    s = stream.read(l).decode('utf-8', errors='replace') if l < 1000 else stream.read(l)
                    print(f"{indent}    [{i}] {ci_t_str} at {ci_pos}: len={l}")
                elif ci_t == 0x28:  # tuple
                    n = read_int(stream)
                    print(f"{indent}    [{i}] TUPLE at {ci_pos}: {n} items (skipping)")
                    for _ in range(n):
                        sub_t = stream.read(1)[0]
                        if sub_t in (0x6e, 0x70, 0x71):
                            pass
                        elif sub_t in (0x7a, 0x5a):
                            l = stream.read(1)[0]
                            stream.read(l)
                        elif sub_t in (0x61, 0x74, 0x73, 0x75):
                            l = read_int(stream)
                            stream.read(l)
                elif ci_t == 0x69:  # int
                    read_int(stream)
                else:
                    break
    else:
        print(f"{indent}  UNEXPECTED co_consts type: 0x{ct:02x}")
    
    # Check where we end up
    end_pos = stream.tell()
    print(f"{indent}  --- end of trace at {end_pos} ---")

# Start tracing from the beginning
stream.seek(0)
trace_type_code(stream)
print(f"\nFinal stream position: {stream.tell()} / {len(data)}")
print(f"Expected final position: {len(data)} (entire marshal consumed)")
