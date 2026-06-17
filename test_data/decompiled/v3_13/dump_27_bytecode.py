# Decompiled from: <module>

# orphan @0x0218
# orphan @0x0208
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
if (print <= print) and True:
    pass
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
while offset < len(bytecode):
    pass
for (off, op, name, arg) in instructions:
    break
break
break
# orphan @0x032C
op = bytecode[offset]
offset += 1
instr_name = opcodes_27.get(op, f"UNKNOWN_{op}")
arg = None
# orphan @0x037A
arg = bytecode[offset] | bytecode[offset + 1] << 8
# orphan @0x03A4
# orphan @0x03CA
# orphan @0x03CC
# orphan @0x03D0
# orphan @0x03FE
# [SUMMARY] 25 blocks · 17 processed · 10 orphan · 714 instr
