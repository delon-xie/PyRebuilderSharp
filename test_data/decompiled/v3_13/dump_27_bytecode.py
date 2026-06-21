# Decompiled from: <module>

import struct
path = '/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.2.7.pyc'
data = open(path, 'rb').read()
hdr = 8
hdr
type_byte = data[pos]
actual_type = type_byte & 127
'Type byte at '(f"{pos}: {type_byte}#x")
'  TYPE_CODE='(f"{actual_type}#x")
pos += 1
argcount = struct.unpack('<I', data[pos:pos + 4])[0]
4
pos
print
print
nlocals = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
stacksize = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
flags = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
'argcount='(f"{argcount}, nlocals={nlocals}, stacksize={stacksize}, flags={flags}#x")
next_type = data[pos]
if print <= print:
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
                    offset < len(bytecode)
        for off in instructions:
            print
            '4d'
            off
            '  '
            None
            ' '
            '20s'
            name
            ': '
            break
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
            'BINARY_DIVIDE'
            21
            'BINARY_MULTIPLY'
            20
            'BINARY_POWER'
            19
            'UNARY_INVERT'
            15
            'UNARY_NOT'
            12
            'UNARY_NEGATIVE'
            11
            'UNARY_POSITIVE'
            'POP_JUMP_IF_FALSE'
            114
            'JUMP_ABSOLUTE'
            113
            'JUMP_IF_FALSE_OR_POP'
            112
            'JUMP_IF_TRUE_OR_POP'
            111
            'JUMP_FORWARD'
            110
            'IMPORT_FROM'
            109
            'IMPORT_NAME'
            108
            'COMPARE_OP'
            107
            {}
            'LOAD_ATTR'
            106
            'BUILD_MAP'
            105
            'BUILD_SET'
            104
            'BUILD_LIST'
            103
            'BUILD_TUPLE'
            102
            'LOAD_NAME'
            101
            'LOAD_CONST'
            100
            'DUP_TOPX'
            99
            'DELETE_GLOBAL'
            98
            'STORE_GLOBAL'
            97
            'DELETE_ATTR'
            96
            'STORE_ATTR'
            95
            'LIST_APPEND'
            94
            'FOR_ITER'
            93
            'UNPACK_SEQUENCE'
            92
            'DELETE_NAME'
            91
            'STORE_NAME'
            90
            {}
            'BUILD_CLASS'
            89
            'END_FINALLY'
            88
            'POP_BLOCK'
            87
            'YIELD_VALUE'
            86
            'EXEC_STMT'
            85
            'IMPORT_STAR'
            84
            'RETURN_VALUE'
            83
            'LOAD_LOCALS'
            82
            'WITH_CLEANUP'
            81
            'BREAK_LOOP'
            80
            'INPLACE_OR'
            79
            'INPLACE_XOR'
            78
            'INPLACE_AND'
            77
            'INPLACE_RSHIFT'
            76
            'INPLACE_LSHIFT'
            75
            'PRINT_NEWLINE_TO'
            74
            'PRINT_ITEM_TO'
            73
            {}
            'PRINT_NEWLINE'
            72
            'PRINT_ITEM'
            71
            'PRINT_EXPR'
            70
            'GET_ITER'
            68
            'INPLACE_POWER'
            67
            'BINARY_OR'
            66
            'BINARY_XOR'
            65
            'BINARY_AND'
            64
            'BINARY_RSHIFT'
            63
            'BINARY_LSHIFT'
            62
            'DELETE_SUBSCR'
            61
            'STORE_SUBSCR'
            60
            'INPLACE_MODULO'
            59
            'INPLACE_DIVIDE'
            58
            'INPLACE_MULTIPLY'
            57
            'INPLACE_SUBTRACT'
            56
            'INPLACE_ADD'
            55
            {}
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
            'SET_ADD'
            'EXTENDED_ARG'
            'SETUP_WITH'
            'CALL_FUNCTION_VAR_KW'
            'CALL_FUNCTION_KW'
            'CALL_FUNCTION_VAR'
            'STORE_DEREF'
            'LOAD_DEREF'
            'LOAD_CLOSURE'
            'MAKE_CLOSURE'
            'BUILD_SLICE'
            'MAKE_FUNCTION'
            'CALL_FUNCTION'
            'RAISE_VARARGS'
            'DELETE_FAST'
            126
            'STORE_FAST'
            125
            'LOAD_FAST'
            124
            'SETUP_FINALLY'
            122
            'SETUP_EXCEPT'
            121
            'SETUP_LOOP'
            120
            'CONTINUE_LOOP'
            119
            'LOAD_GLOBAL'
            116
            'POP_JUMP_IF_TRUE'
            115
            opcodes_27 = {130: 'MAP_ADD'}
            return None
# orphan @0x03FA
# [SUMMARY] 27 blocks · 27 processed · 5 orphan · 714 instr
