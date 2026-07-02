import marshal

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                code = bytes(d.co_code)
                print(f"=== decorating_function 字节码解析（前 40 字节）===")
                i = 0
                while i < min(40, len(code)):
                    op = code[i]
                    arg = code[i+1] if i+1 < len(code) else 0
                    print(f'0x{i:04X}: op={op:3d}, arg={arg:3d}')
                    
                    # 检查是否是扩展指令
                    if op == 71:  # EXTENDED_ARG
                        i += 4
                    else:
                        i += 2
                break
        break

print(f"\n=== co_names ===")
for i, name in enumerate(d.co_names):
    print(f"  [{i}] {name}")
