"""Check marshal structure of 3.11 .pyc file"""
import marshal, dis, struct

# Manual header skip for 3.11+
with open('test_data/compiled/abc.3.11.pyc', 'rb') as f:
    magic = f.read(4)
    flags = struct.unpack('<I', f.read(4))[0]
    ts = struct.unpack('<I', f.read(4))[0]  # timestamp
    size = struct.unpack('<I', f.read(4))[0]  # source size
    print(f"Header: magic={magic.hex()} flags={flags} ts={ts} size={size}")
    
    code = marshal.load(f)
    print(f"\nTop-level code object:")
    print(f"  argcount={code.co_argcount}")
    print(f"  nlocals={code.co_nlocals}")
    print(f"  stacksize={code.co_stacksize}")
    print(f"  flags={code.co_flags}")
    print(f"  code_len={len(code.co_code)}")
    print(f"  consts={len(code.co_consts)} items")
    print(f"  names={len(code.co_names)} items")
    print(f"  varnames={len(code.co_varnames)} items")
    print(f"  freevars={len(code.co_freevars)} items")
    print(f"  cellvars={len(code.co_cellvars)} items")
    print(f"  filename={code.co_filename}")
    print(f"  name={code.co_name}")
    print(f"  firstlineno={code.co_firstlineno}")
    
    # List nested code objects
    for i, c in enumerate(code.co_consts):
        if hasattr(c, 'co_code'):
            print(f"\n  Const[{i}]: <code {c.co_name} @ 0x{c.co_firstlineno:x}> flags=0x{c.co_flags:x}")
            print(f"    arg={c.co_argcount} nlocals={c.co_nlocals} stack={c.co_stacksize}")
            print(f"    consts={len(c.co_consts)} names={len(c.co_names)}")
            # Check for deeper nesting
            for j, cc in enumerate(c.co_consts):
                if hasattr(cc, 'co_code'):
                    print(f"      Const[{j}]: <code {cc.co_name}>")
    
    # Show first few instructions
    print(f"\nFirst 10 instructions:")
    for i, instr in enumerate(dis.get_instructions(code)):
        print(f"  {instr.offset:4d}: {instr.opname:<20s} {instr.argrepr}")
        if i >= 10: break
