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
    while offset < len(bytecode):
        for (off, op, name, arg) in instructions:
            break
        print(f"
Constants at {pos}:")
        const_type = data[pos]
        break
    op = bytecode[offset]
    offset += 1
    instr_name = opcodes_27.get(op, f"UNKNOWN_{op}")
    arg = None
    if op >= HAVE_ARGUMENT:
        arg = bytecode[offset] | bytecode[offset + 1] << 8
    elif op >= HAVE_ARGUMENT:
        pass
# [WARN] 1 instructions not decompiled
#   @0x04FC: JUMP_BACKWARD arg=292
# [SUMMARY] 25 blocks · 26 processed · 0 orphan · 730 instr
