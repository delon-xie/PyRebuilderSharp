import dis, marshal, sys

for ver in ['3.10', '3.11', '3.12', '3.13', '3.14']:
    try:
        path = f'test_data/compiled/abc.{ver}.pyc'
        with open(path, 'rb') as f:
            magic = f.read(4)
            f.read(4)  # flags
            timestamp = int.from_bytes(f.read(4), 'little')
            size = int.from_bytes(f.read(4), 'little')
            if ver in ('3.11', '3.12', '3.13', '3.14'):
                # 3.11+ has 4 more bytes for hash
                hash_bytes = f.read(4)
            code = marshal.load(f)
            n_instrs = len(code.co_code) // 2  # 3.11+ uses 2-byte instructions
            if ver == '3.10':
                n_instrs = len(code.co_code) // 2
            print(f"abc.{ver}.pyc: OK, {n_instrs} instrs, {len(code.co_code)} raw bytes, {len(code.co_consts)} consts")
            if code.co_consts:
                c0 = code.co_consts[0]
                print(f"  Const[0]: {c0!r:.80}")
    except Exception as e:
        print(f"abc.{ver}.pyc: FAILED: {e}")
