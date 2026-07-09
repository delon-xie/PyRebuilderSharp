import marshal
import dis

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                print(f"co_varnames: {d.co_varnames}")
                print(f"co_cellvars: {d.co_cellvars}")
                print(f"co_freevars: {d.co_freevars}")
                print(f"len(varnames) = {len(d.co_varnames)}")
                print(f"len(cellvars) = {len(d.co_cellvars)}")
                print(f"len(freevars) = {len(d.co_freevars)}")
                
                # 手动分析字节码中的索引
                code = bytes(d.co_code)
                print("\n=== 关键指令分析 ===")
                for i in range(0, len(code), 2):
                    op = code[i]
                    arg = code[i+1] if i+1 < len(code) else 0
                    
                    # 只关注关键指令
                    if op in [62, 83, 84, 85]:  # DELETE_DEREF, LOAD_DEREF, LOAD_FAST, LOAD_FAST_AND_CLEAR
                        opname = {62: 'DELETE_DEREF', 83: 'LOAD_DEREF', 84: 'LOAD_FAST', 85: 'LOAD_FAST_AND_CLEAR'}.get(op, f'UNKNOWN_{op}')
                        print(f'0x{i:04X}: {opname:25} arg={arg}')
                break
        break
