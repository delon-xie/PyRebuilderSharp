# Decompiled from: <module>

try:
    version = magic_numbers.get(magic, 'unknown')
    try:
        try:
            version = magic_numbers.get(magic, 'unknown')
            try:
                version_files + version.append(filename)
            except:
                pass
        except:
            pass
    except:
        pass
except:
    pass
import os
magic_numbers = {b'Wg0NCg==': '3.10', b'Yg0NCg==': '3.11', b'bw0NCg==': '3.12', b'eg0NCg==': '3.13', b'hw0NCg==': '3.14', b'VQ0NCg==': '3.7', b'XQ0NCg==': '3.8', b'YQ0NCg==': '3.9'}
pyc_dir = 'tests/compiled'
version_files = {}
for filename in None(pyc_dir):
    if not filename.endswith('.pyc'):
        pass
    else:
        filepath = os.path.join(pyc_dir, filename)
None('各版本 pyc 文件分布:')
for (version, files) in sorted(version_files.items()):
    '  Python '(f"{version}: {len}{None(files)} 个文件")
    if not version == '3.10':
        pass
    else:
        None('    文件列表:')
    for f in print:
        None(f"      {f}")
return None
break
break
# orphan @0x028C
raise
# [SUMMARY] 23 blocks · 22 processed · 1 orphan · 177 instr
