import marshal
import dis

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
                print(f"\n反汇编:")
                dis.dis(d)
                break
        break
