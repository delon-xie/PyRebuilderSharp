import dis, sys

# Just use the dis module directly - it handles .pyc headers internally
for ver in ['3.10', '3.11', '3.12', '3.13', '3.14']:
    path = f'test_data/compiled/abc.{ver}.pyc'
    try:
        with open(path, 'rb') as f:
            raw = f.read()
        
        import importlib.util
        # Can't use importlib for .pyc, so use dis.dis directly
        code_obj = dis.code_info(raw)
        # Actually, let's just try loading via importlib._bootstrap_external
        code = compile(raw, f'abc.{ver}.pyc', 'exec')
        print(f"abc.{ver}.pyc: {len(code.co_code)} bytes")
    except Exception as e:
        print(f"abc.{ver}.pyc: error: {e}")
