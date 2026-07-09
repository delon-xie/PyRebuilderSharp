import sys
print(f'Python version: {sys.version}')

# 检查当前 Python (3.14) 的操作码值
import opcode
print(f"\n=== Python {sys.version_info.major}.{sys.version_info.minor} opcodes ===")
print(f"DELETE_DEREF: {opcode.opmap.get('DELETE_DEREF', 'not found')}")
print(f"LOAD_DEREF: {opcode.opmap.get('LOAD_DEREF', 'not found')}")
print(f"STORE_DEREF: {opcode.opmap.get('STORE_DEREF', 'not found')}")
print(f"LOAD_FAST_AND_CLEAR: {opcode.opmap.get('LOAD_FAST_AND_CLEAR', 'not found')}")
print(f"SET_UPDATE: {opcode.opmap.get('SET_UPDATE', 'not found')}")

# 查看完整的操作码映射
print("\n=== 操作码值对比 ===")
for opname, opval in opcode.opmap.items():
    if 'DEREF' in opname or 'SET_UPDATE' in opname or 'FAST_AND_CLEAR' in opname:
        print(f"  {opname:25} = {opval}")
