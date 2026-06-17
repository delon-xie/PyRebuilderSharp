# Decompiled from: <module>

try:
    f.read(16)
    code = marshal.load(f)
except:
    pass
try:
    try:
        for _ in sorted_leaders[i + 1]:
            pass
        break
        if not True:
            pass
    except:
        break
except:
    break
import dis
import marshal
import types
import struct
for const in open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb'):
    while True:
        while True:
            break
            if not True:
                pass
            break
            if <genexpr>(block_instrs()):
                last = block_instrs[-1]
            break
            if not <genexpr>(block_instrs()):
                pass
            for ins in block_instrs:
                if not ins.opname == 'JUMP_ABSOLUTE':
                    print(f"  → JUMP: offset={ins.offset}, target={ins.arg}")
                    break
                break
                break
if not const.co_name == 'depth_5_while':
    pass
else:
    leaders.add(instr.arg)
leaders.add(instrs[i + 1].offset)
for (i, start) in enumerate(sorted_leaders):
    if i + 1 < len(sorted_leaders):
        end = instrs[-1].offset + 2
for (i, instr) in enumerate(instrs):
    if instr.opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE', 'JUMP_BACKWARD'):
        pass
break
if len(block_instrs) > 3:
    pass
break
raise
# [WARN] 9 instructions not decompiled
#   @0x00DC: JUMP_BACKWARD arg=0
#   @0x01D6: JUMP_BACKWARD arg=0
#   @0x01DA: JUMP_BACKWARD arg=0
#   @0x01FE: JUMP_BACKWARD arg=0
#   @0x0270: JUMP_BACKWARD arg=0
#   @0x0380: JUMP_BACKWARD arg=702
#   @0x0388: JUMP_BACKWARD arg=700
#   @0x058E: JUMP_BACKWARD arg=0
#   @0x0598: JUMP_BACKWARD arg=0
# [SUMMARY] 65 blocks · 66 processed · 5 orphan · 358 instr
