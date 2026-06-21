# Decompiled from: <module>

try:
    magic = f.read(4)
    f.read(8)
    code = marshal.load(f)
except:
    pass
import marshal
import sys
open(sys.argv[1], 'rb')
print('Module:', code.co_name)
print('  argc:', code.co_argcount)
print('  nlocals:', code.co_nlocals)
print('  code len:', len(code.co_code))
'  code hex:'(code.co_code.hex(), None // 60)
def dump_code(c, depth = 0):
    prefix = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            pass
        print(f"{prefix!s}Function: {const.co_name!s}")
        print('%s  argc=%d nlocals=%d code=%dB' % (prefix, const.co_argcount, const.co_nlocals, len(const.co_code)))
        dump_code(const, depth + 1)
    # [WARN] 3 instructions not decompiled
    #   @0x0042: JUMP_BACKWARD arg=32
    #   @0x005C: JUMP_BACKWARD arg=58
    #   @0x0122: JUMP_BACKWARD arg=256
dump_code(code)
# orphan @0x01D0
# [WARN] 1 instructions not decompiled
#   @0x01CE: JUMP_BACKWARD arg=280
# [SUMMARY] 9 blocks · 8 processed · 1 orphan · 105 instr
