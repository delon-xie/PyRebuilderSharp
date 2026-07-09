import struct

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    header = f.read(16)

print(f"Raw header bytes: {header.hex()}")

# Try big-endian magic
magic_be = struct.unpack('>I', header[0:4])[0]
print(f"\nMagic (BE): 0x{magic_be:08X}")

# Python magic numbers
magic_versions = {
    0x0A0D5533: "Python 3.13 (BE)",
    0x0A0D5634: "Python 3.14 (BE)",
    0x33550D0A: "Python 3.13 (LE)",
    0x34560D0A: "Python 3.14 (LE)",
}

for magic, version in magic_versions.items():
    if magic == magic_be or magic == struct.unpack('<I', header[0:4])[0]:
        print(f"\nDetected Python version: {version}")
        break
else:
    print("\nUnknown Python version")

# 尝试读取 marshal 数据
import marshal
with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    f.read(16)
    try:
        code_obj = marshal.load(f)
        print(f"\nSuccessfully loaded code object!")
        print(f"Code object type: {type(code_obj)}")
        if hasattr(code_obj, 'co_version'):
            print(f"co_version: {code_obj.co_version}")
    except Exception as e:
        print(f"\nError loading marshal data: {e}")
