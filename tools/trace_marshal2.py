"""Trace marshal structure of abc.3.12.pyc with byte positions"""
import marshal, struct, io, sys

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/abc.3.12.pyc', 'rb') as f:
    f.read(16)  # skip header
    data = f.read()

def trace(stream, name='<module>', depth=0, max_depth=20):
    """Walk the marshal stream field by field, recording positions"""
    indent = '  ' * depth
    if depth > max_depth:
        return
    
    pos = stream.tell()
    raw_type = stream.read(1)[0]
    pure_type = raw_type & ~0x80  # strip FLAG_REF
    has_flag = raw_type & 0x80
    
    if pure_type == 0x63:  # TYPE_CODE
        # Get name first (we'll pass it through)
        print(f"TRACE: {indent}TYPE_CODE at pos {pos} (raw=0x{raw_type:02x} flagRef={bool(has_flag)})")
        
        fields_start = stream.tell()
        if depth == 0:
            # Top-level: 3.12, 5 fields
            f1 = struct.unpack('<i', stream.read(4))[0]  # argcount
            f2 = struct.unpack('<i', stream.read(4))[0]  # posonlyargcount
            f3 = struct.unpack('<i', stream.read(4))[0]  # kwonlyargcount
            f4 = struct.unpack('<i', stream.read(4))[0]  # stacksize
            f5 = struct.unpack('<i', stream.read(4))[0]  # flags
            print(f"TRACE: {indent}  fields[{fields_start}-{stream.tell()-1}]: arg={f1} posonly={f2} kwonly={f3} stack={f4} flags=0x{f5:04x}")
        else:
            # Nested: same 5 fields for 3.12
            f1 = struct.unpack('<i', stream.read(4))[0]
            f2 = struct.unpack('<i', stream.read(4))[0]
            f3 = struct.unpack('<i', stream.read(4))[0]
            f4 = struct.unpack('<i', stream.read(4))[0]
            f5 = struct.unpack('<i', stream.read(4))[0]
            print(f"TRACE: {indent}  fields[{fields_start}-{stream.tell()-1}]: arg={f1} posonly={f2} kwonly={f3} stack={f4} flags=0x{f5:04x}")
        
        # bytecodes
        bc_pos = stream.tell()
        bc_raw = stream.read(1)[0]
        bc_pure = bc_raw & ~0x80
        print(f"TRACE: {indent}  bytecodes at pos {bc_pos}: type=0x{bc_raw:02x} (pure=0x{bc_pure:02x})")
        
        if bc_pure in (0x73, 0x75):  # TYPE_STRING or TYPE_UNICODE
            bc_len = struct.unpack('<i', stream.read(4))[0]
            stream.read(bc_len)
            print(f"TRACE: {indent}    long_str: len={bc_len}")
        elif bc_pure in (0x7a, 0x5a):  # TYPE_SHORT_ASCII
            bc_len = stream.read(1)[0]
            stream.read(bc_len)
            print(f"TRACE: {indent}    short_str: len={bc_len}")
        elif bc_pure == 0x7c:  # TYPE_BYTES
            bc_len = struct.unpack('<i', stream.read(4))[0]
            stream.read(bc_len)
            print(f"TRACE: {indent}    bytes: len={bc_len}")
        else:
            print(f"TRACE: {indent}    UNKNOWN bytecode type!")
            return
        
        # co_consts
        cc_pos = stream.tell()
        cc_type = stream.read(1)[0] & ~0x80
        print(f"TRACE: {indent}  co_consts at pos {cc_pos}: type=0x{cc_type:02x}")
        
        if cc_type == 0x28:  # TUPLE
            n = struct.unpack('<i', stream.read(4))[0]
            print(f"TRACE: {indent}    tuple({n})")
            for i in range(n):
                trace(stream, f'{name}[{i}]', depth+1)
        elif cc_type == 0x29:  # SMALL_TUPLE
            n = stream.read(1)[0]
            print(f"TRACE: {indent}    small_tuple({n})")
            for i in range(n):
                trace(stream, f'{name}[{i}]', depth+1)
        elif cc_type == 0x6e:  # None
            print(f"TRACE: {indent}    None")
        else:
            # Skip unknown
            pass
        
        # names, varnames, freevars, cellvars
        for field in ['names', 'varnames', 'freevars', 'cellvars']:
            f_pos = stream.tell()
            f_type = stream.read(1)[0] & ~0x80
            print(f"TRACE: {indent}  {field} at pos {f_pos}: type=0x{f_type:02x}")
            if f_type in (0x28, 0x29):  # TUPLE or SMALL_TUPLE
                n = struct.unpack('<i', stream.read(4))[0] if f_type == 0x28 else stream.read(1)[0]
                print(f"TRACE: {indent}    tuple({n}) - skipping contents")
                for _ in range(n):
                    trace_skip(stream)
            else:
                break
        
        # filename, name
        fn_pos = stream.tell()
        fn_raw = stream.read(1)[0]
        fn_pure = fn_raw & ~0x80
        print(f"TRACE: {indent}  filename at pos {fn_pos}: type=0x{fn_raw:02x}")
        trace_skip(stream)
        
        nm_pos = stream.tell()
        nm_raw = stream.read(1)[0]
        nm_pure = nm_raw & ~0x80
        print(f"TRACE: {indent}  name at pos {nm_pos}: type=0x{nm_raw:02x}")
        trace_skip(stream)
        
        # qualname (3.11+ only)
        if True:  # isPython311+
            qn_pos = stream.tell()
            qn_raw = stream.read(1)[0]
            print(f"TRACE: {indent}  qualname at pos {qn_pos}: type=0x{qn_raw:02x}")
            trace_skip(stream)
        
        # firstlineno (int32)
        fl_pos = stream.tell()
        if stream.tell() + 4 <= len(data):
            fl = struct.unpack('<i', stream.read(4))[0]
            print(f"TRACE: {indent}  firstlineno at pos {fl_pos}: {fl}")
        else:
            print(f"TRACE: {indent}  firstlineno at pos {fl_pos}: OOB!")
        
        # lnotab
        ln_pos = stream.tell()
        ln_raw = stream.read(1)[0]
        ln_pure = ln_raw & ~0x80
        print(f"TRACE: {indent}  lnotab at pos {ln_pos}: type=0x{ln_raw:02x} (pure=0x{ln_pure:02x})")
        trace_skip(stream)
        
        # exceptiontable (3.11+ only)
        if True:
            et_pos = stream.tell()
            if et_pos < len(data):
                et_raw = stream.read(1)[0]
                print(f"TRACE: {indent}  exceptiontable at pos {et_pos}: type=0x{et_raw:02x}")
                trace_skip(stream)
        
        # After code object, go back past the qualname/firstlineno/etc we just read
        # Actually, we already consumed them - so no need to seek back
        
        print(f"TRACE: {indent}  --- end of code object at pos {stream.tell()} ---")
        
    elif pure_type in (0x73, 0x75, 0x61, 0x74):  # long strings
        l = struct.unpack('<i', stream.read(4))[0]
        data_s = stream.read(min(l, 40))
        if l > 40:
            stream.read(l - 40)
        print(f"TRACE: {indent}  long_str(len={l}) at {pos}")
    elif pure_type in (0x7a, 0x5a):  # short strings
        l = stream.read(1)[0]
        data_s = stream.read(l)
        print(f"TRACE: {indent}  short_str(len={l}) at {pos}: {data_s.decode('ascii', errors='replace')}")
    elif pure_type == 0x7c:  # TYPE_BYTES
        l = struct.unpack('<i', stream.read(4))[0]
        stream.read(min(l, 10))
        if l > 10: stream.read(l - 10)
        print(f"TRACE: {indent}  bytes(len={l}) at {pos}")
    elif pure_type == 0x6e:  # None
        print(f"TRACE: {indent}  None at {pos}")
    elif pure_type in (0x70, 0x71):  # True/False
        print(f"TRACE: {indent}  bool at {pos}")
    elif pure_type == 0x72:  # REF
        idx = struct.unpack('<i', stream.read(4))[0]
        print(f"TRACE: {indent}  REF[{idx}] at {pos}")
    else:
        print(f"TRACE: {indent}  UNKNOWN type=0x{pure_type:02x} at {pos}")
        # Try to skip
        try:
            l = struct.unpack('<i', stream.read(4))[0]
            stream.read(min(l, 4))
        except:
            pass

