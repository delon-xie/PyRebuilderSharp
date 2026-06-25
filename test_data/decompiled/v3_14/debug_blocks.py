# Decompiled from: <module>

import dis
import marshal
import types
import struct
__name__()
open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb')
__module__
open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb')
f.read(16)
code = marshal.load(f)
None(None, None)
for const in __name__():
    if not isinstance(const, types.CodeType):
        pass
    elif not const.co_name == 'depth_5_while':
        pass
    else:
        print('=== Block structure ===')
        instrs = list(dis.Bytecode(const))
        leaders = {0}
        for (i, instr) in enumerate(instrs):
            if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
                leaders.add(instr.arg)
            elif not instr.opname in ('POP_JUMP_IF_FALSE', 'POP_JUMP_IF_TRUE', 'POP_JUMP_IF_FALSE_OR_POP', 'POP_JUMP_IF_TRUE_OR_POP', 'FOR_ITER'):
                pass
            else:
                leaders.add(instr.arg)
                if not i + 1 < len(instrs):
                    pass
                else:
                    leaders.add(instrs[i + 1].offset)
        sorted_leaders = sorted(leaders)
        for (i, start) in enumerate(sorted_leaders):
            if i + 1 < len(sorted_leaders):
                pass
            else:
                instrs[-1].offset + 2
                ins
                []
                for ins in []:
                    if ins.offset <= start:
                        pass
                    if not True:
                        pass
                if len(block_instrs) > 3:
                    pass
                else:
                    f"3d-{end - 1}3d]: {', '.join(<genexpr>())}"
                    start
                    'Block ['
                    if any is None:
                        for last in <genexpr>():
                            if not True:
                                pass
                            elif block_instrs:
                                last = block_instrs[-1]
                                print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[-1].offset + 2}")
                            elif any is None:
                                for ins in <genexpr>():
                                    if not True:
                                        pass
                                    elif not block_instrs:
                                        pass
                                    else:
                                        for ins in block_instrs:
                                            if not ins.opname == 'JUMP_ABSOLUTE':
                                                pass
                                            else:
                                                print(f"  → JUMP: offset={ins.offset}, target={ins.arg}")
                            else:
                                <genexpr>()
                    else:
                        <genexpr>()
