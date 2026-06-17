# Decompiled from: <module>

import struct
for ver in ('3.5', '3.6', '3.7', '3.8', '3.9', '3.10'):
    path = f"/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.{ver}.pyc"
    data = open(path, 'rb').read()
    if ver in ('2.7',):
        hdr = 8
    elif ver in ('3.5', '3.6'):
        hdr = 12
return None
# [SUMMARY] 15 blocks · 16 processed · 0 orphan · 273 instr
