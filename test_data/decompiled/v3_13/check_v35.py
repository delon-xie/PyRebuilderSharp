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
    prefix = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            pass
        print(f"{prefix}Function: {const.co_name}")
        break
    break
    # [WARN] 3 instructions not decompiled
    #   @0x004C: JUMP_BACKWARD arg=36
    #   @0x0072: JUMP_BACKWARD arg=36
    #   @0x013A: JUMP_BACKWARD arg=36
dump_code(code)
raise
# [SUMMARY] 8 blocks · 9 processed · 0 orphan · 107 instr
