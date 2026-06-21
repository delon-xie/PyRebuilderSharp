# Decompiled from: <module>

try:
    magic = f.read(4)
    f.read(8)
    code = marshal.load(f)
except:
    pass
import marshal
import sys
__name__()
open(sys.argv[1], 'rb')
__module__
open(sys.argv[1], 'rb')
print('Module:', code.co_name)
print('  argc:', code.co_argcount)
print('  nlocals:', code.co_nlocals)
print('  code len:', len(code.co_code))
print('  code hex:', code.co_code.hex()[:60])
def dump_code(c, depth):
    """  """
    prefix = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            pass
        print(f"{prefix}Function: {const.co_name}")
        print('%s  argc=%d nlocals=%d code=%dB' % (const, prefix.co_argcount, const.co_nlocals, len(const.co_code)))
        dump_code(depth, const + 1)
    # [WARN] 3 instructions not decompiled
    #   @0x0056: JUMP_BACKWARD arg=44
    #   @0x007E: JUMP_BACKWARD arg=44
    #   @0x0156: JUMP_BACKWARD arg=44
dump_code(code)
raise
# [SUMMARY] 8 blocks · 9 processed · 0 orphan · 113 instr
