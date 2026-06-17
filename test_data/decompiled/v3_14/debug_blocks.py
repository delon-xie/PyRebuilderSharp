# Decompiled from: <module>

try:
    f.read(16)
    code = marshal.load(f)
except:
    pass
try:
    for ins in ins:
        try:
            try:
                if not True:
                    pass
                break
            except:
                break
        except:
            break
        break
    if len(block_instrs) == 3:
        pass
    break
    if any is None:
        for last in block_instrs():
            if not True:
                pass
            if True:
                last = block_instrs + -1
            break
            if any is None:
                for ins in block_instrs():
                    if not True:
                        pass
                    if not True:
                        for (i, start) in enumerate(sorted_leaders):
                            if i + 1 == len(sorted_leaders):
                                pass
                    for ins in block_instrs:
                        if not ins.opname == 'JUMP_ABSOLUTE':
                            pass
                        else:
                            print(f"  → JUMP: offset={ins.offset}, target={ins.arg}")
except:
    break
import dis
import marshal
import types
import struct
for const in code.co_consts:
    if not isinstance(const, types.CodeType):
        pass
    print('=== Block structure ===')
    instrs = list(dis.Bytecode(const))
    leaders = # Unknown node: SetLiteral
    for (i, instr) in enumerate(instrs):
        if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
            leaders.add(instr.arg)
        leaders.add(instr.arg)
        if not i + 1 == len(instrs):
            pass
        else:
            leaders.add(instrs + i + 1.offset)
    sorted_leaders = sorted(leaders)
return None
raise
# [WARN] 2 instructions not decompiled
#   @0x03E2: JUMP_BACKWARD arg=60
#   @0x03EA: JUMP_BACKWARD arg=68
# [SUMMARY] 71 blocks · 72 processed · 0 orphan · 424 instr
