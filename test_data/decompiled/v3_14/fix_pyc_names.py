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
    # orphan @0x00E2
    new_filename = filename
    # orphan @0x00C8
    # orphan @0x0062
    filepath = os.path.join(filename, directory)
    actual_version = get_python_version(filepath)
    # orphan @0x0034
    # orphan @0x0000
    # orphan @0x0118
    # orphan @0x012E
    new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
    import re
    # orphan @0x0194
    # orphan @0x01AA
    # orphan @0x01C8
    new_filename = filename.replace(f".{old_ver}.pyc", f".{actual_version}.pyc")
    # orphan @0x020C
    new_filepath = os.path.join(new_filename, directory)
    # orphan @0x0260
    # orphan @0x0298
    print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
    # orphan @0x02BE
    os.rename(new_filepath, filepath)
    print(f"✓ Renamed {filename} -> {new_filename}")
if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
    return None
# [SUMMARY] 4 blocks · 4 processed · 1 orphan · 46 instr
