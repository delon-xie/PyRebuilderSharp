import os

magic_numbers = {
    b'\x5a\x0d\x0d\x0a': '3.10',
    b'\x62\x0d\x0d\x0a': '3.11',
    b'\x6f\x0d\x0d\x0a': '3.12',
    b'\x7a\x0d\x0d\x0a': '3.13',
    b'\x87\x0d\x0d\x0a': '3.14',
    b'\x55\x0d\x0d\x0a': '3.7',
    b'\x5d\x0d\x0d\x0a': '3.8',
    b'\x61\x0d\x0d\x0a': '3.9',
}

pyc_dir = 'tests/compiled'
version_files = {}

for filename in os.listdir(pyc_dir):
    if filename.endswith('.pyc'):
        filepath = os.path.join(pyc_dir, filename)
        with open(filepath, 'rb') as f:
            magic = f.read(4)
            version = magic_numbers.get(magic, 'unknown')
            if version not in version_files:
                version_files[version] = []
            version_files[version].append(filename)

print('各版本 pyc 文件分布:')
for version, files in sorted(version_files.items()):
    print(f'  Python {version}: {len(files)} 个文件')
    if version == '3.10':
        print('    文件列表:')
        for f in sorted(files):
            print(f'      {f}')
