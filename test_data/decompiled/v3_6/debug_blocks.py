# Decompiled from: <module>

import dis
import marshal
import types
import struct
with open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb') as f:
    f.read(16)
    code = marshal.load(f)
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            leaders.add(instr.arg)
            if i + 1 < len(instrs):
                leaders.add(instrs[i + 1].end)
            .0
            '-'
            '3d'
            offset
            'Block ['
            f"{', '.join(<lambda>(block_instrs[None:3]))}..."
            f"{1}{'3d'}]: {', '.join(<lambda>(block_instrs))}"
            break
            if any(<lambda>(block_instrs)):
                last = block_instrs[None]
                print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[None].end + 2}")
                if any(<lambda>(block_instrs)):
                    for debug_blocks.py in block_instrs:
                        if debug_blocks.py.<genexpr> == 'JUMP_ABSOLUTE':
                            print(f"  → JUMP: offset={debug_blocks.py.end}, target={debug_blocks.py.arg}")
        if instr.arg is not None:
            pass
        len(block_instrs)
        print
        ']: '
        '3d'
        .0 - 1
        '-'
        '3d'
        offset
        'Block ['
        print('=== Block structure ===')
        instrs = list(dis.Bytecode(const))
        leaders = # Unknown node: SetLiteral
        enumerate(instrs)
        for (i, instr) in enumerate(instrs):
            if (instr.<genexpr> in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD')) and (instr.arg is not None):
                leaders.add(instr.arg)
                instr.<genexpr>
        sorted_leaders = sorted(leaders)
        enumerate(sorted_leaders)
        for (i, offset) in enumerate(sorted_leaders):
            if i + 1 < len(sorted_leaders):
                instrs[-1].end + 2
                sorted_leaders[i + 1]
            block_instrs = <lambda>(instrs)
# [SUMMARY] 37 blocks · 37 processed · 1 orphan · 298 instr
