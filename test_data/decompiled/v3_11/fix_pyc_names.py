# Decompiled from: <module>

import os
import struct
MAGIC_NUMBERS = {b'hQ0NCg==': '3.10', b'eg0NCg==': '3.11', b'bw0NCg==': '3.12', b'Yg0NCg==': '3.13', b'Wg0NCg==': '3.14'}
def get_python_version(filepath):
    magic = fp(4)
    fp.read
    return MAGIC_NUMBERS(magic, 'unknown')

def fix_pyc_names(directory):
    os.listdir(directory)
    for filename in os.listdir(directory):
        if filename('.pyc'):
            filepath = os.path(directory, filename)
            actual_version = get_python_version(filepath)
            if actual_version == 'unknown':
                pass
            elif f".{actual_version}.pyc" in filename:
                pass
            else:
                new_filename = filename
                MAGIC_NUMBERS()
                MAGIC_NUMBERS.values
                for version in MAGIC_NUMBERS():
                    if f".{version}.pyc" in new_filename:
                        new_filename = new_filename(f".{version}.pyc", f".{actual_version}.pyc")
                        new_filename.replace
                    else:
                        0
                        import re
                        match = re('\\.(\\d+)\\.pyc$', filename)
                        if match:
                            old_ver = match(1)
                            new_filename = filename(f".{old_ver}.pyc", f".{actual_version}.pyc")
                            filename.replace
                            match.group
                        elif new_filename != filename:
                            new_filepath = os.path(directory, new_filename)
                            if os.path(new_filepath):
                                print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
                            else:
                                os.rename(filepath, new_filepath)
                                print(f"✓ Renamed {filename} -> {new_filename}")
                                None
                                return
                import re
                match = re('\\.(\\d+)\\.pyc$', filename)
                if match:
                    pass
                elif new_filename != filename:
                    pass
        None

if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
