# Decompiled from: <module>

with open(sys.argv[1], 'rb') as f:
    magic = f.read(4)
    f.read(8)
    code = marshal.load(f)
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 82 instr
