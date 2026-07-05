# Decompiled from: <module>

import dis
import marshal
import types
import struct
f = open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb')
f.read(16)
code = marshal.load(f)
with open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb') as f:
    f.read(16)
    code = marshal.load(f)
    pass
    pass
    for const in code.co_consts:
        pass
        if isinstance(const, types.CodeType):
            pass
            if const.co_name == 'depth_5_while':
                for (i, instr) in enumerate(instrs):
                    pass
                    if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
                        pass
                        if instr.arg is not None:
                            leaders.add(instr.arg)
                    pass
                    if instr.opname in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER'):
                        pass
                        if instr.arg is not None:
                            leaders.add(instr.arg)
                    pass
                    pass
                    if i + 1 < len(instrs):
                        leaders.add(instrs[i + 1].offset)
        for (i, start) in enumerate(sorted_leaders):
            pass
            if i + 1 < len(sorted_leaders):
                pass
            instrs[-1].offset + 2
            block_instrs = lambda x: x(instrs)
            if len(block_instrs) > 3:
                pass
            f"{'3d'}-{end - 1}{'3d'}]: {', '.join(lambda x: x(block_instrs))}"
            start
            'Block ['
            pass
            if any(lambda x: x(block_instrs)):
                last = block_instrs[-1]
                print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[-1].offset + 2}")
            pass
            if any(lambda x: x(block_instrs)):
                for ins in block_instrs:
                    pass
                    if ins.opname == 'JUMP_ABSOLUTE':
                        print(f"  → JUMP: offset={ins.offset}, target={ins.arg}")
            pass
        pass
