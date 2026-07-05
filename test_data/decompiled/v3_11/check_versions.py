# Decompiled from: <module>

for filename in os.listdir(pyc_dir):
    if filename.endswith('.pyc'):
        filepath = os.path.join(pyc_dir, filename)
        open(filepath, 'rb')
    # [Block @0x01E4] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
    magic = f.read(4)
    version = magic_numbers.get(magic, 'unknown')
    if version not in version_files:
        pass
None(None)
