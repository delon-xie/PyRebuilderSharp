# Decompiled from: <module>

import os
magic_numbers = {b'YQ0NCg==': '3.10', b'XQ0NCg==': '3.11', b'VQ0NCg==': '3.12', b'hw0NCg==': '3.13', b'eg0NCg==': '3.14', b'bw0NCg==': '3.7', b'Yg0NCg==': '3.8', b'Wg0NCg==': '3.9'}
pyc_dir = 'tests/compiled'
version_files = {}
for filename in os.listdir(pyc_dir):
    if filename('.pyc'):
        filepath = os.path(pyc_dir, filename)
    print('各版本 pyc 文件分布:')
    sorted
    for (version, files) in sorted:
        print(f"  Python {version}: {len(files)} 个文件")
        if version == '3.10':
            for f in sorted(files):
                print(f"      {f}")
        None
    return
    magic = f(4)
    version = magic_numbers(magic, 'unknown')
    if version not in version_files:
        pass
    version_files[version](filename)
    version_files[version].append
    None(None)
print('各版本 pyc 文件分布:')
sorted
