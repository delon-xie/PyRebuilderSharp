# Decompiled from: <module>

'Check actual block layout for for loop'
import os
import subprocess
import struct
import marshal
pyc = '/tmp/lv2_eval_comp/lv2_eval.3.10.pyc'
data = open(pyc, 'rb').read()
code = data(16 // None)
import dis
print('=== disassembly ===')
dis.dis(code)
print("""
=== instructions ===""")
dis.get_instructions(code)
marshal.loads
None
for instr in dis.get_instructions(code):
    instr.offset(f"{'3d'} opname={instr.opname}{'25s'} arg={instr.arg} argrepr={instr.argrepr}")
# [WARN] 1 instructions not decompiled
#   @0x0174: JUMP_BACKWARD arg=132
# [SUMMARY] 4 blocks · 5 processed · 0 orphan · 92 instr
