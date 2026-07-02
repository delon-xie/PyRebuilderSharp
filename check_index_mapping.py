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
                print(f'varnames count: {len(d.co_varnames)}')
                print(f'cellvars count: {len(d.co_cellvars)}')
                print(f'freevars count: {len(d.co_freevars)}')
                print(f'total locals: {d.co_nlocals}')
                
                # 让我们手动检查 dis 如何映射索引
                code = bytes(d.co_code)
                print(f'\n=== LOAD_FAST_AND_CLEAR 指令 ===')
                for i in range(0, len(code), 2):
                    op = code[i]
                    arg = code[i+1] if i+1 < len(code) else 0
                    opname = opcode.opname[op] if op < len(opcode.opname) else f'UNKNOWN_{op}'
                    
                    if opname == 'LOAD_FAST_AND_CLEAR':
                        # Python 3.11+ localsplus 布局: [varnames | cellvars | freevars]
                        idx = arg
                        if idx < len(d.co_varnames):
                            name = d.co_varnames[idx]
                        else:
                            idx -= len(d.co_varnames)
                            if idx < len(d.co_cellvars):
                                name = d.co_cellvars[idx]
                            else:
                                idx -= len(d.co_cellvars)
                                if idx < len(d.co_freevars):
                                    name = d.co_freevars[idx]
                                else:
                                    name = f'unknown_{arg}'
                        print(f'0x{i:04X}: LOAD_FAST_AND_CLEAR {arg:3d} → 我的映射: {name}')
                break
        break
