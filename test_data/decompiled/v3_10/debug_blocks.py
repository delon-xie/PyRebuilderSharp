# Decompiled from: <module>

import dis
import marshal
import types
import struct
with open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb') as f:
    f.read(16)
    code = marshal.load(f)
    raise
    for const in code.co_consts:
        if isinstance(const, types.CodeType) and (const.co_name == 'depth_5_while'):
            for (i, instr) in enumerate(instrs):
                if (instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD')) and (instr.arg is not None):
                    leaders.add(instr.arg)
                if instr.arg is not None:
                    leaders.add(instr.arg)
                elif i + 1 < len(instrs):
                    leaders.add(instrs[i + 1].offset)
        for (i, start) in enumerate(sorted_leaders):
            if i + 1 < len(sorted_leaders):
                pass
            else:
                instrs[-1].offset + 2
            block_instrs = <listcomp>(instrs)
            if len(block_instrs) > 3:
                pass
            else:
                f"{'3d'}-{end - 1}{'3d'}]: {', '.join(<genexpr>(block_instrs))}"
                start
                'Block ['
            break
            if any(<genexpr>(block_instrs)):
                last = block_instrs[-1]
                print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[-1].offset + 2}")
            elif any(<genexpr>(block_instrs)):
                for ins in block_instrs:
                    if ins.opname == 'JUMP_ABSOLUTE':
                        print(f"  → JUMP: offset={ins.offset}, target={ins.arg}")
# [SUMMARY] 38 blocks · 37 processed · 1 orphan · 300 instr
