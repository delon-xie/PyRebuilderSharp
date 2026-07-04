# Decompiled from: <module>

import struct
import marshal
import dis
None
open
__name__
'/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc'('rb')
__module__
'/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc'('rb')
print('Names:', code.co_names)
print('Constants:', code.co_consts)
print('Varnames:', code.co_varnames)
print()
print('Instructions:')
dis.get_instructions(code)
instr = {instr.offset(f"4d {instr.opname}20s {instr.arg} {instr.argrepr}") for instr in dis.get_instructions(code)}
instr = {instr.offset(f"4d {instr.opname}20s {instr.arg} {instr.argrepr}") for instr in dis.get_instructions(code)}
