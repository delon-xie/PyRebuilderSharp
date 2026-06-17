# Decompiled from: <module>

import marshal
import sys
with open(sys.argv[1], 'rb') as f:
    magic = f.read(4)
    f.read(8)
    code = marshal.load(f)
    raise
    print('Module:', code.co_name)
    print('  argc:', code.co_argcount)
    print('  nlocals:', code.co_nlocals)
    print('  code len:', len(code.co_code))
def dump_code(c, depth):
    prefix = '  ' * depth
    for const in c.co_consts:
        if hasattr(const, 'co_code'):
            if hasattr(const, 'co_name'):
                print('%sFunction: %s' % (prefix, const.co_name))
                print('%s  argc=%d nlocals=%d code=%dB' % (prefix, const.co_argcount, const.co_nlocals, len(const.co_code)))
                dump_code(const, depth + 1)
dump_code(code)
return None
# [SUMMARY] 4 blocks · 5 processed · 0 orphan · 96 instr
