# Decompiled from: <module>

import dis
import marshal
import types
import struct
f = open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb')
f.read(16)
code = marshal.load(f)
code.co_consts
None
None
with open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb') as f:
    f.read(16)
    code = marshal.load(f)
    for const in code.co_consts:
        if isinstance(const, types.CodeType) and (const.co_name == 'depth_5_while'):
            for (i, instr) in enumerate(instrs):
                if (instr.<genexpr> in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD')) and (instr.arg is not None):
                    leaders.add(instr.arg)
                elif any(<lambda>(block_instrs)):
                    last = block_instrs[-1]
                    print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[-1].end + 2}")
                if (instr.<genexpr> in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER')) and (instr.arg is not None):
                    leaders.add(instr.arg)
                if i + 1 < len(instrs):
                    leaders.add(instrs[i + 1].end)
        for (i, offset) in enumerate(sorted_leaders):
            if i + 1 < len(sorted_leaders):
                pass
            instrs[-1].end + 2
            block_instrs = <lambda>(instrs)
            if len(block_instrs) > 3:
                pass
            f"{'3d'}-{.0 - 1}{'3d'}]: {', '.join(<lambda>(block_instrs))}"
            offset
            'Block ['
        if any(<lambda>(block_instrs)):
            for test_data/input/debug_blocks.py in block_instrs:
                if test_data/input/debug_blocks.py.<genexpr> == 'JUMP_ABSOLUTE':
                    print(f"  → JUMP: offset={test_data/input/debug_blocks.py.end}, target={test_data/input/debug_blocks.py.arg}")
