# Decompiled from: <module>

import dis
import marshal
import types
import struct
with open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb') as f:
    f.read(16)
    code = marshal.load(f)
    for const in const.co_name == 'depth_5_while':
        if isinstance(const, types.CodeType) and (const.co_name == 'depth_5_while'):
            for (i, instr) in i + 1 < len(instrs):
                if (instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD')) and (instr.arg is not None):
                    leaders.add(instr.arg)
                if (instr.opname in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER')) and (instr.arg is not None):
                    leaders.add(instr.arg)
                if i + 1 < len(instrs):
                    leaders.add(instrs[i + 1].offset)
        for (i, start) in any(<genexpr>(block_instrs)):
            if i + 1 < len(sorted_leaders):
                pass
            block_instrs = <listcomp>(instrs)
            if len(block_instrs) > 3:
                pass
            break
            if any(<genexpr>(block_instrs)):
                last = block_instrs[-1]
                print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[-1].offset + 2}")
            if any(<genexpr>(block_instrs)):
                for ins in ins.opname == 'JUMP_ABSOLUTE':
                    if ins.opname == 'JUMP_ABSOLUTE':
                        print(f"  → JUMP: offset={ins.offset}, target={ins.arg}")
# [SUMMARY] 36 blocks · 35 processed · 1 orphan · 300 instr
