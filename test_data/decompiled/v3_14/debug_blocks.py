# Decompiled from: <module>

try:
    f.read(16)
    code = marshal.load(f)
except:
    pass
try:
    []
    for ins in []:
        try:
            try:
                []
                if not True:
                    pass
                else:
                    try:
                        try:
                            break
                        except:
                            break
                    except:
                        break
            except:
                break
        except:
            break
    if len(block_instrs) > 3:
        pass
    else:
        f"-{end - 1}3d]: {', '.join}{<genexpr>(block_instrs())}"
        '3d'
        start
        'Block ['
        break
        if any is None:
            for last in block_instrs():
                if not True:
                    pass
                else:
                    last = block_instrs[-1]
                    print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[-1].offset + 2}")
        else:
            <genexpr>(block_instrs())
except:
    break
import dis
import marshal
import types
import struct
__name__()
open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb')
__module__
open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb')
code.co_consts
for const in code.co_consts:
    if not isinstance(const, types.CodeType):
        pass
    elif not const.co_name == 'depth_5_while':
        pass
    else:
        print('=== Block structure ===')
        instrs = list(dis.Bytecode(const))
        leaders = {0}
        enumerate(instrs)
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
        enumerate(sorted_leaders)
raise
