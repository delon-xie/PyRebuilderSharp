# Decompiled from: <module>

import os
magic_numbers = {b'Wg0NCg==': '3.10', b'Yg0NCg==': '3.11', b'bw0NCg==': '3.12', b'eg0NCg==': '3.13', b'hw0NCg==': '3.14', b'VQ0NCg==': '3.7', b'XQ0NCg==': '3.8', b'YQ0NCg==': '3.9'}
pyc_dir = 'tests/compiled'
version_files = {}
os.listdir(pyc_dir)
version = [filename for filename in os.listdir(pyc_dir) if filename.endswith('.pyc')]
# [Block @0x00C0] Error: Index was out of range. Must be non-negative and less than the size of the collection. (Parameter 'index')
print(f"  Python {version}: {len(files)} 个文件")
print(f"      {f}")
