# Decompiled from: <module>

import marshal
import sys
f = open(sys.argv[1], 'rb')
magic = f.read(4)
f.read(8)
code = marshal.load(f)
print('Module:', code.co_name)
print('  argc:', code.co_argcount)
print('  nlocals:', code.co_nlocals)
print('  code len:', len(code.co_code))
print('  code hex:', code.co_code.hex()[:60])
def dump_code(c, depth):
    prefix = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        pass
    print('%sFunction: %s' % (prefix, const.co_name))
    print('%s  argc=%d nlocals=%d code=%dB' % (prefix, const.co_argcount, const.co_nlocals, len(const.co_code)))
    dump_code(const, depth + 1)
dump_code(code)
with open(sys.argv[1], 'rb') as f:
    magic = f.read(4)
    f.read(8)
    code = marshal.load(f)
