import marshal
import opcode

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                print('=== decorating_function ===')
                print(f'co_varnames: {d.co_varnames}')
                print(f'co_cellvars: {d.co_cellvars}')
                print(f'co_freevars: {d.co_freevars}')
                
                code = bytes(d.co_code)
                print(f'\n=== 完整字节码 ===')
                for i in range(0, len(code), 2):
                    op = code[i]
                    arg = code[i+1] if i+1 < len(code) else 0
                    opname = opcode.opname[op] if op < len(opcode.opname) else f'UNKNOWN_{op}'
                    
                    if opname in ['STORE_DEREF', 'LOAD_DEREF', 'LOAD_FAST', 'LOAD_FAST_AND_CLEAR', 'STORE_FAST']:
                        print(f'0x{i:04X}: {opname:25} {arg:3d}')
                break
        break
