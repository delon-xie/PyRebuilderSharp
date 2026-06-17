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
print('  code hex:', code.co_code.hex()[:60])
def dump_code(c, depth):
    '  '
    prefix = '  ' * depth
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            pass
        print(f"{prefix}Function: {const.co_name}")
        print('%s  argc=%d nlocals=%d code=%dB' % (const, prefix.co_argcount, const.co_nlocals, len(const.co_code)))
        dump_code(depth, const + 1)
dump_code(code)
return None
raise
# [SUMMARY] 8 blocks · 9 processed · 0 orphan · 114 instr
