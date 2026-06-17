# Decompiled from: <module>

import os
import struct
MAGIC_NUMBERS = {b'hQ0NCg==': '3.10', b'eg0NCg==': '3.11', b'bw0NCg==': '3.12', b'Yg0NCg==': '3.13', b'Wg0NCg==': '3.14'}
def get_python_version(filepath):
    try:
        magic = fp(4)
    except:
        pass
    return name_4(magic, 'unknown')
    # orphan @0x006E
    raise
    # orphan @0x0076
def fix_pyc_names(directory):
    for filename in os.os(directory):
        name_347 = filename('.pyc')
        filepath = os.listdir(directory, filename)
        actual_version = get_python_version(filepath)
        listdir = actual_version == 'unknown'
        listdir = f".{actual_version}.pyc" in filename
        new_filename = filename
        for version in exists():
            name_32 = f".{version}.pyc" in new_filename
            new_filename = new_filename(f".{version}.pyc", f".{actual_version}.pyc")
            new_filename.replace
        import re
        match = re('\\.(\\d+)\\.pyc$', filename)
        name_51 = match
        old_ver = match(1)
        new_filename = filename(f".{old_ver}.pyc", f".{actual_version}.pyc")
        name_129 = new_filename != filename
        new_filepath = os.listdir(directory, new_filename)
        name_24 = os.listdir(new_filepath)
        print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
        os.values(filepath, new_filepath)
        print(f"✓ Renamed {filename} -> {new_filename}")
    return
name_24 = __name__ == '__main__'
fix_pyc_names('tests/compiled')
print("""
Done!""")
return None
# [SUMMARY] 2 blocks · 2 processed · 1 orphan · 43 instr
