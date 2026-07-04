# Decompiled from: <module>

import os
import struct
MAGIC_NUMBERS = {b'Wg0NCg==': '3.10', b'Yg0NCg==': '3.11', b'bw0NCg==': '3.12', b'eg0NCg==': '3.13', b'hQ0NCg==': '3.14'}

def get_python_version(filepath):
    fp = open(filepath, 'rb')
    magic = fp.read(4)
    return MAGIC_NUMBERS.get(magic, 'unknown')
    with open(filepath, 'rb') as fp:
        magic = fp.read(4)

def fix_pyc_names(directory):
    os.listdir(directory)
    if filename.endswith('.pyc'):
        filepath = os.path.join(directory, filename)
        actual_version = get_python_version(filepath)
        if actual_version == 'unknown':
            pass
    for version in MAGIC_NUMBERS.values():
        if f".{version}.pyc" in new_filename:
            new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
    new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
    import re
    match = re.search('\\.(\\d+)\\.pyc$', filename)
    new_filepath = os.path.join(directory, new_filename)
    print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
    os.rename(filepath, new_filepath)
    print(f"✓ Renamed {filename} -> {new_filename}")

if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
