import marshal

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                code = bytes(d.co_code)
                # 找到 opcode 107
                for i in range(0, len(code), 2):
                    op = code[i]
                    arg = code[i+1] if i+1 < len(code) else 0
                    if op == 107:
                        print(f'Found opcode 107 at offset 0x{i:04X}, arg={arg}')
                        # 查看前后的指令
                        start = max(0, i-6)
                        end = min(len(code), i+14)
                        for j in range(start, end, 2):
                            op_j = code[j]
                            arg_j = code[j+1] if j+1 < len(code) else 0
                            print(f'  0x{j:04X}: op={op_j}, arg={arg_j}')
                break
        break
