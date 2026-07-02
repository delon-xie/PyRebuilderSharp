import marshal
import opcode

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                for e in d.co_consts:
                    if hasattr(e, 'co_name') and e.co_name == 'wrapper':
                        print('=== wrapper 函数 (Python 3.13) ===')
                        print(f'co_varnames: {e.co_varnames}')
                        print(f'co_cellvars: {e.co_cellvars}')
                        print(f'co_freevars: {e.co_freevars}')
                        print(f'len(varnames): {len(e.co_varnames)}')
                        print(f'len(cellvars): {len(e.co_cellvars)}')
                        print(f'len(freevars): {len(e.co_freevars)}')
                        
                        code = bytes(e.co_code)
                        print(f'\n=== wrapper 变量访问指令 ===')
                        
                        for i in range(0, len(code), 2):
                            op = code[i]
                            arg = code[i+1] if i+1 < len(code) else 0
                            opname = opcode.opname[op] if op < len(opcode.opname) else f'UNKNOWN_{op}'
                            
                            if opname in ['LOAD_FAST_AND_CLEAR', 'LOAD_FAST', 'STORE_FAST', 
                                         'LOAD_DEREF', 'STORE_DEREF', 'DELETE_DEREF',
                                         'COPY_FREE_VARS']:
                                print(f'0x{i:04X}: {opname:25} arg={arg:3d}')
                        break
                break
        break
