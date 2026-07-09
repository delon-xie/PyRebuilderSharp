import dis, marshal, sys, struct

def skip_header(f):
    """Skip the .pyc header and return the marshal'd code object"""
    magic = f.read(4)
    flags = struct.unpack('<I', f.read(4))[0]
    
    # Python 3.7+ header format
    # bit 0 of flags: 0 = timestamp-based, 1 = hash-based
    hash_based = bool(flags & 1)
    
    if hash_based:
        f.read(8)  # source hash (SipHash)
    else:
        f.read(4)  # timestamp
    f.read(4)  # source size
    
    return marshal.load(f)

for ver in ['3.10', '3.11', '3.12', '3.13', '3.14']:
    path = f'test_data/compiled/abc.{ver}.pyc'
    with open(path, 'rb') as f:
        code = skip_header(f)
    
    print(f"\n=== abc.{ver}.pyc ===")
    print(f"  co_code: {len(code.co_code)} bytes")
    print(f"  co_consts: {len(code.co_consts)} entries")
    print(f"  co_names: {len(code.co_names)} entries")
    print(f"  co_varnames: {len(code.co_varnames)} entries")
    print(f"  co_nlocals: {code.co_nlocals}")
    print(f"  co_stacksize: {code.co_stacksize}")
    print(f"  co_flags: 0x{code.co_flags:x}")
    
    # Disassemble first 20 instructions
    print(f"  First instructions:")
    instructions = list(dis.get_instructions(code))
    for i, instr in enumerate(instructions[:10]):
        print(f"    {instr.offset:4d}: {instr.opname:<20s} {instr.argrepr}")
    if len(instructions) > 10:
        print(f"    ... ({len(instructions)} total)")
