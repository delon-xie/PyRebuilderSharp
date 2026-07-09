import marshal
import opcode

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                print('=== decorating_function 信息 ===')
                print(f'co_varnames: {d.co_varnames}')
                print(f'co_cellvars: {d.co_cellvars}')
                print(f'co_freevars: {d.co_freevars}')
                print(f'co_names: {d.co_names}')
                print(f'co_consts: {d.co_consts}')
                
                code = bytes(d.co_code)
                print(f'\n=== 字节码 (前 100 字节) ===')
                for i in range(0, min(100, len(code)), 2):
                    op = code[i]
                    arg = code[i+1] if i+1 < len(code) else 0
                    opname = opcode.opname[op] if op < len(opcode.opname) else f'UNKNOWN_{op}'
                    print(f'0x{i:04X}: {opname:25} {arg:3d}')
                break
        break
