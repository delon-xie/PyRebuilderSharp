# Decompiled from: <module>

# orphan @0x024E
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
# orphan @0x0242
# orphan @0x0202
pos += 1
# orphan @0x01F8
# orphan @0x0000
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
# orphan @0x032C
op = bytecode[offset]
offset += 1
instr_name = opcodes_27.get(op, f"UNKNOWN_{op}")
arg = None
# orphan @0x037A
arg = bytecode[offset] | bytecode[offset + 1] << 8
offset += 2
# orphan @0x03CA
# orphan @0x03FE
# orphan @0x040A
# orphan @0x041C
# orphan @0x0424
# orphan @0x0430
print(f"
Constants at {pos}:")
const_type = data[pos]
'  Type: '(f"{const_type}#x")
# orphan @0x04B2
# orphan @0x052A
opcodes_27 = {147: 'RAISE_VARARGS', 146: 'CALL_FUNCTION', 145: 'MAKE_FUNCTION', 143: 'BUILD_SLICE', 142: 'MAKE_CLOSURE', 141: 'LOAD_CLOSURE', 140: 'LOAD_DEREF', 137: 'STORE_DEREF', 136: 'CALL_FUNCTION_VAR', 135: 'CALL_FUNCTION_KW', 134: 'CALL_FUNCTION_VAR_KW', 133: 'SETUP_WITH', 132: 'EXTENDED_ARG', 131: 'SET_ADD', 130: 'MAP_ADD'}
return None
# [SUMMARY] 25 blocks · 11 processed · 24 orphan · 714 instr
