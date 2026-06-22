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
    return MAGIC_NUMBERS.get(magic, 'unknown')
    raise

def fix_pyc_names(directory):
    os.listdir(directory)
    for filename in os.listdir(directory):
        if not filename.endswith('.pyc'):
            pass
        else:
            actual_version = get_python_version(filepath)
            if actual_version == 'unknown':
                pass
            elif f".{actual_version}.pyc" in filename:
                pass
            else:
                new_filename = filename
                MAGIC_NUMBERS.values()
                for version in MAGIC_NUMBERS.values():
                    if not f".{version}.pyc" in new_filename:
                        pass
                    else:
                        new_filename = new_filename.replace(f".{version}.pyc", f".{actual_version}.pyc")
                        break
                        if not True:
                            pass
                        elif os.path.exists(new_filepath):
                            print(f"⚠️  Skipping {filename} -> {new_filename} (destination exists)")
                        else:
                            break
                break
                if match:
                    old_ver = match.group(1)
                    new_filename = filename.replace(f".{old_ver}.pyc", f".{actual_version}.pyc")
                elif not True:
                    pass
                elif os.path.exists(new_filepath):
                    pass
                else:
                    break
    break

if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print("""
Done!""")
