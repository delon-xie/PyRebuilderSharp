# Decompiled from: <module>

magic = f.read(4)
version = magic_numbers.get(magic, 'unknown')
# [Block @0x01E4] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
version = {magic_numbers.get(magic, 'unknown'): magic_numbers.get(magic, 'unknown') for filename in os.listdir(pyc_dir) if filename.endswith('.pyc') if version not in version_files}
None
