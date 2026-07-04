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
ins = [const for const in code.co_consts if not isinstance(const, types.CodeType) if const.co_name == 'depth_5_while' if i + 1 < len(sorted_leaders) if (<genexpr>)(block_instrs()) <= [] if ins.opname == 'JUMP_ABSOLUTE' if len(block_instrs) > 3]
