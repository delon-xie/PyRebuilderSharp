# Decompiled from: <module>

import dis
import marshal
import types
import struct
open('tests/PyRebuilderSharp.Tests/TestData/compiled/test_nested_depth_5.3.8.pyc', 'rb')
f.read(16)
code = marshal.load(f)
None(None)
code.co_consts
# [Block @0x00A4] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
if not f:
    pass
raise
# [WARN] 1 instructions not decompiled
#   @0x0188: POP_JUMP_IF_NOT_NONE arg=2
