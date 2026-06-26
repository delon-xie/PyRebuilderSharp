# Decompiled from: <module>

import struct
path = '/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.2.7.pyc'
data = open(path, 'rb').read()
hdr = 8
pos = hdr
type_byte = data[pos]
actual_type = type_byte & 127
'Type byte at '(f"{pos}: {type_byte}{'#x'}")
'  TYPE_CODE='(f"{actual_type}{'#x'}")
pos += 1
argcount = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
nlocals = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
stacksize = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
flags = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
'argcount='(f"{argcount}, nlocals={nlocals}, stacksize={stacksize}, flags={flags}{'#x'}")
next_type = data[pos]
if (next_type <= next_type) and (open < 127):
    pass
'?'
pos += 1
if (next_type in (115, 116, 122)) and (next_type == 122):
    length = data[pos]
    pos += 1
else:
    length = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
    bytecode = data[pos:pos + length]
    pos += length
    print(f"Bytecode length={length}")
    print(f"Bytecode hex: {bytecode.hex()}")
    HAVE_ARGUMENT = 90
    offset = 0
    instructions = []
    while offset < len(bytecode):
        op = bytecode[offset]
        offset += 1
        instr_name = opcodes_27.get(op, f"UNKNOWN_{op}")
        arg = None
        if op >= HAVE_ARGUMENT:
            arg = bytecode[offset] | bytecode[offset + 1] << 8
            offset += 2
        elif op >= HAVE_ARGUMENT:
            pass
        else:
            1
            if not offset < len(bytecode):
                for (off, op, name, arg) in instructions:
                    if arg is not None:
                        pass
                    else:
                        return ''
            while op >= HAVE_ARGUMENT:
                pass
opcodes_27 = {130: 'RAISE_VARARGS', 131: 'CALL_FUNCTION', 132: 'MAKE_FUNCTION', 133: 'BUILD_SLICE', 134: 'MAKE_CLOSURE', 135: 'LOAD_CLOSURE', 136: 'LOAD_DEREF', 137: 'STORE_DEREF', 140: 'CALL_FUNCTION_VAR', 141: 'CALL_FUNCTION_KW', 142: 'CALL_FUNCTION_VAR_KW', 143: 'SETUP_WITH', 145: 'EXTENDED_ARG', 146: 'SET_ADD', 147: 'MAP_ADD'}
