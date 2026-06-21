# Decompiled from: <module>

try:
    f.read(16)
    code = marshal.load(f)
except:
    break
try:
    []
    for ins in []:
        try:
            try:
                []
                if not True:
                    pass
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
        break
except:
    break
import dis
import marshal
import types
import struct
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
    break
    for (i, start) in enumerate(sorted_leaders):
        if i + 1 < len(sorted_leaders):
            pass
        else:
            instrs[-1].offset + 2
        ins
        instrs
    break
break
if len(block_instrs) > 3:
    pass
else:
    f"-{end - 1}3d]: {', '.join}{<genexpr>(block_instrs())}"
    '3d'
    start
    'Block ['
break
if <genexpr>(block_instrs()):
    last = block_instrs[-1]
    print(f"  → COND: jump_target={last.arg}, fallthrough_offset={block_instrs[-1].offset + 2}")
elif not <genexpr>(block_instrs()):
    pass
else:
    block_instrs
break
raise
# [WARN] 14 instructions not decompiled
#   @0x00DC: JUMP_BACKWARD arg=164
#   @0x0100: JUMP_BACKWARD arg=164
#   @0x01DA: JUMP_BACKWARD arg=346
#   @0x01FE: JUMP_BACKWARD arg=346
#   @0x0270: JUMP_BACKWARD arg=346
#   @0x02B6: JUMP_BACKWARD arg=346
#   @0x0380: JUMP_BACKWARD arg=844
#   @0x0388: JUMP_BACKWARD arg=844
#   @0x0390: JUMP_BACKWARD arg=844
#   @0x050E: JUMP_BACKWARD arg=734
# [SUMMARY] 55 blocks · 55 processed · 0 orphan · 358 instr
