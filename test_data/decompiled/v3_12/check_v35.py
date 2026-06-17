# Decompiled from: <module>

try:
    magic = f.read(4)
    f.read(8)
    code = marshal.load(f)
except:
    pass
import marshal
import sys
print('Module:', code.co_name)
print('  argc:', code.co_argcount)
print('  nlocals:', code.co_nlocals)
print('  code len:', len(code.co_code))
'  code hex:'(code.co_code.hex(), None // 60)
def dump_code(c, depth):
    prefix = '  ' * depth
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            pass
        print(f"{prefix!s}Function: {const.co_name!s}")
        print('%s  argc=%d nlocals=%d code=%dB' % (prefix, const.co_argcount, const.co_nlocals, len(const.co_code)))
        dump_code(const, depth + 1)
dump_code(code)
return None
# orphan @0x01D0
raise
# [WARN] 1 instructions not decompiled
#   @0x01CE: JUMP_BACKWARD arg=280
# [SUMMARY] 9 blocks · 8 processed · 1 orphan · 105 instr
