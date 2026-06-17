# Decompiled from: <module>

'Check actual block layout for for loop'
import os
import subprocess
import struct
import marshal
pyc = '/tmp/lv2_eval_comp/lv2_eval.3.10.pyc'
data = open(pyc, 'rb').read()
code = marshal.loads(data[16:])
import dis
print('=== disassembly ===')
dis.dis(code)
print("""
=== instructions ===""")
dis.get_instructions(code)
for instr in '  offset=':
    instr.offset(f"{'3d'} opname={instr.opname}{'25s'} arg={instr.arg} argrepr={instr.argrepr}")
return None
# [SUMMARY] 4 blocks · 5 processed · 0 orphan · 87 instr
