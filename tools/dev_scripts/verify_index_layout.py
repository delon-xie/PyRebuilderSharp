import marshal

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                print(f"=== decorating_function ===")
                print(f"co_varnames: {d.co_varnames} (count={len(d.co_varnames)})")
                print(f"co_cellvars: {d.co_cellvars} (count={len(d.co_cellvars)})")
                print(f"co_freevars: {d.co_freevars} (count={len(d.co_freevars)})")
                
                # 检查 wrapper 函数
                for const in d.co_consts:
                    if hasattr(const, 'co_name') and const.co_name == 'wrapper':
                        print(f"\n=== wrapper ===")
                        print(f"co_varnames: {const.co_varnames}")
                        print(f"co_cellvars: {const.co_cellvars}")
                        print(f"co_freevars: {const.co_freevars}")
                        break
                break
        break
