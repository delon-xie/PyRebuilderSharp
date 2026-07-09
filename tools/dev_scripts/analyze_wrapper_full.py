import marshal

def read_varint(data, offset):
    result = 0
    shift = 0
    while True:
        b = data[offset]
        result |= (b & 0x3f) << shift
        offset += 1
        if not (b & 0x40):
            break
        shift += 6
    return result, offset

with open('test_data/compiled/reprlib.3.11.pyc', 'rb') as f:
    f.read(16)
    code = marshal.load(f)

def find_func(code, name):
    for c in code.co_consts:
        if hasattr(c, 'co_name') and c.co_name == name:
            return c
    return None

recursive_repr = find_func(code, 'recursive_repr')
decorating_function = find_func(recursive_repr, 'decorating_function')
wrapper = find_func(decorating_function, 'wrapper')

print(f"=== wrapper function ===")
print(f"Name: {wrapper.co_name}")
print(f"Locals: {wrapper.co_varnames}")
print(f"Names: {wrapper.co_names}")
print(f"Code length: {len(wrapper.co_code)} bytes")

print(f"\n=== Exception Table ===")
et_data = wrapper.co_exceptiontable
offset = 0
entry_num = 0
while offset < len(et_data):
    start, offset = read_varint(et_data, offset)
    size, offset = read_varint(et_data, offset)
    target, offset = read_varint(et_data, offset)
    depth_lasti, offset = read_varint(et_data, offset)
    end = start + size
    depth = depth_lasti >> 1
    lasti = (depth_lasti & 1) != 0
    print(f"  Entry {entry_num}: start={start*2}, end={end*2}, target={target*2}, depth={depth}, lasti={lasti}")
    entry_num += 1

print(f"\n=== Instructions (all) ===")
code_bytes = wrapper.co_code
opnames = {
    90: 'NOP', 91: 'POP_TOP', 92: 'ROT_TWO', 93: 'ROT_THREE', 94: 'DUP_TOP',
    100: 'BINARY_POWER', 101: 'BINARY_MULTIPLY', 102: 'BINARY_MODULO',
    104: 'BINARY_ADD', 105: 'BINARY_SUBTRACT', 106: 'BINARY_SUBSCR',
    110: 'BINARY_FLOOR_DIVIDE', 111: 'BINARY_TRUE_DIVIDE',
    113: 'INPLACE_FLOOR_DIVIDE', 114: 'INPLACE_TRUE_DIVIDE',
    116: 'GET_AITER', 117: 'GET_ANEXT', 118: 'BEFORE_ASYNC_WITH',
    124: 'LOAD_CONST', 125: 'LOAD_NAME', 126: 'BUILD_TUPLE',
    127: 'BUILD_LIST', 128: 'BUILD_SET', 129: 'BUILD_MAP',
    130: 'LOAD_ATTR', 131: 'COMPARE_OP', 132: 'IMPORT_NAME',
    133: 'IMPORT_FROM', 134: 'JUMP_FORWARD', 135: 'JUMP_IF_FALSE_OR_POP',
    136: 'JUMP_IF_TRUE_OR_POP', 137: 'JUMP_ABSOLUTE', 138: 'POP_JUMP_IF_FALSE',
    139: 'POP_JUMP_IF_TRUE', 140: 'LOAD_GLOBAL',
    141: 'RETURN_VALUE', 142: 'EXEC_STMT', 143: 'YIELD_VALUE',
    144: 'POP_BLOCK', 145: 'END_FINALLY', 146: 'BUILD_CLASS',
    147: 'STORE_NAME', 148: 'DELETE_NAME', 149: 'UNPACK_SEQUENCE',
    150: 'FOR_ITER', 151: 'LIST_APPEND', 152: 'STORE_ATTR',
    153: 'DELETE_ATTR', 154: 'STORE_GLOBAL', 155: 'DELETE_GLOBAL',
    156: 'DUP_TOPX', 157: 'LOAD_CONST', 158: 'EXECUTE_STMT',
    160: 'RAISE_VARARGS', 161: 'CALL_FUNCTION', 162: 'MAKE_FUNCTION',
    163: 'BUILD_SLICE', 164: 'EXTENDED_ARG', 165: 'CALL_FUNCTION_KW',
    166: 'CALL_FUNCTION_EX', 167: 'SETUP_WITH',
    170: 'LIST_EXTEND', 171: 'SET_UPDATE', 172: 'DICT_MERGE', 173: 'DICT_UPDATE',
    174: 'LOAD_CLOSURE', 175: 'LOAD_DEREF', 176: 'STORE_DEREF',
    180: 'DELETE_DEREF',
    183: 'SETUP_ANNOTATIONS',
    185: 'LOAD_LOCALS',
    190: 'LOAD_FAST', 191: 'STORE_FAST', 192: 'DELETE_FAST',
    200: 'LOAD_GLOBAL',
    201: 'BREAK_LOOP', 202: 'CONTINUE_LOOP',
    204: 'SETUP_LOOP', 205: 'SETUP_EXCEPT', 206: 'SETUP_FINALLY',
    207: 'SETUP_WITH',
    208: 'POP_EXCEPT',
    209: 'END_FINALLY',
    210: 'CALL_FINALLY',
    211: 'POP_FINALLY',
    220: 'LOAD_METHOD',
    221: 'CALL_METHOD',
    222: 'LIST_TO_TUPLE',
    223: 'IS_OP',
    224: 'CONTAINS_OP',
    225: 'JUMP_IF_NOT_EXC_MATCH',
    226: 'CHECK_EXC_MATCH',
    227: 'CHECK_EG_MATCH',
    228: 'COPY',
    229: 'BINARY_OP',
    230: 'SEND',
    231: 'ASYNC_GEN_WRAP',
    232: 'LIST_APPEND',
    233: 'SET_ADD',
    234: 'MAP_ADD',
    235: 'LOAD_ASSERTION_ERROR',
    236: 'FORMAT_VALUE',
    237: 'BUILD_CONST_KEY_MAP',
    238: 'BUILD_STRING',
    239: 'LOAD_FAST',
    240: 'STORE_FAST',
    241: 'DELETE_FAST',
    242: 'LOAD_GLOBAL',
    243: 'MATCH_MAPPING',
    244: 'MATCH_KEYS',
    245: 'MATCH_SEQUENCE',
    246: 'MATCH_CLASS',
    247: 'MATCH_STAR',
    248: 'MATCH_AS',
    249: 'MATCH_OR',
    250: 'MATCH_NOT',
    251: 'MATCH_COPY',
    252: 'MATCH_EXCEPT',
    253: 'POP_JUMP_IF_NONE',
    254: 'POP_JUMP_IF_NOT_NONE',
}

i = 0
while i < len(code_bytes):
    op = code_bytes[i]
    opname = opnames.get(op, f'UNKNOWN({op})')
    if op >= 90:
        arg = code_bytes[i+1]
        print(f"  {i:04d}: {opname:20s} arg={arg}")
        i += 2
    else:
        print(f"  {i:04d}: {opname:20s}")
        i += 1