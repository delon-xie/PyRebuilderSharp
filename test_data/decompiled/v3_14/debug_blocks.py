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
                try:
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
                            last = block_instrs[-1]
                            print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[-1].offset + 2}")
                    else:
                        <genexpr>(block_instrs())
                    break
                except:
                    break
            except:
                break
        except:
            break
        break
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
    print('=== Block structure ===')
    instrs = list(dis.Bytecode(const))
    leaders = {0}
    enumerate(instrs)
    for (i, instr) in enumerate(instrs):
        if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
            leaders.add(instr.arg)
        leaders.add(instr.arg)
        if not i + 1 < len(instrs):
            pass
        else:
            leaders.add(instrs[i + 1].offset)
    sorted_leaders = sorted(leaders)
    enumerate(sorted_leaders)
raise
# [WARN] 16 instructions not decompiled
#   @0x00EE: JUMP_BACKWARD arg=180
#   @0x0114: JUMP_BACKWARD arg=180
#   @0x01F2: JUMP_BACKWARD arg=366
#   @0x0218: JUMP_BACKWARD arg=366
#   @0x0296: JUMP_BACKWARD arg=366
#   @0x02EC: JUMP_BACKWARD arg=366
#   @0x03E2: JUMP_BACKWARD arg=938
#   @0x03EA: JUMP_BACKWARD arg=938
#   @0x03F2: JUMP_BACKWARD arg=938
#   @0x0510: JUMP_BACKWARD arg=1278
# [SUMMARY] 71 blocks · 72 processed · 0 orphan · 405 instr
