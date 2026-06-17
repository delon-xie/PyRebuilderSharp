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
None
struct.unpack
print
print
while print <= print:
    for (off, op, name, arg) in print <= print:
        '4d'
        off
        '  '
        None
        print
        '20s'
        name
        ': '
        ''
        arg
        ' '
        break
        'STORE_MAP'
        54
        'DELETE_SLICE+3'
        53
        'DELETE_SLICE+2'
        52
        'DELETE_SLICE+1'
        51
        'DELETE_SLICE+0'
        50
        'STORE_SLICE+3'
        43
        'STORE_SLICE+2'
        42
        'STORE_SLICE+1'
        41
        'STORE_SLICE+0'
        40
        'SLICE+3'
        33
        'SLICE+2'
        32
        'SLICE+1'
        31
        'SLICE+0'
        30
        'INPLACE_TRUE_DIVIDE'
        29
        'INPLACE_FLOOR_DIVIDE'
        28
        'BINARY_TRUE_DIVIDE'
        27
        'BINARY_FLOOR_DIVIDE'
        26
        {}
        'BINARY_SUBSCR'
        25
        'BINARY_SUBTRACT'
        24
        'BINARY_ADD'
        23
        'BINARY_MODULO'
        22
        opcodes_27 = {130: 'RAISE_VARARGS', 131: 'CALL_FUNCTION', 132: 'MAKE_FUNCTION', 133: 'BUILD_SLICE', 134: 'MAKE_CLOSURE', 135: 'LOAD_CLOSURE', 136: 'LOAD_DEREF', 137: 'STORE_DEREF', 140: 'CALL_FUNCTION_VAR', 141: 'CALL_FUNCTION_KW', 142: 'CALL_FUNCTION_VAR_KW', 143: 'SETUP_WITH', 145: 'EXTENDED_ARG', 146: 'SET_ADD', 147: 'MAP_ADD'}
        return None
pos += 1
if (next_type in (115, 116, 122)) and (next_type == 122):
    length = data[pos]
    pos += 1
    length = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
    bytecode = data[pos:pos + length]
    pos += length
    print(f"Bytecode length={length}")
    print(f"Bytecode hex: {bytecode.hex()}")
    HAVE_ARGUMENT = 90
    offset = 0
    instructions = []
    if offset < len(bytecode):
        op = bytecode[offset]
        offset += 1
        instr_name = opcodes_27.get(op, f"UNKNOWN_{op}")
        arg = None
        if op >= HAVE_ARGUMENT:
            arg = bytecode[offset] | bytecode[offset + 1] << 8
            offset += 2
            if op >= HAVE_ARGUMENT:
                pass
# [WARN] 1 instructions not decompiled
#   @0x04FC: JUMP_BACKWARD arg=988
# [SUMMARY] 25 blocks · 26 processed · 6 orphan · 722 instr
