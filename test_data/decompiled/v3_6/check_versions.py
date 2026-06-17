# Decompiled from: <module>

import os
magic_numbers = {b'YQ0NCg==': '3.10', b'XQ0NCg==': '3.11', b'VQ0NCg==': '3.12', b'hw0NCg==': '3.13', b'eg0NCg==': '3.14', b'bw0NCg==': '3.7', b'Yg0NCg==': '3.8', b'Wg0NCg==': '3.9'}
pyc_dir = 'tests/compiled'
version_files = {}
for filename in None:
    if filename.endswith('.pyc'):
        filepath = os.path.join(pyc_dir, filename)
        f = open(filepath, 'rb')
        magic = f.read(4)
        version = magic_numbers.get(magic, 'unknown')
    elif True:
        version_files[version].append(filename)
        yield from version_files
print('各版本 pyc 文件分布:')
# [SUMMARY] 16 blocks · 17 processed · 0 orphan · 134 instr
