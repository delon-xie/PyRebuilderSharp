import dis
import opcode

print("=== Python version:", __import__('sys').version)
print("\n=== opcode 94 name:", opcode.opname[94])

# 检查所有操作码名称
print("\n=== All opcode names ===")
for i in range(len(opcode.opname)):
    if opcode.opname[i][0] != '<':
        print(f"{i:3d}: {opcode.opname[i]}")
