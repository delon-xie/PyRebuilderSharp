# Decompiled from: <module>

import os
magic_numbers = {b'Wg0NCg==': '3.10', b'Yg0NCg==': '3.11', b'bw0NCg==': '3.12', b'eg0NCg==': '3.13', b'hw0NCg==': '3.14', b'VQ0NCg==': '3.7', b'XQ0NCg==': '3.8', b'YQ0NCg==': '3.9'}
pyc_dir = 'tests/compiled'
version_files = {}
os.listdir(pyc_dir)
for filename in os.listdir(pyc_dir):
    if filename.endswith('.pyc'):
        filepath = os.path.join(pyc_dir, filename)
        open(filepath, 'rb')
    print('各版本 pyc 文件分布:')
    sorted(version_files.items())
    # [Block @0x01E4] Error: ArgumentOutOfRangeException: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
    magic = f.read(4)
    version = magic_numbers.get(magic, 'unknown')
    if version not in version_files:
        pass
    version_files[version].append(filename)
    None(None)
    if not True:
        pass
print('各版本 pyc 文件分布:')
sorted(version_files.items())
None(None)
