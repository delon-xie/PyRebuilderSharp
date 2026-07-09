import struct
import marshal

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    magic = f.read(4)
    print(f"Magic: {magic.hex()}")
    
    # PEP 552 header (16 bytes total)
    flags = struct.unpack('<I', f.read(4))[0]
    print(f"Flags: {flags:#010x}")
    
    timestamp = struct.unpack('<Q', f.read(8))[0]
    print(f"Timestamp: {timestamp}")
    
    code_obj = marshal.load(f)
    print(f"\n=== Module code object ===")
    print(f"co_name: {code_obj.co_name}")
    print(f"co_argcount: {code_obj.co_argcount}")
    print(f"co_code length: {len(code_obj.co_code)}")
    
    for c in code_obj.co_consts:
        if hasattr(c, 'co_name') and c.co_name == 'recursive_repr':
            print(f"\n=== recursive_repr ===")
            print(f"co_code length: {len(c.co_code)}")
            print(f"First instruction: op={c.co_code[0]}, arg={c.co_code[1]}")
            
            for d in c.co_consts:
                if hasattr(d, 'co_name') and d.co_name == 'decorating_function':
                    print(f"\n=== decorating_function ===")
                    print(f"co_code length: {len(d.co_code)}")
                    print(f"First instruction: op={d.co_code[0]}, arg={d.co_code[1]}")
                    
                    # Check if first instruction is RESUME (op=149)
                    if d.co_code[0] == 149:
                        print("Has RESUME at start")
                    else:
                        print(f"No RESUME at start! First op is {d.co_code[0]}")
                    break
            break
