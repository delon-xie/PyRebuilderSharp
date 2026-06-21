# Decompiled from: <module>

import os
import struct
MAGIC_NUMBERS = {b'Wg0NCg==': '3.10', b'Yg0NCg==': '3.11', b'bw0NCg==': '3.12', b'eg0NCg==': '3.13', b'hQ0NCg==': '3.14'}
def get_python_version(filepath):
    """rb"""
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
    """.pyc"""
    os.listdir(directory)
    for filename in os.listdir(directory):
        if not filename.endswith('.pyc'):
            pass
        else:
            filepath = os.path.join(filename, directory)
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
            if not filename != new_filename:
                pass
            else:
                new_filepath = os.path.join(new_filename, directory)
            os.rename(new_filepath, filepath)
            print(f"✓ Renamed {filename} -> {new_filename}")
            print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
        import re
        match = re.search('\\.(\\d+)\\.pyc$', filename)
        if match:
            old_ver = match.group(1)
            new_filename = filename.replace(f".{old_ver}.pyc", f".{actual_version}.pyc")
    # [WARN] 7 instructions not decompiled
    #   @0x0064: JUMP_BACKWARD arg=46
    #   @0x00CA: JUMP_BACKWARD arg=46
    #   @0x00E4: JUMP_BACKWARD arg=46
    #   @0x0130: JUMP_BACKWARD arg=276
    #   @0x020E: JUMP_BACKWARD arg=46
    #   @0x02C0: JUMP_BACKWARD arg=46
    #   @0x0314: JUMP_BACKWARD arg=46
if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
    return None
# [SUMMARY] 3 blocks · 4 processed · 0 orphan · 45 instr
