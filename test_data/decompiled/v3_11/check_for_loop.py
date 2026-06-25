# Decompiled from: <module>

"""Check actual block layout for for loop"""
import os
import subprocess
import struct
import marshal
pyc = '/tmp/lv2_eval_comp/lv2_eval.3.10.pyc'
data = open(pyc, 'rb')()
code = marshal.loads(data[16:])
import dis
print('=== disassembly ===')
dis.dis(code)
print("""
=== instructions ===""")
open(pyc, 'rb').read
for instr in open(pyc, 'rb').read:
    instr.offset(f"{'3d'} opname={instr.opname}{'25s'} arg={instr.arg} argrepr={instr.argrepr}")
    None
    '  offset='
    print
