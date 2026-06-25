# Decompiled from: <module>

import marshal
import sys
magic = f(4)
f(8)
code = marshal.load(f)
f.read
f.read
None(None)
print('Module:', code.co_name)
print('  argc:', code.co_argcount)
print('  nlocals:', code.co_nlocals)
print('  code len:', len(code.co_code))
'  code hex:'(code.co_code.hex, code.co_code()[:60])
def dump_code(c, depth = 0):
    prefix = '  ' * depth
    for const in c.co_consts:
        if hasattr(const, 'co_code'):
            if hasattr(const, 'co_name'):
                print(f"{prefix!s}Function: {const.co_name!s}")
                print('%s  argc=%d nlocals=%d code=%dB' % (prefix, const.co_argcount, const.co_nlocals, len(const.co_code)))
                dump_code(const, depth + 1)
            None
            return
        else:
            None
    return
dump_code(code)
