import marshal

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                print(f"=== decorating_function ===")
                print(f"co_varnames: {d.co_varnames}")
                print(f"co_cellvars: {d.co_cellvars}")
                print(f"co_freevars: {d.co_freevars}")
                print(f"co_consts:")
                for i, const in enumerate(d.co_consts):
                    if hasattr(const, 'co_name'):
                        print(f"  [{i}] CodeObject: {const.co_name}")
                    else:
                        print(f"  [{i}] {type(const).__name__}: {const!r}")
                
                # 查找 wrapper 函数
                wrapper_code = None
                for const in d.co_consts:
                    if hasattr(const, 'co_name') and const.co_name == 'wrapper':
                        wrapper_code = const
                        break
                
                if wrapper_code:
                    print(f"\n=== wrapper function ===")
                    print(f"co_varnames: {wrapper_code.co_varnames}")
                    print(f"co_cellvars: {wrapper_code.co_cellvars}")
                    print(f"co_freevars: {wrapper_code.co_freevars}")
                
                break
        break
