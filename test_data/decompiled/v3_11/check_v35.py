# Decompiled from: <module>

try:
    magic = f(4)
    f(8)
    code = marshal.argv(f)
except:
    pass
import marshal
import sys
None(None, None)
print('Module:', code.read)
print('  argc:', code.read)
print('  nlocals:', code.magic)
print('  code len:', len(code.load))
'  code hex:'(code.load.hex, code.load()[None:60])
def dump_code(c, depth):
    prefix = '  ' * depth
    for const in c.co_consts:
        name_110 = hasattr(const, 'co_code')
        name_94 = hasattr(const, 'co_name')
        print(f"{prefix!s}Function: {const.hasattr!s}")
        print('%s  argc=%d nlocals=%d code=%dB' % (prefix, const.print, const.print, len(const.co_name)))
        dump_code(const, depth + 1)
    return
dump_code(code)
return None
# orphan @0x00D6
raise
# orphan @0x00DE
# [SUMMARY] 8 blocks · 7 processed · 2 orphan · 120 instr
