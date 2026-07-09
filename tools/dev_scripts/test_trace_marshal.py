"""Trace marshal structure of abc.3.11.pyc byte by byte"""
import struct, sys

path = 'test_data/compiled/abc.3.11.pyc'
with open(path, 'rb') as f:
    data = f.read()

# Header is 16 bytes
# Marshal starts at offset 16
pos = 16

def read_byte():
    global pos
    b = data[pos]
    pos += 1
    return b

def read_int32():
    global pos
    v = struct.unpack('<i', data[pos:pos+4])[0]
    pos += 4
    return v

def read_marshal_object(depth=0, label=""):
    global pos
    indent = "  " * depth
    if depth > 10:
        print(f"{indent}(max depth reached)")
        return
    
    raw_type = read_byte()
    actual_type = raw_type & 0x7F
    has_ref = bool(raw_type & 0x80)
    
    type_names = {
        0x2A: 'SMALL_TUPLE', 0x29: 'TUPLE', 0x28: 'INT', 0x41: 'FLOAT',
        0x42: 'BINARY_FLOAT', 0x4E: 'NONE', 0x54: 'TRUE', 0x46: 'FALSE',
        0x63: 'TYPE_CODE', 0x73: 'STR/CODE_SIMPLE', 0x7B: 'DICT',
        0x6C: 'LIST', 0x3F: 'LONG', 0x72: 'REF', 0x7A: 'SET',
        0x7E: 'FROZENSET', 0x6E: 'ELLIPSIS',
        0x7D: 'SHORT_ASCII', 0x5A: 'SHORT_ASCII_INTERNED',
        0x61: 'ASCII', 0x74: 'ASCII_INTERNED', 0x75: 'BYTES',
        0x7A: 'SET', 0x73: 'STRING', 0x7C: 'CODE_SIMPLE',
    }
    tn = type_names.get(actual_type, f'0x{actual_type:02X}')
    
    if has_ref:
        print(f"{indent}[REF#{label or '?'}] {tn} (0x{raw_type:02X})")
    else:
        print(f"{indent}{tn} (0x{raw_type:02X})")
    
    if actual_type == 0x63:  # TYPE_CODE
        read_type_code(depth+1)
    elif actual_type == 0x73:  # TYPE_STRING (or TYPE_CODE_SIMPLE in 3.11+)
        # For 3.11+, this is TYPE_CODE_SIMPLE
        read_type_code_simple(depth+1)
    elif actual_type in (0x2A, 0x29, 0x6C):  # SMALL_TUPLE, TUPLE, LIST
        if actual_type == 0x2A:
            count = read_byte()
        else:
            count = read_int32()
        print(f"{indent}  (count={count})")
        for i in range(count):
            read_marshal_object(depth+1, str(i))
    elif actual_type == 0x7B:  # DICT
        print(f"{indent}  (key-value pairs)")
        while pos < len(data):
            peek = data[pos] & 0x7F
            if peek == 0x4E:  # TYPE_NONE
                read_byte()
                break
            read_marshal_object(depth+1, "key")
            read_marshal_object(depth+1, "val")
    elif actual_type == 0x72:  # REF
        ref_idx = read_int32()
        print(f"{indent}  -> ref#{ref_idx}")
    elif actual_type in (0x7A, 0x5A, 0x7D,):  # SHORT_ASCII, SHORT_ASCII_INTERNED
        length = read_byte()
        val = data[pos:pos+length].decode('ascii', errors='replace')
        pos += length
        print(f"{indent}  = '{val[:60]}'")
    elif actual_type in (0x61, 0x74, 0x75):  # ASCII, ASCII_INTERNED, UNICODE, BYTES
        length = read_int32()
        if length > 0:
            val = data[pos:pos+length]
            pos += length
            if length < 100:
                try:
                    print(f"{indent}  = '{val.decode('ascii', errors='replace')[:60]}'")
                except:
                    print(f"{indent}  = bytes {val.hex()[:40]}")
            else:
                print(f"{indent}  = ({length} bytes)")
    elif actual_type == 0x28:  # INT
        val = read_int32()
        print(f"{indent}  = {val}")
    elif actual_type == 0x4E:  # NONE
        pass
    elif actual_type in (0x54, 0x46):  # TRUE, FALSE
        print(f"{indent}  = {actual_type == 0x54}")
    elif actual_type == 0x6E:  # ELLIPSIS
        print(f"{indent}  = ...")
    else:
        print(f"{indent}  [unknown type at pos {pos-1}]")

