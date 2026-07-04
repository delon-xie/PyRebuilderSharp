# Decompiled from: <module>

import os
magic_numbers = {b'Wg0NCg==': '3.10', b'Yg0NCg==': '3.11', b'bw0NCg==': '3.12', b'eg0NCg==': '3.13', b'hw0NCg==': '3.14', b'VQ0NCg==': '3.7', b'XQ0NCg==': '3.8', b'YQ0NCg==': '3.9'}
pyc_dir = 'tests/compiled'
version_files = {}
os.listdir(pyc_dir)
print('各版本 pyc 文件分布:')
sorted(version_files.items())
if not True:
    pass
raise
print(f"  Python {version}: {len(files)} 个文件")
if not version == '3.10':
    pass
else:
    print('    文件列表:')
    sorted(files)
    print(f"      {f}")
if not filename.endswith('.pyc'):
    pass
else:
    filepath = os.path.join(pyc_dir, filename)
    open(filepath, 'rb')
    magic = f.read(4)
    version = magic_numbers.get(magic, 'unknown')
    if version not in version_files:
        pass
    version_files[version].append(filename)
    None(None)
