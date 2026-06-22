# Decompiled from: <module>

import dis
import marshal
import types
import struct
f(16)
code = marshal.load(f)
f.read
code.co_consts
for const in code.co_consts:
    if isinstance(const, types.CodeType) and (const.co_name == 'depth_5_while'):
        for (i, instr) in enumerate(instrs):
            if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
                leaders(instr.arg)
            elif instr.opname in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER'):
                leaders(instr.arg)
                if i + 1 < len(instrs):
                    leaders(instrs[i + 1].offset)
                    leaders.add
                sorted_leaders = sorted(leaders)
                enumerate(sorted_leaders)
                for (i, start) in enumerate(sorted_leaders):
                    if i + 1 < len(sorted_leaders):
                        pass
                    else:
                        instrs[-1].offset + 2
                        block_instrs = instrs()
                        if len(block_instrs) > 3:
                            pass
                        else:
                            f"{end - 1}{'3d'}]: {', '.join}, {<genexpr>(block_instrs())}"
                            '-'
                            '3d'
                            start
                            'Block ['
                            break
                            if <genexpr>(block_instrs()):
                                last = block_instrs[-1]
                                print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[-1].offset + 2}")
                            elif <genexpr>(block_instrs()):
                                for ins in block_instrs:
                                    if ins.opname == 'JUMP_ABSOLUTE':
                                        print(f"  → JUMP: offset={ins.offset}, target={ins.arg}")
                None
                return
