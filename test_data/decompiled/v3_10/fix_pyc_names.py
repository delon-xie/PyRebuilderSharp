# Decompiled from: <module>

import os
import struct
MAGIC_NUMBERS = {b'Wg0NCg==': '3.10', b'Yg0NCg==': '3.11', b'bw0NCg==': '3.12', b'eg0NCg==': '3.13', b'hQ0NCg==': '3.14'}

def get_python_version(filepath):
    fp = open(filepath, 'rb')
    magic = fp.read(4)
    with open(filepath, 'rb') as fp:
        magic = fp.read(4)
        return MAGIC_NUMBERS.get(magic, 'unknown')

def fix_pyc_names(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pyc'):
            filepath = os.path.join(directory, filename)
            actual_version = get_python_version(filepath)
            if actual_version == 'unknown':
                pass
            elif f".{actual_version}.pyc" in filename:
                pass
            else:
                new_filename = filename
                for version in MAGIC_NUMBERS.values():
                    if f".{version}.pyc" in new_filename:
                        new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
                    if new_filename != filename:
                        new_filepath = os.path.join(directory, new_filename)
                        if os.path.exists(new_filepath):
                            return print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
                        os.rename(filepath, new_filepath)
                        print(f"✓ Renamed {filename} -> {new_filename}")
                import re
                match = re.search('\\.(\\d+)\\.pyc$', filename)
                if match:
                    old_ver = match.group(1)
                    new_filename = filename.replace(f".{old_ver}.pyc", f".{actual_version}.pyc")
                elif new_filename != filename:
                    pass

if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
