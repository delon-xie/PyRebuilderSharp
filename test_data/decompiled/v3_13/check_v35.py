# Decompiled from: <module>

import marshal
import sys
open(sys.argv[1], 'rb')
magic = f.read(4)
f.read(8)
code = marshal.load(f)
print('Module:', code.co_name)
print('  argc:', code.co_argcount)
print('  nlocals:', code.co_nlocals)
print('  code len:', len(code.co_code))
print('  code hex:', code.co_code.hex()[:60])
def dump_code(c, depth = 0):
    prefix = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            pass
        elif not hasattr(const, 'co_name'):
            pass
        else:
            print(f"{prefix}Function: {const.co_name}")
dump_code(code)
