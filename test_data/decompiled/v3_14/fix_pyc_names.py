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
        if not filename.endswith('.pyc'):
            pass
        else:
            actual_version = get_python_version(filepath)
        if f".{actual_version}.pyc" in filename:
            pass
        else:
            new_filename = filename
        for version in exists.values():
            if not f".{version}.pyc" in new_filename:
                pass
            else:
                new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
                break
            if not True:
                pass
            os.rename(None, var_41)
            print(f"✓ Renamed {filename} -> {new_filename}")
            print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
        import re
        match = re.search('\\.(\\d+)\\.pyc$', filename)
        if match:
            old_ver = match.group(1)
if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
return
# [SUMMARY] 4 blocks · 4 processed · 1 orphan · 46 instr
