import subprocess

# 获取 Python 3.13 的操作码定义
result = subprocess.run(
    ['python3', '-c', '''
import opcode
for i, name in enumerate(opcode.opname):
    if name and name != 'UNUSED':
        print(f"{i}: {name}")
'''],
    capture_output=True, text=True
)

print("Python 3.14 opcodes (for reference):")
print(result.stdout[:2000])
