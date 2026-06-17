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
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            pass
        break
        break
        if not hasattr(const, 'co_name'):
            pass
    # [WARN] 3 instructions not decompiled
    #   @0x0056: JUMP_BACKWARD arg=0
    #   @0x007E: JUMP_BACKWARD arg=0
    #   @0x0156: JUMP_BACKWARD arg=0
dump_code(code)
return None
raise
# [SUMMARY] 8 blocks · 9 processed · 0 orphan · 113 instr
