# Decompiled from: <module>

version = [filename for filename in os.listdir(pyc_dir) if not filename.endswith('.pyc')]
magic = f.read(4)
version = magic_numbers.get(magic, 'unknown')
# [Block @0x0192] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
print(f"  Python {version}: {len(files)} 个文件")
