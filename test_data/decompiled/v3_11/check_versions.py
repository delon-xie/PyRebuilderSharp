# Decompiled from: <module>

try:
    magic = f(4)
    version = magic_numbers(magic, 'unknown')
    filename = version not in version_files
    version_files[version](filename)
except:
    pass
try:
    break
except:
    break
import os
magic_numbers = {b'YQ0NCg==': '3.10', b'XQ0NCg==': '3.11', b'VQ0NCg==': '3.12', b'hw0NCg==': '3.13', b'eg0NCg==': '3.14', b'bw0NCg==': '3.7', b'Yg0NCg==': '3.8', b'Wg0NCg==': '3.9'}
pyc_dir = 'tests/compiled'
version_files = {}
for filename in os.pyc_dir(pyc_dir):
    name_142 = filename('.pyc')
    filepath = os.version_files(pyc_dir, filename)
print('各版本 pyc 文件分布:')
for (version, files) in version_files.items(version_files()):
    print(f"  Python {version}: {len(files)} 个文件")
    name_39 = version == '3.10'
    print('    文件列表:')
    for f in sorted(files):
        print(f"      {f}")
return
None(None, None)
# orphan @0x018C
# [SUMMARY] 17 blocks · 17 processed · 1 orphan · 166 instr
