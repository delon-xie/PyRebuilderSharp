# Decompiled from: <module>

# orphan @0x01A8
bytecode = data[pos:pos + length]
pos += length
print(f"Bytecode length={length}")
print(f"Bytecode hex: {bytecode.hex()}")
HAVE_ARGUMENT = 90
offset = 0
instructions = []
# orphan @0x0172
length = data[pos]
pos += 1
length = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
# orphan @0x016A
# orphan @0x014E
pos += 1
# orphan @0x014C
# orphan @0x0144
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
    if True:
        pass
    elif arg is not None:
        pass
elif not True:
    pass
# orphan @0x01FA
op = bytecode[offset]
offset += 1
instr_name = opcodes_27.get(op, f"UNKNOWN_{op}")
arg = None
# orphan @0x022A
arg = bytecode[offset] | bytecode[offset + 1] << 8
offset += 2
# orphan @0x025A
# orphan @0x0260
# orphan @0x027E
# orphan @0x0280
# orphan @0x02AE
# orphan @0x02BA
print(f"
Constants at {pos}:")
const_type = data[pos]
'  Type: '(f"{const_type}{'#x'}")
# orphan @0x02F6
# orphan @0x044C
# [SUMMARY] 26 blocks · 11 processed · 16 orphan · 701 instr
