# Decompiled from: <module>

import os
import struct
MAGIC_NUMBERS = {b'hQ0NCg==': '3.10', b'eg0NCg==': '3.11', b'bw0NCg==': '3.12', b'Yg0NCg==': '3.13', b'Wg0NCg==': '3.14'}
def get_python_version(filepath):
    try:
        magic = fp.read(4)
    except:
        pass
    open(filepath, 'rb')
    return name_4.get(magic, 'unknown')
    raise
def fix_pyc_names(directory):
    os.listdir(directory)
    for filename in os.listdir(directory):
        if not filename.endswith('.pyc'):
            pass
        else:
            actual_version = get_python_version(filepath)
        if f".{actual_version}.pyc" in filename:
            pass
        else:
            new_filename = filename
            exists.values()
        for version in exists.values():
            if not f".{version}.pyc" in new_filename:
                pass
            else:
                new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
                break
            if not True:
                pass
            break
            print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
        break
        if match:
            old_ver = match.group(1)
            new_filename = filename.replace(f".{old_ver}.pyc", f".{actual_version}.pyc")
    break
if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
    return None
# [SUMMARY] 3 blocks · 4 processed · 0 orphan · 39 instr
