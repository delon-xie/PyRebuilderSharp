import marshal
import opcode

# 读取 Python 3.13 的 reprlib.pyc
with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                print('=== decorating_function (Python 3.13) ===')
                print(f'co_varnames: {d.co_varnames}')
                print(f'co_cellvars: {d.co_cellvars}')
                print(f'co_freevars: {d.co_freevars}')
                print(f'len(varnames): {len(d.co_varnames)}')
                print(f'len(cellvars): {len(d.co_cellvars)}')
                print(f'len(freevars): {len(d.co_freevars)}')
                
                # 分析字节码，找到所有涉及变量访问的指令
                code = bytes(d.co_code)
                print(f'\n=== 变量访问指令分析 ===')
                
                for i in range(0, len(code), 2):
                    op = code[i]
                    arg = code[i+1] if i+1 < len(code) else 0
                    opname = opcode.opname[op] if op < len(opcode.opname) else f'UNKNOWN_{op}'
                    
                    if opname in ['LOAD_FAST_AND_CLEAR', 'LOAD_FAST', 'STORE_FAST', 
                                 'LOAD_DEREF', 'STORE_DEREF', 'DELETE_DEREF']:
                        print(f'0x{i:04X}: {opname:25} arg={arg:3d}')
                
                # 检查是否有 MAKE_CELL 指令
                print(f'\n=== MAKE_CELL 指令 ===')
                for i in range(0, len(code), 2):
                    op = code[i]
                    arg = code[i+1] if i+1 < len(code) else 0
                    opname = opcode.opname[op] if op < len(opcode.opname) else f'UNKNOWN_{op}'
                    
                    if opname == 'MAKE_CELL':
                        print(f'0x{i:04X}: {opname:25} arg={arg:3d}')
                break
        break
