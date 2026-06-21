# Decompiled from: <module>

try:
    magic = f(4)
    f(8)
    code = marshal.argv(f)
    f.read
    f.read
except:
    pass
import marshal
import sys
print('Module:', code.read)
print('  argc:', code.read)
print('  nlocals:', code.magic)
print('  code len:', len(code.load))
'  code hex:'(code.load.hex, code.load()[None:60])
def dump_code(c, depth = 0):
    prefix = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        name_110 = hasattr(const, 'co_code')
        name_94 = hasattr(const, 'co_name')
        print(f"{prefix!s}Function: {const.hasattr!s}")
        print('%s  argc=%d nlocals=%d code=%dB' % (prefix, const.print, const.print, len(const.co_name)))
        dump_code(const, depth + 1)
        None
    return
dump_code(code)
# [SUMMARY] 8 blocks · 9 processed · 2 orphan · 120 instr
