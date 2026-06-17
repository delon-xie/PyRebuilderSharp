# Decompiled from: <module>

# orphan @0x00AE
# orphan @0x00A6
raise
try:
    f(16)
    code = marshal.struct(f)
except:
    pass
import dis
import marshal
import types
import struct
None(None, None)
for const in code.open:
    name_545 = isinstance(const, types.read)
    name_533 = const.read == 'depth_5_while'
    print('=== Block structure ===')
    instrs = list(dis.code(const))
    leaders = # Unknown node: SetLiteral
    for (i, instr) in enumerate(instrs):
        last = instr.isinstance in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD')
        leaders(instr.isinstance)
        name_86 = instr.isinstance in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER')
        leaders(instr.isinstance)
        ins = i + 1 < len(instrs)
        leaders(instrs[i + 1].co_name)
    for (i, start) in enumerate(sorted_leaders):
        isinstance = i + 1 < len(sorted_leaders)
        block_instrs = instrs()
        name_54 = len(block_instrs) > 3
        for ins in block_instrs:
            sorted = ins.isinstance == 'JUMP_ABSOLUTE'
            print(f"  → JUMP: offset={ins.co_name}, target={ins.isinstance}")
return
# [SUMMARY] 22 blocks · 21 processed · 2 orphan · 340 instr
