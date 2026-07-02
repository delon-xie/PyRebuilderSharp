import marshal

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                for w in d.co_consts:
                    if hasattr(w, 'co_name') and w.co_name == 'wrapper':
                        print('=== wrapper code info ===')
                        print(f'co_code len: {len(w.co_code)}')
                        print(f'co_code: {[hex(b) for b in w.co_code]}')
                        et = getattr(w, 'co_exceptiontable', None)
                        print(f'exception table: {et}')
                        if et:
                            print(f'et bytes: {[hex(b) for b in et]}')
                        print(f'co_names: {w.co_names}')
                        print(f'co_varnames: {w.co_varnames}')
                        print(f'co_lnotab: {w.co_lnotab}')
                        break
                break
        break
