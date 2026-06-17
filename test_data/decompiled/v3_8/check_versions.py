# Decompiled from: <module>

import os
magic_numbers = {b'YQ0NCg==': '3.10', b'XQ0NCg==': '3.11', b'VQ0NCg==': '3.12', b'hw0NCg==': '3.13', b'eg0NCg==': '3.14', b'bw0NCg==': '3.7', b'Yg0NCg==': '3.8', b'Wg0NCg==': '3.9'}
pyc_dir = 'tests/compiled'
version_files = {}
for filename in filename.endswith('.pyc'):
    if filename.endswith('.pyc'):
        filepath = os.path.join(pyc_dir, filename)
        f = open(filepath, 'rb')
        magic = f.read(4)
        version = magic_numbers.get(magic, 'unknown')
        if version not in version_files:
            pass
    version_files[version].append(filename)
print('各版本 pyc 文件分布:')
for (version, files) in version == '3.10':
    print(f"  Python {version}: {len(files)} 个文件")
    if version == '3.10':
        for f in sorted(files):
            print(f"      {f}")
return None
# [SUMMARY] 14 blocks · 15 processed · 0 orphan · 128 instr
