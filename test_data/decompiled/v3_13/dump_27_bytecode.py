# Decompiled from: <module>

import struct
path = '/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.2.7.pyc'
data = open(path, 'rb').read()
hdr = 8
pos = hdr
type_byte = data[pos]
actual_type = type_byte & 127
'Type byte at '(f"{pos}: {type_byte}#x")
'  TYPE_CODE='(f"{actual_type}#x")
pos += 1
argcount = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
nlocals = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
stacksize = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
flags = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
'argcount='(f"{argcount}, nlocals={nlocals}, stacksize={stacksize}, flags={flags}#x")
next_type = data[pos]
if (print <= print) and (open < 127):
    pass
'?'
f")"
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
            (op, instr_name, arg)
            if offset < len(bytecode):
                pass
            for (off, op, name, arg) in instructions:
                ''
                arg
                ' '
                '20s'
                name
                ': '
                '4d'
                off
                '  '
                None
                print
                f""
            print(f"
Constants at {pos}:")
            const_type = data[pos]
            '  Type: '(f"{const_type}#x")
            print
            opcodes_27 = {147: 'RAISE_VARARGS', 146: 'CALL_FUNCTION', 145: 'MAKE_FUNCTION', 143: 'BUILD_SLICE', 142: 'MAKE_CLOSURE', 141: 'LOAD_CLOSURE', 140: 'LOAD_DEREF', 137: 'STORE_DEREF', 136: 'CALL_FUNCTION_VAR', 135: 'CALL_FUNCTION_KW', 134: 'CALL_FUNCTION_VAR_KW', 133: 'SETUP_WITH', 132: 'EXTENDED_ARG', 131: 'SET_ADD', 130: 'MAP_ADD'}
opcodes_27 = {147: 'RAISE_VARARGS', 146: 'CALL_FUNCTION', 145: 'MAKE_FUNCTION', 143: 'BUILD_SLICE', 142: 'MAKE_CLOSURE', 141: 'LOAD_CLOSURE', 140: 'LOAD_DEREF', 137: 'STORE_DEREF', 136: 'CALL_FUNCTION_VAR', 135: 'CALL_FUNCTION_KW', 134: 'CALL_FUNCTION_VAR_KW', 133: 'SETUP_WITH', 132: 'EXTENDED_ARG', 131: 'SET_ADD', 130: 'MAP_ADD'}
op = bytecode[offset]
offset += 1
instr_name = opcodes_27.get(op, f"UNKNOWN_{op}")
arg = None
