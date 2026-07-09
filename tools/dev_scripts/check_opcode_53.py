import marshal

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                code = bytes(d.co_code)
                # 查看前 30 个字节
                print(f"=== First 30 bytes ===")
                for i in range(0, min(30, len(code)), 2):
                    op = code[i]
                    arg = code[i+1] if i+1 < len(code) else 0
                    print(f'0x{i:04X}: op={op}, arg={arg}')
                break
        break
