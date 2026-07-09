import sys
print(f"Python version: {sys.version}")

import opcode
print(f"\n=== Opcode 55 name: {opcode.opname[55]}")
print(f"Opcode 107 name: {opcode.opname[107]}")

import _opcode
if hasattr(_opcode, 'INTRINSIC_EMPTY_SET'):
    print(f"\nINTRINSIC_EMPTY_SET = {_opcode.INTRINSIC_EMPTY_SET}")
if hasattr(_opcode, 'INTRINSIC_LIST_TO_TUPLE'):
    print(f"INTRINSIC_LIST_TO_TUPLE = {_opcode.INTRINSIC_LIST_TO_TUPLE}")

# 检查所有 intrinsic 常量
intrinsics = [attr for attr in dir(_opcode) if attr.startswith('INTRINSIC')]
print(f"\n=== All INTRINSIC constants ===")
for attr in sorted(intrinsics):
    print(f"{attr} = {getattr(_opcode, attr)}")
