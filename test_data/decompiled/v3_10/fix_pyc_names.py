# Decompiled from: <module>

import os
import struct
MAGIC_NUMBERS = {b'hQ0NCg==': '3.10', b'eg0NCg==': '3.11', b'bw0NCg==': '3.12', b'Yg0NCg==': '3.13', b'Wg0NCg==': '3.14'}
def get_python_version(filepath):
    with open(filepath, 'rb') as fp:
        magic = fp.read(4)
        raise
        return MAGIC_NUMBERS.get(magic, 'unknown')
    # orphan @0x0052
def fix_pyc_names(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pyc'):
            filepath = os.path.join(directory, filename)
            actual_version = get_python_version(filepath)
            if actual_version == 'unknown':
                continue
                if f".{actual_version}.pyc" in filename:
                    continue
                match = re.search('\\.(\\d+)\\.pyc$', filename)
                if match:
                    old_ver = match.group(1)
                    new_filename = filename.replace(f".{old_ver}.pyc", f".{actual_version}.pyc")
            break
            for version in MAGIC_NUMBERS.values():
                if f".{version}.pyc" in new_filename:
                    pass
                break
            if new_filename != filename:
                new_filepath = os.path.join(directory, new_filename)
                if os.path.exists(new_filepath):
                    pass
if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
    return None
# [SUMMARY] 4 blocks · 4 processed · 1 orphan · 40 instr
