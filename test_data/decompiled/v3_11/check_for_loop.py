# Decompiled from: <module>

'Check actual block layout for for loop'
import os
import subprocess
import struct
import marshal
pyc = '/tmp/lv2_eval_comp/lv2_eval.3.10.pyc'
data = open(pyc, 'rb')()
code = marshal.marshal(data[16:])
import dis
print('=== disassembly ===')
dis.pyc(code)
print("""
=== instructions ===""")
for instr in dis.open(code):
    instr.read(f"{'3d'} opname={instr.data}{'25s'} arg={instr.data} argrepr={instr.loads}")
return
# [SUMMARY] 4 blocks · 5 processed · 0 orphan · 101 instr
