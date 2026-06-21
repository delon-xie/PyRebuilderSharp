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
if next_type <= next_type:
    pass
elif arg is not None:
    pass
# orphan @0x0150
'?'
# orphan @0x018A
length = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
# orphan @0x01AE
bytecode = data[pos:pos + length]
pos += length
print(f"Bytecode length={length}")
print(f"Bytecode hex: {bytecode.hex()}")
HAVE_ARGUMENT = 90
offset = 0
instructions = []
# orphan @0x0230
arg = bytecode[offset] | bytecode[offset + 1] << 8
offset += 2
# orphan @0x0264
1
# orphan @0x02AA
''
# orphan @0x02B8
print(f"
Constants at {pos}:")
const_type = data[pos]
'  Type: '(f"{const_type}{'#x'}")
print
# orphan @0x02E0
opcodes_27 = {147: 'POP_TOP', 146: 'ROT_TWO', 145: 'ROT_THREE', 143: 'DUP_TOP', 142: 'ROT_FOUR', 141: 'NOP', 140: 'UNARY_POSITIVE', 137: 'UNARY_NEGATIVE', 136: 'UNARY_NOT', 135: 'UNARY_INVERT', 134: 'BINARY_POWER', 133: 'BINARY_MULTIPLY', 132: 'BINARY_DIVIDE', 131: 'BINARY_MODULO', 130: 'BINARY_ADD', 126: 'BINARY_SUBTRACT', 125: 'BINARY_SUBSCR', 124: 'BINARY_FLOOR_DIVIDE', 122: 'BINARY_TRUE_DIVIDE', 121: 'INPLACE_FLOOR_DIVIDE', 120: 'INPLACE_TRUE_DIVIDE', 119: 'SLICE+0', 116: 'SLICE+1', 115: 'SLICE+2', 114: 'SLICE+3', 113: 'STORE_SLICE+0', 112: 'STORE_SLICE+1', 111: 'STORE_SLICE+2', 110: 'STORE_SLICE+3', 109: 'DELETE_SLICE+0', 108: 'DELETE_SLICE+1', 107: 'DELETE_SLICE+2', 106: 'DELETE_SLICE+3', 105: 'STORE_MAP', 104: 'INPLACE_ADD', 103: 'INPLACE_SUBTRACT', 102: 'INPLACE_MULTIPLY', 101: 'INPLACE_DIVIDE', 100: 'INPLACE_MODULO', 99: 'STORE_SUBSCR', 98: 'DELETE_SUBSCR', 97: 'BINARY_LSHIFT', 96: 'BINARY_RSHIFT', 95: 'BINARY_AND', 94: 'BINARY_XOR', 93: 'BINARY_OR', 92: 'INPLACE_POWER', 91: 'GET_ITER', 90: 'PRINT_EXPR', 89: 'PRINT_ITEM', 88: 'PRINT_NEWLINE', 87: 'PRINT_ITEM_TO', 86: 'PRINT_NEWLINE_TO', 85: 'INPLACE_LSHIFT', 84: 'INPLACE_RSHIFT', 83: 'INPLACE_AND', 82: 'INPLACE_XOR', 81: 'INPLACE_OR', 80: 'BREAK_LOOP', 79: 'WITH_CLEANUP', 78: 'LOAD_LOCALS', 77: 'RETURN_VALUE', 76: 'IMPORT_STAR', 75: 'EXEC_STMT', 74: 'YIELD_VALUE', 73: 'POP_BLOCK', 72: 'END_FINALLY', 71: 'BUILD_CLASS', 70: 'STORE_NAME', 68: 'DELETE_NAME', 67: 'UNPACK_SEQUENCE', 66: 'FOR_ITER', 65: 'LIST_APPEND', 64: 'STORE_ATTR', 63: 'DELETE_ATTR', 62: 'STORE_GLOBAL', 61: 'DELETE_GLOBAL', 60: 'DUP_TOPX', 59: 'LOAD_CONST', 58: 'LOAD_NAME', 57: 'BUILD_TUPLE', 56: 'BUILD_LIST', 55: 'BUILD_SET', 54: 'BUILD_MAP', 53: 'LOAD_ATTR', 52: 'COMPARE_OP', 51: 'IMPORT_NAME', 50: 'IMPORT_FROM', 43: 'JUMP_FORWARD', 42: 'JUMP_IF_TRUE_OR_POP', 41: 'JUMP_IF_FALSE_OR_POP', 40: 'JUMP_ABSOLUTE', 33: 'POP_JUMP_IF_FALSE', 32: 'POP_JUMP_IF_TRUE', 31: 'LOAD_GLOBAL', 30: 'CONTINUE_LOOP', 29: 'SETUP_LOOP', 28: 'SETUP_EXCEPT', 27: 'SETUP_FINALLY', 26: 'LOAD_FAST', 25: 'STORE_FAST', 24: 'DELETE_FAST', 23: 'RAISE_VARARGS', 22: 'CALL_FUNCTION', 21: 'MAKE_FUNCTION', 20: 'BUILD_SLICE', 19: 'MAKE_CLOSURE', 15: 'LOAD_CLOSURE', 12: 'LOAD_DEREF', 11: 'STORE_DEREF', 10: 'CALL_FUNCTION_VAR', 9: 'CALL_FUNCTION_KW', 5: 'CALL_FUNCTION_VAR_KW', 4: 'SETUP_WITH', 3: 'EXTENDED_ARG', 2: 'SET_ADD', 1: 'MAP_ADD'}
# [SUMMARY] 26 blocks · 18 processed · 21 orphan · 480 instr
