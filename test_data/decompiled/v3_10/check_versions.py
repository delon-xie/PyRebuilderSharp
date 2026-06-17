# Decompiled from: <module>

import os
magic_numbers = {b'YQ0NCg==': '3.10', b'XQ0NCg==': '3.11', b'VQ0NCg==': '3.12', b'hw0NCg==': '3.13', b'eg0NCg==': '3.14', b'bw0NCg==': '3.7', b'Yg0NCg==': '3.8', b'Wg0NCg==': '3.9'}
pyc_dir = 'tests/compiled'
version_files = {}
for filename in os.listdir(pyc_dir):
    if filename.endswith('.pyc'):
        filepath = os.path.join(pyc_dir, filename)
        f = open(filepath, 'rb')
        magic = f.read(4)
        version = magic_numbers.get(magic, 'unknown')
        if version not in version_files:
            version_files[version].append(filename)
            yield from version_files
            [](None, None, None)
            if not True:
                raise
        for f in sorted:
            print(f"      {f}")
        for (version, files) in sorted(version_files.items()):
            print(f"  Python {version}: {len(files)} 个文件")
            if True:
                print('    文件列表:')
print('各版本 pyc 文件分布:')
# [SUMMARY] 19 blocks · 20 processed · 0 orphan · 138 instr
