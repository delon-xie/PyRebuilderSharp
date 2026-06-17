# Decompiled from: <module>

# orphan @0x0000
__doc__ = 'Check actual block layout for for loop'
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
# orphan @0x00F6
instr.offset(f"3d opname={instr.opname}25s arg={instr.arg} argrepr={instr.argrepr}")
'  offset='
return None
# [SUMMARY] 4 blocks · 3 processed · 3 orphan · 93 instr
