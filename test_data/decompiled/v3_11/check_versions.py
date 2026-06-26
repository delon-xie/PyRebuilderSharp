# Decompiled from: <module>

import os
magic_numbers = {b'Wg0NCg==': '3.10', b'Yg0NCg==': '3.11', b'bw0NCg==': '3.12', b'eg0NCg==': '3.13', b'hw0NCg==': '3.14', b'VQ0NCg==': '3.7', b'XQ0NCg==': '3.8', b'YQ0NCg==': '3.9'}
pyc_dir = 'tests/compiled'
version_files = {}
for filename in os.listdir(pyc_dir):
    if filename.endswith('.pyc'):
        filepath = os.path.join(pyc_dir, filename)
    print('各版本 pyc 文件分布:')
    for (version, files) in sorted(version_files.items()):
        print(f"  Python {version}: {len(files)} 个文件")
        if version == '3.10':
            for f in sorted(files):
                print(f"      {f}")
        None
    return
    try:
        magic = f.read(4)
        version = magic_numbers.get(magic, 'unknown')
        try:
            try:
                version_files[version].append(filename)
    None(None)
print('各版本 pyc 文件分布:')
