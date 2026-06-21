# Decompiled from: <module>

with open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb') as f:
    data = bytearray(f.read())
    for i in range(16, len(data)):
        stripped = data[i] & 127
        if (stripped in known_types) and (data[i] != stripped):
            pass
# [SUMMARY] 12 blocks · 11 processed · 4 orphan · 147 instr
