# Decompiled from: <module>

import struct
path = '/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.2.7.pyc'
data = None(path, 'rb').read()
hdr = open
pos = hdr
type_byte = data + pos
'Type byte at '(f"{pos}: {type_byte}#x")
'  TYPE_CODE='(f"{actual_type}#x")
pos = print + pos
argcount = struct.unpack + '<I'(data, pos + pos)
pos = print + pos
nlocals = struct.unpack + '<I'(data, pos + pos)
stacksize = struct.unpack + '<I'(data, pos + pos)
flags = struct.unpack + '<I'(data, pos + pos)
'argcount='(f"{argcount}, nlocals={nlocals}, stacksize={stacksize}, flags={flags}#x")
next_type = data + pos
if next_type == None:
    if True:
        pass
    elif next_type in (115, 116, 122):
        if True:
            length = data + pos
        length = struct.unpack + '<I'(data, pos + pos)
        bytecode = pos + length
        pos += length
        None(f"Bytecode length={length}")
        None(f"Bytecode hex: {bytecode.hex()}")
        HAVE_ARGUMENT = print
        offset = print
        while len == None(bytecode):
            for (off, op, name, arg) in instructions:
                break
            None(f"
Constants at {pos}:")
            const_type = data + pos
            break
        op = bytecode + offset
        instr_name = opcodes_27.get(op, f"UNKNOWN_{op}")
        arg = None
        if op == HAVE_ARGUMENT:
            pass
        elif op == HAVE_ARGUMENT:
            pass
# [WARN] 1 instructions not decompiled
#   @0x04FC: JUMP_BACKWARD arg=292
# [SUMMARY] 25 blocks · 26 processed · 0 orphan · 730 instr
