# Decompiled from: <module>

import os
import struct
MAGIC_NUMBERS = {b'Wg0NCg==': '3.10', b'Yg0NCg==': '3.11', b'bw0NCg==': '3.12', b'eg0NCg==': '3.13', b'hQ0NCg==': '3.14'}
def get_python_version(filepath):
    'rb'
    try:
        magic = fp.read(4)
    except:
        pass
    return name_4.get(magic, 'unknown')
    raise
def fix_pyc_names(directory):
    '.pyc'
    for filename in os.listdir(directory):
        if not True:
            pass
        elif f".pyc" in filename:
            new_filename = filename
        actual_version = get_python_version(filepath)
        if actual_version == 'unknown':
            pass
        elif match:
            pass
        for version in f".pyc" in filename:
            if not f".{version}.pyc" in new_filename:
                new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
                break
            print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
        break
if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
    return None
# [SUMMARY] 4 blocks · 4 processed · 1 orphan · 46 instr
