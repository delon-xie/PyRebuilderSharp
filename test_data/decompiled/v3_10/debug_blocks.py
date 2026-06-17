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
        if isinstance(const, types.CodeType):
            if const.co_name == 'depth_5_while':
                for (i, instr) in enumerate(instrs):
                    if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
                        if instr.arg is not None:
                            leaders.add(instr.arg)
                            continue
                            if instr.opname in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER'):
                                if instr.arg is not None:
                                    leaders.add(instr.arg)
                                    if i + 1 < len(instrs):
                                        leaders.add(instrs[i + 1].offset)
                                    break
                                    if any(<genexpr>(block_instrs)):
                                        for ins in block_instrs:
                                            if ins.opname == 'JUMP_ABSOLUTE':
                                                print(f"  → JUMP: offset={ins.offset}, target={ins.arg}")
                                break
                                if True:
                                    last = block_instrs[-1]
        sorted_leaders = sorted(leaders)
        for (i, start) in enumerate(sorted_leaders):
            if i + 1 < len(sorted_leaders):
                pass
            block_instrs = <listcomp>(instrs)
            if len(block_instrs) > 3:
                pass
# [SUMMARY] 41 blocks · 41 processed · 1 orphan · 300 instr
