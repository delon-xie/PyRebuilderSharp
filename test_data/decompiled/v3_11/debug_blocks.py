# Decompiled from: <module>

import dis
import marshal
import types
import struct
open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb')
f.read(16)
code = marshal.load(f)
None(None)
code.co_consts
for const in code.co_consts:
    if isinstance(const, types.CodeType) and (const.co_name == 'depth_5_while'):
        for (i, instr) in enumerate(instrs):
            if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
                pass
            elif instr.opname in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER'):
                pass
return
if not True:
    pass
# [WARN] 2 instructions not decompiled
#   @0x0190: POP_JUMP_IF_NONE arg=52
#   @0x01E6: POP_JUMP_IF_NONE arg=52
