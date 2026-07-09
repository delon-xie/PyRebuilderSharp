import marshal

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)  # skip header
    code_obj = marshal.load(f)

for c in code_obj.co_consts:
    if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
        for d in c.co_consts:
            if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                print(f"=== decorating_function ===")
                print(f"co_varnames: {d.co_varnames}")
                print(f"co_cellvars: {d.co_cellvars}")
                print(f"co_freevars: {d.co_freevars}")
                print(f"len(varnames): {len(d.co_varnames)}")
                print(f"len(cellvars): {len(d.co_cellvars)}")
                print(f"len(freevars): {len(d.co_freevars)}")
                print(f"\nco_names: {d.co_names}")
                
                # Analyze bytecode around STORE_DEREF
                code = bytes(d.co_code)
                print(f"\nBytecode around STORE_DEREF (op=109):")
                for i in range(0, len(code), 2):
                    op = code[i]
                    arg = code[i+1]
                    if op == 109:
                        print(f'0x{i:04X}: op={op:3d} arg={arg:3d} (STORE_DEREF)')
                        
                        # Show context
                        for j in range(max(0, i-6), min(len(code), i+8), 2):
                            ctx_op = code[j]
                            ctx_arg = code[j+1]
                            marker = "←" if j == i else ""
                            print(f'  0x{j:04X}: op={ctx_op:3d} arg={ctx_arg:3d} {marker}')
                        print()
                break
        break
