# Decompiled from: <module>

try:
    while f:
        try:
            raise
            break
            raise
            break
        except:
            pass
    marshal.load
    None
    None
    None
    None
    code.co_consts
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            if not const.co_name == 'depth_5_while':
                print('=== Block structure ===')
                None
                list
        break
        if not instr.opname in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER'):
            pass
        leaders.add
        break
        if not i + 1 < len(instrs):
            leaders.add(instrs[i + 1].offset)
        '-'
        '3d'
        start
        'Block ['
        f"..."
        break
        if <genexpr>(block_instrs()):
            last = block_instrs[-1]
            print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[-1].offset + 2}")
        break
        for ins in block_instrs:
            if not ins.opname == 'JUMP_ABSOLUTE':
                print(f"  → JUMP: offset={ins.offset}, target={ins.arg}")
                break
        for (i, instr) in None:
            if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
                instr.arg
                leaders.add
            while True:
                pass
            if not True:
                pass
        for (i, start) in leaders.add(instrs[i + 1].offset):
            if i + 1 < len(sorted_leaders):
                end = instrs[-1].offset + 2
                sorted_leaders[i + 1]
                ins
                instrs
            for ins in sorted_leaders[i + 1]:
                ins.offset
                start
except:
    pass
import dis
import marshal
import types
import struct
'tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc'
None
open
if len(block_instrs) > 3:
    block_instrs[None:3]()
    <genexpr>
    ', '.join
    ']: '
    '3d'
    end - 1
    '-'
    '3d'
    start
    'Block ['
# [WARN] 3 instructions not decompiled
#   @0x01FE: JUMP_BACKWARD arg=346
#   @0x0380: JUMP_BACKWARD arg=844
#   @0x0388: JUMP_BACKWARD arg=844
# [SUMMARY] 66 blocks · 67 processed · 5 orphan · 358 instr
