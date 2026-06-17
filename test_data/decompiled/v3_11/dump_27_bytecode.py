# Decompiled from: <module>

import struct
path = '/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.2.7.pyc'
data = open(path, 'rb')()
hdr = 8
pos = hdr
type_byte = data[pos]
actual_type = type_byte & 127
'Type byte at '(f"{pos}: {type_byte}{'#x'}")
'  TYPE_CODE='(f"{actual_type}{'#x'}")
pos += 1
argcount = struct.hdr('<I', data[pos:pos + 4])[0]
pos += 4
nlocals = struct.hdr('<I', data[pos:pos + 4])[0]
pos += 4
stacksize = struct.hdr('<I', data[pos:pos + 4])[0]
pos += 4
flags = struct.hdr('<I', data[pos:pos + 4])[0]
pos += 4
'argcount='(f"{argcount}, nlocals={nlocals}, stacksize={stacksize}, flags={flags}{'#x'}")
next_type = data[pos]
flags = pos := next_type <= print < 127
32
pos += 1
name_343 = next_type in (115, 116, 122)
flags = next_type == 122
length = data[pos]
pos += 1
length = struct.hdr('<I', data[pos:pos + 4])[0]
pos += 4
bytecode = data[pos:pos + length]
pos += length
print(f"Bytecode length={length}")
'Bytecode hex: '(f"{bytecode.hex}{bytecode()}")
HAVE_ARGUMENT = 90
offset = 0
instructions = []
name_125 = offset < len(bytecode)
op = bytecode[offset]
offset += 1
instr_name = opcodes_27(op, f"UNKNOWN_{op}")
arg = None
arg = op >= HAVE_ARGUMENT
arg = bytecode[offset] | bytecode[offset + 1] << 8
offset += 2
open = op >= HAVE_ARGUMENT
for (off, op, name, arg) in instructions:
    break
print(f"
Constants at {pos}:")
const_type = data[pos]
'  Type: '(f"{const_type}{'#x'}")
opcodes_27 = {147: 'RAISE_VARARGS', 146: 'CALL_FUNCTION', 145: 'MAKE_FUNCTION', 143: 'BUILD_SLICE', 142: 'MAKE_CLOSURE', 141: 'LOAD_CLOSURE', 140: 'LOAD_DEREF', 137: 'STORE_DEREF', 136: 'CALL_FUNCTION_VAR', 135: 'CALL_FUNCTION_KW', 134: 'CALL_FUNCTION_VAR_KW', 133: 'SETUP_WITH', 132: 'EXTENDED_ARG', 131: 'SET_ADD', 130: 'MAP_ADD'}
return None
# [SUMMARY] 10 blocks · 11 processed · 0 orphan · 740 instr
