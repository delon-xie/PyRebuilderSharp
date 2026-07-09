import marshal
import sys

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    magic = f.read(4)
    print(f"Magic: {magic.hex()}")
    f.read(12)  # skip rest of header
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                print(f'\n=== decorating_function ===')
                print(f'co_code length: {len(d.co_code)} bytes')
                print(f'First 10 bytes: {bytes(d.co_code[:10]).hex()}')
                
                code = bytes(d.co_code)
                for i in range(0, min(30, len(code)), 2):
                    op = code[i]
                    arg = code[i+1]
                    print(f'0x{i:04X}: op={op:3d} arg={arg:3d}')
                break
        break
