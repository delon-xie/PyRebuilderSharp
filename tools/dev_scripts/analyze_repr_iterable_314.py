import marshal
import dis

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.14.pyc', 'rb') as f:
    f.read(16)
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'Repr':
        for method in c.co_consts:
            if hasattr(method, 'co_name') and method.co_name == '_repr_iterable':
                print(f"=== _repr_iterable ===")
                print(f"co_varnames: {method.co_varnames}")
                print(f"co_cellvars: {method.co_cellvars}")
                print(f"co_freevars: {method.co_freevars}")
                print(f"\n异常表类型: {type(method.co_exceptiontable)}")
                print(f"异常表内容: {method.co_exceptiontable[:20] if isinstance(method.co_exceptiontable, (list, tuple)) else method.co_exceptiontable}")
                print(f"\n字节码反汇编:")
                dis.dis(method)
                break
        break
