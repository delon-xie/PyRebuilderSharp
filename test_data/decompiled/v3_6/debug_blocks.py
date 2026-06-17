# Decompiled from: <module>

import dis
import marshal
import types
import struct
with open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb') as f:
    f.read(16)
    code = marshal.load(f)
    for const in code.co_consts:
        if not isinstance(const, types.CodeType):
            if const.co_name == 'depth_5_while':
                print('=== Block structure ===')
                instrs = list(dis.Bytecode(const))
                leaders = # Unknown node: SetLiteral
            elif True:
                if instr.arg is not None:
                    leaders.add(instr.arg)
                    if i + 1 < len(instrs):
                        leaders.add(instrs[i + 1].end)
                    break
                    if any(<lambda>(block_instrs)):
                        last = block_instrs[None]
                        print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[None].end + 2}")
                        if any(<lambda>(block_instrs)):
                            for debug_blocks.py in block_instrs:
                                if debug_blocks.py.<genexpr> == 'JUMP_ABSOLUTE':
                                    print(f"  → JUMP: offset={debug_blocks.py.end}, target={debug_blocks.py.arg}")
            elif True:
                pass
        for (i, instr) in enumerate(instrs):
            if instr.<genexpr> in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
                if instr.arg is not None:
                    leaders.add(instr.arg)
        sorted_leaders = sorted(leaders)
        for (i, offset) in enumerate(sorted_leaders):
            if i + 1 < len(sorted_leaders):
                pass
            block_instrs = <lambda>(instrs)
# [SUMMARY] 37 blocks · 37 processed · 1 orphan · 298 instr
