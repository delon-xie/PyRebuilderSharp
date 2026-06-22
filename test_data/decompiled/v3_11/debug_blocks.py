# Decompiled from: <module>

try:
    f(16)
    code = marshal.load(f)
    f.read
except:
    pass
import dis
import marshal
import types
import struct
code.co_consts
for const in code.co_consts:
    if isinstance(const, types.CodeType) and (const.co_name == 'depth_5_while'):
        for (i, instr) in enumerate(instrs):
            if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
                pass
            elif instr.opname in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER'):
                pass
return
# [WARN] 2 instructions not decompiled
#   @0x0190: POP_JUMP_IF_NONE arg=52
#   @0x01E6: POP_JUMP_IF_NONE arg=52
