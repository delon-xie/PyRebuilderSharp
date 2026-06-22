# Decompiled from: <module>

with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as f:
    f.write(src)
    py_path = f.name
