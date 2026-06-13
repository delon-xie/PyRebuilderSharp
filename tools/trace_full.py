"""Dump marshal position of EVERY field for abc.3.12.pyc.
This shows exactly where Python's marshal.load positions things."""

import marshal, struct, io, sys

def read_const_at(code, idx, indent=""):
    """Show what a const looks like"""
    c = code.co_consts[idx] if idx < len(code.co_consts) else None
    if isinstance(c, type(lambda:0)):  # code object
        return f"<code {c.co_name}>"
    elif isinstance(c, str):
        return repr(c)[:60]
    elif c is None:
        return "None"
    else:
        return str(c)[:60]

# Load with deep nesting dump
with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/abc.3.12.pyc', 'rb') as f:
    header = f.read(16)
    data = f.read()

# Use Python's marshal to load the full structure
# BUT marshal.load is a C function that doesn't produce position info.
# Let's trace manually through the marshal data.

stream = io.BytesIO(data)
total = len(data)

def read_type():
    raw = stream.read(1)[0]
    return raw, raw & ~0x80

def read_int32():
    return struct.unpack('<i', stream.read(4))[0]

def skip_marshal_value():
    """Skip a single marshal value (don't parse it)"""
    raw, t = read_type()
    if t == 0x6E:  # NONE
        return
    elif t in (0x69, 0x70):  # INT, INT64
        stream.seek(4, 1)
    elif t in (0x6A, 0x71):  # LONG
        # Skip until 0
        while True:
            b = stream.read(1)[0]
            if b == 0:
                break
    elif t in (0x66, 0x67, 0x63):  # FLOAT, BINARY_FLOAT, COMPLEX (skip these)
        stream.seek(8, 1)
    elif t in (0x79, 0x7A):  # BINARY_COMPLEX
        stream.seek(16, 1)
    elif t in (0x7A, 0x5A):  # SHORT_ASCII variants
        slen = stream.read(1)[0]
        stream.seek(slen, 1)
    elif t in (0x73, 0x75, 0x61, 0x74, 0x7C, 116):  # LONG strings
        slen = read_int32()
        stream.seek(slen, 1)
    elif t == 0x28:  # TUPLE
        count = read_int32()
        for _ in range(count):
            skip_marshal_value()
    elif t == 0x29:  # SMALL_TUPLE
        count = stream.read(1)[0]
        for _ in range(count):
            skip_marshal_value()
    elif t == 0x72:  # REF
        read_int32()
    elif t == 0x63:  # TYPE_CODE
        # Read 5 int32 fields
        fields = [read_int32() for _ in range(5)]
        print(f"TYPE_CODE fields={fields} at {stream.tell()-20}")
        # bytecodes
        skip_marshal_value()
        # co_consts
        consts_pos = stream.tell()
        skip_marshal_value()
        consts_end = stream.tell()
        print(f"  co_consts: {consts_pos} → {consts_end} ({consts_end-consts_pos}B)")
        # names, varnames, freevars, cellvars
        for name in ['names','varnames','freevars','cellvars']:
            p = stream.tell()
            skip_marshal_value()
            print(f"  {name}: {p} → {stream.tell()}")
        # filename, name
        for name in ['filename','name']:
            p = stream.tell()
            skip_marshal_value()
            print(f"  {name}: {p} → {stream.tell()}")
        # qualname (3.11+)
        p = stream.tell()
        skip_marshal_value()
        print(f"  qualname: {p} → {stream.tell()}")
        # firstlineno
        p = stream.tell()
        fl = read_int32()
        print(f"  firstlineno: {p}={fl}")
        # lnotab
        p = stream.tell()
        skip_marshal_value()
        print(f"  lnotab: {p} → {stream.tell()}")
        # exceptiontable (3.11+)
        p = stream.tell()
        skip_marshal_value()
        print(f"  exceptiontable: {p} → {stream.tell()}")
    elif t == 0x73:  # Could be TYPE_CODE_SIMPLE for 3.11+
        # For 3.11+, treat as TYPE_CODE_SIMPLE: 4 fields
        fields = [read_int32() for _ in range(4)]
        print(f"TYPE_CODE_SIMPLE fields={fields} at {stream.tell()-16}")
        # Then same structure as TYPE_CODE
        skip_marshal_value()
        consts_pos = stream.tell()
        skip_marshal_value()
        consts_end = stream.tell()
        print(f"  co_consts: {consts_pos} → {consts_end}")
        for name in ['names','varnames','freevars','cellvars']:
            p = stream.tell()
            skip_marshal_value()
            print(f"  {name}: {p} → {stream.tell()}")
        for name in ['filename','name']:
            p = stream.tell()
            skip_marshal_value()
            print(f"  {name}: {p} → {stream.tell()}")
        # No qualname for TYPE_CODE_SIMPLE? Let me check...
        # Actually qualname IS always present for 3.11+ code objects
        p = stream.tell()
        skip_marshal_value()
        print(f"  qualname: {p} → {stream.tell()}")
        p = stream.tell()
        fl = read_int32()
        print(f"  firstlineno: {p}={fl}")
        p = stream.tell()
        skip_marshal_value()
        print(f"  lnotab: {p} → {stream.tell()}")
        p = stream.tell()
        skip_marshal_value()
        print(f"  exceptiontable: {p} → {stream.tell()}")

# Skip top-level type byte + 5 fields
stream.seek(21)

# Read bytes for bytecodes type byte
stream.read(1)
bc_len = read_int32()
stream.seek(bc_len, 1)
print(f"\n== Top-level code structure ==")
print(f"After bytecodes: {stream.tell()}")

# Now read co_consts
skip_marshal_value()
print(f"After co_consts: {stream.tell()}")

print(f"\nTotal marshal data: {total} bytes")
print(f"Final position: {stream.tell()}")
print(f"Difference: {total - stream.tell()} bytes")
