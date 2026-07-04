# Decompiled from: <module>

import dis
import marshal
import types
import struct
open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb')
f.read(16)
code = marshal.load(f)
None(None)
code.co_consts
if not f:
    pass
raise
raise
if not isinstance(const, types.CodeType):
    pass
elif not const.co_name == 'depth_5_while':
    pass
else:
    print('=== Block structure ===')
    instrs = list(dis.Bytecode(const))
    leaders = {0}
    enumerate(instrs)
    sorted_leaders = sorted(leaders)
    enumerate(sorted_leaders)
    if i + 1 < len(sorted_leaders):
        pass
    else:
        instrs[-1].offset + 2
        ins
        instrs
        []
        if len(block_instrs) > 3:
            pass
        else:
            f"-{end - 1}{'3d'}]: {', '.join}{(ins.opname for ins in block_instrs())}"
            '3d'
            start
            'Block ['
            if (<genexpr>)(block_instrs()):
                last = block_instrs[-1]
                print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[-1].offset + 2}")
            elif not (<genexpr>)(block_instrs()):
                pass
            else:
                block_instrs
                if not ins.opname == 'JUMP_ABSOLUTE':
                    pass
                else:
                    print(f"  → JUMP: offset={ins.offset}, target={ins.arg}")
        if (ins.offset <= start) and not start < end:
            pass
        else:
            ins
    if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
        pass
    elif not instr.opname in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER'):
        pass
    elif instr.arg:
        leaders.add(instr.arg)
# [WARN] 2 instructions not decompiled
#   @0x0188: POP_JUMP_IF_NOT_NONE arg=2
#   @0x01F8: POP_JUMP_IF_NONE arg=54