def read_type_code(depth=0):
    indent = "  " * depth
    code_start = pos - 1
    argcount = read_int32()
    posonly = read_int32()
    kwonly = read_int32()
    stacksize = read_int32()
    flags = read_int32()
    print(f"{indent}  arg={argcount} posonly={posonly} kwonly={kwonly} stack={stacksize} flags=0x{flags:x}")
    
    # bytecode
    raw = data[pos]
    pos += 1
    bc_type = raw & 0x7F
    if bc_type == 0x73:  # TYPE_STRING
        bc_len = struct.unpack('<i', data[pos:pos+4])[0]
        pos += 4 + bc_len
        print(f"{indent}  bytecode: {bc_len} bytes")
    else:
        print(f"{indent}  bytecode: unexpected type 0x{bc_type:02X} at pos {pos-1}")
    
    # constants as tuple
    read_marshal_object(depth+1, "consts")
    
    # names
    read_marshal_object(depth+1, "names")
    # localsplusnames
    read_marshal_object(depth+1, "localsplusnames")
    # localspluskinds
    raw = data[pos]
    pos += 1
    lp_type = raw & 0x7F
    if lp_type == 0x73:  # TYPE_STRING
        lp_len = struct.unpack('<i', data[pos:pos+4])[0]
        pos += 4 + lp_len
        print(f"{indent}  localspluskinds: {lp_len} bytes")
    else:
        print(f"{indent}  localspluskinds: unexpected type 0x{lp_type:02X}")
    
    # filename
    read_marshal_object(depth+1, "filename")
    # name
    read_marshal_object(depth+1, "name")
    # qualname
    read_marshal_object(depth+1, "qualname")
    
    # firstlineno
    lineno = read_int32()
    print(f"{indent}  firstlineno={lineno}")
    
    # lnotab
    raw = data[pos]
    pos += 1
    lno_type = raw & 0x7F
    if lno_type in (0x73, 0x75):  # TYPE_STRING or TYPE_BYTES
        lno_len = struct.unpack('<i', data[pos:pos+4])[0]
        pos += 4 + lno_len
        print(f"{indent}  lnotab: {lno_len} bytes")
    
    # exceptiontable
    if pos < len(data):
        raw = data[pos]
        ex_type = raw & 0x7F
        if ex_type in (0x73, 0x75):
            pos += 1
            ex_len = struct.unpack('<i', data[pos:pos+4])[0]
            pos += 4 + ex_len
            print(f"{indent}  exceptiontable: {ex_len} bytes")
        elif ex_type == 0x72:
            pos += 1
            ref_idx = read_int32()
            print(f"{indent}  exceptiontable: ref#{ref_idx}")

def read_type_code_simple(depth=0):
    indent = "  " * depth
    argcount = read_int32()
    nlocals = read_int32()
    stacksize = read_int32()
    flags = read_int32()
    print(f"{indent}  [SIMPLE] arg={argcount} nlocals={nlocals} stack={stacksize} flags=0x{flags:x}")
    # Then same as type_code for bytecode+ etc
    # bytecode
    raw = data[pos]
    pos += 1
    bc_type = raw & 0x7F
    if bc_type == 0x73:  # TYPE_STRING
        bc_len = struct.unpack('<i', data[pos:pos+4])[0]
        pos += 4 + bc_len
        print(f"{indent}  bytecode: {bc_len} bytes")
    # ... same as type_code for the rest

print(f"=== Marshal structure at offset {pos} ===\n")
read_marshal_object(0, "top")
print(f"\nFinal position: {pos}/{len(data)} (remaining: {len(data)-pos} bytes)")
