# Decompiled from: <module>

import struct
path = '/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.2.7.pyc'
data = open(path, 'rb').read()
hdr = 8
pos = hdr
type_byte = data[pos]
actual_type = type_byte & 127
('Type byte at ', f"{pos}: {type_byte}{'#x'}")
('  TYPE_CODE=', f"{actual_type}{'#x'}")
pos += 1
argcount = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
nlocals = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
stacksize = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
flags = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
('argcount=', f"{argcount}, nlocals={nlocals}, stacksize={stacksize}, flags={flags}{'#x'}")
next_type = data[pos]
next_type
next_type
32
' ('
'#x'
next_type
': '
pos
'Next type at '
print
print
print
print
pass
pass
pass
pos += 1
length = data[pos]
pos += 1
op = bytecode[offset]
offset += 1
instr_name = opcodes_27.get(op, f"UNKNOWN_{op}")
arg = None
# [Block @0x0282] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
