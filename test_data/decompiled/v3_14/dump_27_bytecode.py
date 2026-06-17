# Decompiled from: <module>

# orphan @0x0284
pos += 1
# orphan @0x0278
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
while True:
    pass
# orphan @0x02CE
# orphan @0x02DC
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
# orphan @0x03F4
op = bytecode[offset]
offset += 1
instr_name = opcodes_27.get(op, f"UNKNOWN_{op}")
arg = None
# orphan @0x0454
arg = bytecode[offset] | bytecode[offset + 1] << 8
offset += 2
# orphan @0x04D6
# orphan @0x0500
# orphan @0x0508
# orphan @0x0512
# orphan @0x0522
# orphan @0x052C
# orphan @0x0538
print(f"
Constants at {pos}:")
const_type = data[pos]
'  Type: '(f"{const_type}#x")
# orphan @0x060C
# orphan @0x06C8
opcodes_27 = {130: 'RAISE_VARARGS', 131: 'CALL_FUNCTION', 132: 'MAKE_FUNCTION', 133: 'BUILD_SLICE', 134: 'MAKE_CLOSURE', 135: 'LOAD_CLOSURE', 136: 'LOAD_DEREF', 137: 'STORE_DEREF', 140: 'CALL_FUNCTION_VAR', 141: 'CALL_FUNCTION_KW', 142: 'CALL_FUNCTION_VAR_KW', 143: 'SETUP_WITH', 145: 'EXTENDED_ARG', 146: 'SET_ADD', 147: 'MAP_ADD'}
return None
# [SUMMARY] 25 blocks · 10 processed · 24 orphan · 730 instr
