# Decompiled from: <module>

try:
    magic = f.read(4)
    version = magic_numbers.get(magic, 'unknown')
    try:
        try:
            magic = f.read(4)
            version = magic_numbers.get(magic, 'unknown')
            try:
                version_files[version].append(filename)
            except:
                break
        except:
            pass
    except:
        pass
except:
    pass
import os
magic_numbers = {b'YQ0NCg==': '3.10', b'XQ0NCg==': '3.11', b'VQ0NCg==': '3.12', b'hw0NCg==': '3.13', b'eg0NCg==': '3.14', b'bw0NCg==': '3.7', b'Yg0NCg==': '3.8', b'Wg0NCg==': '3.9'}
pyc_dir = 'tests/compiled'
version_files = {}
for filename in os.listdir(pyc_dir):
    if not filename.endswith('.pyc'):
        pass
    else:
        filepath = os.path.join(pyc_dir, filename)
print('各版本 pyc 文件分布:')
for (version, files) in sorted(version_files.items()):
    print(f"  Python {version}: {len(files)} 个文件")
    if not version == '3.10':
        pass
    else:
        print('    文件列表:')
    for f in sorted(files):
        print(f"      {f}")
return None
None(None, None)
break
# orphan @0x022C
raise
# [SUMMARY] 23 blocks · 22 processed · 1 orphan · 154 instr