def trace_skip(stream):
    """Skip a marshal value"""
    pos = stream.tell()
    if pos >= len(data):
        return
    raw_type = stream.read(1)[0]
    pure_type = raw_type & ~0x80
    
    if pure_type in (0x73, 0x75, 0x61, 0x74, 0x7c):  # long strings/bytes
        l = struct.unpack('<i', stream.read(4))[0]
        stream.read(l)
    elif pure_type in (0x7a, 0x5a):  # short strings
        l = stream.read(1)[0]
        stream.read(l)
    elif pure_type in (0x28,):  # TUPLE
        n = struct.unpack('<i', stream.read(4))[0]
        for _ in range(n):
            trace_skip(stream)
    elif pure_type in (0x29,):  # SMALL_TUPLE
        n = stream.read(1)[0]
        for _ in range(n):
            trace_skip(stream)
    elif pure_type == 0x72:  # REF
        struct.unpack('<i', stream.read(4))[0]
    elif pure_type == 0x63:  # CODE (skip whole code object)
        trace(stream)
    elif pure_type == 0x6e:  # None
        pass
    elif pure_type in (0x70, 0x71):  # True/False
        pass
    elif pure_type == 0x69:  # int
        struct.unpack('<i', stream.read(4))[0]
    elif pure_type in (0x6c,):  # long
        struct.unpack('<q', stream.read(8))[0]
    else:
        pass  # Can't skip

stream = io.BytesIO(data)
try:
    trace(stream)
    print(f"\nFinal position: {stream.tell()} / {len(data)}")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"\nStopped at position {stream.tell()} due to: {e}")
