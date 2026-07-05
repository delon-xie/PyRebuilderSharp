# Decompiled from: <module>

import os
import struct
MAGIC_NUMBERS = {b'Wg0NCg==': '3.10', b'Yg0NCg==': '3.11', b'bw0NCg==': '3.12', b'eg0NCg==': '3.13', b'hQ0NCg==': '3.14'}
import os
import struct
MAGIC_NUMBERS = {b'Wg0NCg==': '3.10', b'Yg0NCg==': '3.11', b'bw0NCg==': '3.12', b'eg0NCg==': '3.13', b'hQ0NCg==': '3.14'}

def get_python_version(filepath):
    # orphan @0x0000
    open(filepath, 'rb')

def fix_pyc_names(directory):
    filepath = os.path.join(directory, filename)
    actual_version = get_python_version(filepath)
    os.listdir(directory)
    for filename in os.listdir(directory):
        pass
        if not filename.endswith('.pyc'):
            pass
        else:
            filepath = os.path.join(directory, filename)
            actual_version = get_python_version(filepath)
            if actual_version == 'unknown':
                pass
            else:
                pass
                if f".{actual_version}.pyc" in filename:
                    pass
                else:
                    new_filename = filename
                    MAGIC_NUMBERS.values()
        import re
        match = re.search('\\.(\\d+)\\.pyc$', filename)
        if match:
            old_ver = match.group(1)
            new_filename = filename.replace(f".{old_ver}.pyc", f".{actual_version}.pyc")
        pass
        if not directory != v_65:
            pass
        else:
            new_filepath = os.path.join(directory, new_filename)
            if os.path.exists(new_filepath):
                pass
            else:
                os.rename(directory, v_41)
                print(f"✓ Renamed {filename} -> {new_filename}")
    new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
    new_filepath = os.path.join(directory, new_filename)

if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
