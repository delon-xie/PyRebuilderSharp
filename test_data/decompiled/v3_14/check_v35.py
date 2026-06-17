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
    # orphan @0x0054
    # orphan @0x0030
    # orphan @0x0000
    prefix = '  ' * depth
    # orphan @0x007C
    # orphan @0x00AC
    # orphan @0x00FC
    dump_code(depth, const + 1)
dump_code(code)
return None
raise
# [SUMMARY] 8 blocks · 9 processed · 0 orphan · 114 instr
