# Decompiled from: <module>

(None, None)
for const in code.co_consts:
    pass
    if isinstance(const, types.CodeType):
        pass
        if const.co_name == 'depth_5_while':
            for (i, instr) in enumerate(instrs):
                pass
                if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
                    pass
                else:
                    for (i, start) in enumerate(sorted_leaders):
                        pass
                        if i + 1 < len(sorted_leaders):
                            pass
                        else:
                            for ins in block_instrs:
                                pass
                                if ins.opname == 'JUMP_ABSOLUTE':
                                    print(f"  → JUMP: offset={ins.offset}, target={ins.arg}")
                        pass
                pass
                leaders.add(instr.arg)
    None
# [WARN] 1 instructions not decompiled
#   @0x0190: POP_JUMP_IF_NONE arg=52
