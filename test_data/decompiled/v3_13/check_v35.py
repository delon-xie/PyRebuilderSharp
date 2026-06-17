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
print('  code hex:', code.co_code.hex()[None:60])
def dump_code(c, depth):
    # orphan @0x004C
    # orphan @0x0028
    # orphan @0x0000
    prefix = '  ' * depth
    # orphan @0x0072
    # orphan @0x009A
dump_code(code)
return None
raise
# [SUMMARY] 8 blocks · 9 processed · 0 orphan · 107 instr
