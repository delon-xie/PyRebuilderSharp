import os
import struct

MAGIC_NUMBERS = {
    b'\x5a\x0d\x0d\x0a': '3.10',
    b'\x62\x0d\x0d\x0a': '3.11',
    b'\x6f\x0d\x0d\x0a': '3.12',
    b'\x7a\x0d\x0d\x0a': '3.13',
    b'\x85\x0d\x0d\x0a': '3.14',
}

def get_python_version(filepath):
    with open(filepath, 'rb') as fp:
        magic = fp.read(4)
    return MAGIC_NUMBERS.get(magic, 'unknown')

def fix_pyc_names(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pyc'):
            filepath = os.path.join(directory, filename)
            actual_version = get_python_version(filepath)
            if actual_version == 'unknown':
                continue
            
            # Check if the filename already has the correct version
            if f'.{actual_version}.pyc' in filename:
                continue
            
            # Find and replace the version in the filename
            # Look for patterns like .3.10.pyc or .310.pyc or .38.pyc
            new_filename = filename
            for version in MAGIC_NUMBERS.values():
                if f'.{version}.pyc' in new_filename:
                    new_filename = new_filename.replace(f'.{version}.pyc', f'.{actual_version}.pyc')
                    break
            else:
                # Try to find patterns like .310.pyc or .38.pyc
                import re
                match = re.search(r'\.(\d+)\.pyc$', filename)
                if match:
                    old_ver = match.group(1)
                    new_filename = filename.replace(f'.{old_ver}.pyc', f'.{actual_version}.pyc')
            
            if new_filename != filename:
                new_filepath = os.path.join(directory, new_filename)
                if os.path.exists(new_filepath):
                    print(f'⚠️  Skipping {filename} -> {new_filename} (destination exists)')
                else:
                    os.rename(filepath, new_filepath)
                    print(f'✓ Renamed {filename} -> {new_filename}')

if __name__ == '__main__':
    fix_pyc_names('tests/compiled')
    print('\nDone!')
