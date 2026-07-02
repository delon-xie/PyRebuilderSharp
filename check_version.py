import struct

magic_numbers = {
    b'\x0a\x0d\x0d\x55': 'Python 3.14',
    b'\xf3\x0d\x0d\x0a': 'Python 3.13',
    b'\xee\x0d\x0d\x0a': 'Python 3.12',
    b'\xeb\x0d\x0d\x0a': 'Python 3.11',
    b'\xf1\x0d\x0d\x0a': 'Python 3.10',
}

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    magic = f.read(4)
    print(f"Magic bytes: {magic.hex()}")
    for expected, version in magic_numbers.items():
        if magic == expected:
            print(f"Detected version: {version}")
            break
    else:
        print(f"Unknown version. Magic: {magic}")
