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
if not True:
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
    if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
        if instr.arg:
            leaders.add(instr.arg)
    elif not instr.opname in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER'):
        pass
    elif instr.arg:
        leaders.add(instr.arg)
        if not i + 1 < len(instrs):
            pass
        else:
            leaders.add(instrs[i + 1].offset)
# [WARN] 2 instructions not decompiled
#   @0x019C: POP_JUMP_IF_NONE arg=474
#   @0x0218: POP_JUMP_IF_NONE arg=594
