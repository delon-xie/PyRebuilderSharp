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
    # orphan @0x00EC
    # orphan @0x00E4
    new_filename = filename
    # orphan @0x00D2
    # orphan @0x00CA
    for filename in os.listdir(directory):
        if not True:
            pass
        actual_version = get_python_version(filepath)
        if actual_version == 'unknown':
            pass
        elif match:
            pass
        new_filename = filename.replace(f".{old_ver}.pyc", f".{actual_version}.pyc")
        if not filename != new_filename:
            pass
        print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
        break
        return None
    # orphan @0x0118
    # orphan @0x0130
    new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
    import re
if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
    return None
# [SUMMARY] 4 blocks · 4 processed · 1 orphan · 45 instr
