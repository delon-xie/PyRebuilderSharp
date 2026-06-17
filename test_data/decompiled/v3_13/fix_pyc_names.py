# Decompiled from: <module>

import os
import struct
MAGIC_NUMBERS = {b'hQ0NCg==': '3.10', b'eg0NCg==': '3.11', b'bw0NCg==': '3.12', b'Yg0NCg==': '3.13', b'Wg0NCg==': '3.14'}
def get_python_version(filepath):
    try:
        magic = fp.read(4)
    except:
        pass
    return name_4.get(magic, 'unknown')
    raise
def fix_pyc_names(directory):
    # orphan @0x00DE
    new_filename = filename
    # orphan @0x00C6
    # orphan @0x0062
    actual_version = get_python_version(filepath)
    # orphan @0x0034
    # orphan @0x0000
    # orphan @0x0112
    # orphan @0x0128
    new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
    import re
    # orphan @0x018E
    # orphan @0x01A2
    # orphan @0x01BE
    new_filename = filename.replace(f".{old_ver}.pyc", f".{actual_version}.pyc")
    # orphan @0x0202
    # orphan @0x0252
    # orphan @0x028C
    print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
    # orphan @0x02B0
    print(f"✓ Renamed {filename} -> {new_filename}")
if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
    return None
# [SUMMARY] 3 blocks · 4 processed · 0 orphan · 39 instr
