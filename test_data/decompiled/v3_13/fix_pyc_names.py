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
    os.listdir
    for filename in os.listdir:
        if not filename.endswith('.pyc'):
            os.path.join
        if f".{actual_version}.pyc" in filename:
            for version in exists.values():
                if not f".{version}.pyc" in new_filename:
                    new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
                    break
                if match:
                    match.group(1)
                elif not True:
                    os.path
                filename.replace
        get_python_version(filepath)
        if actual_version == 'unknown':
            pass
        print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
        break
if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
    return None
# [SUMMARY] 3 blocks · 3 processed · 1 orphan · 39 instr
