import subprocess
import sys

print(f"Current Python version: {sys.version}")

# 检查 Python 3.13 是否可用
try:
    result = subprocess.run(['python3.13', '--version'], capture_output=True, text=True)
    print(f"Python 3.13 version: {result.stdout.strip()}")
    use_python313 = True
except:
    print("Python 3.13 not available")
    use_python313 = False

# 使用当前 Python 检查操作码
import opcode
print(f"\n=== Python {sys.version_info.major}.{sys.version_info.minor} opcodes ===")
print(f"Opcode 107 name: {opcode.opname[107]}")
print(f"Opcode 55 name: {opcode.opname[55]}")

# 检查 _opcode 模块
import _opcode
intrinsics = [attr for attr in dir(_opcode) if attr.startswith('INTRINSIC')]
print(f"\nINTRINSIC constants: {intrinsics}")

# 检查是否有 SET_UPDATE
if hasattr(opcode, '_opcode_metadata'):
    print(f"\n_opcode_metadata available")
