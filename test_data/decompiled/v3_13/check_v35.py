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
print('  code hex:', code.co_code.hex()[None:60])
def dump_code(c, depth):
    # orphan @0x0050
    hasattr(const, 'co_name')
    for const in c.co_consts:
        while hasattr(const, 'co_code'):
            break
            break
    # orphan @0x0072
    const.co_name
    'Function: '
    prefix
    print
    # [WARN] 1 instructions not decompiled
    #   @0x004C: JUMP_BACKWARD arg=36
dump_code(code)
raise
# [SUMMARY] 8 blocks · 9 processed · 0 orphan · 107 instr
