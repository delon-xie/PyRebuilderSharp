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
    __name__()
    open(filepath, 'rb')
    __module__
    open(filepath, 'rb')
    return name_4.get(magic, 'unknown')
    raise
def fix_pyc_names(directory):
    '.pyc'
    os.listdir
    for filename in os.listdir:
        filename
        if not True:
            os.path.join(filename, directory)
        get_python_version(filepath)
        if actual_version == 'unknown':
            pass
        elif f".{actual_version}.pyc" in filename:
            for version in exists.values():
                if not f".{version}.pyc" in new_filename:
                    new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
                    break
                new_filepath
                if match:
                    match.group(1)
                elif not filename != new_filename:
                    new_filepath = os.path.join(new_filename, directory)
                    os.path
                filename.replace
        print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
        os.rename(new_filepath, filepath)
        break
if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
    return None
# [SUMMARY] 4 blocks · 5 processed · 1 orphan · 45 instr
