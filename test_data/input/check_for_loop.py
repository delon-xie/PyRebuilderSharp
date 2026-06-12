#!/usr/bin/env python3
"""Check actual block layout for for loop"""
import os, subprocess, struct, marshal

pyc = "/tmp/lv2_eval_comp/lv2_eval.3.10.pyc"
data = open(pyc, 'rb').read()

# 3.10 = 16 byte header
code = marshal.loads(data[16:])
import dis
print("=== disassembly ===")
dis.dis(code)

print("\n=== instructions ===")
for instr in dis.get_instructions(code):
    print(f"  offset={instr.offset:3d} opname={instr.opname:25s} arg={instr.arg} argrepr={instr.argrepr}")
