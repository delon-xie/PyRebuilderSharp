import struct

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/reprlib.3.13.pyc', 'rb') as f:
    header = f.read(16)
    
magic = struct.unpack('<I', header[0:4])[0]
timestamp = struct.unpack('<I', header[4:8])[0]
size = struct.unpack('<I', header[8:12])[0]
hash = header[12:16]

print(f"Magic: 0x{magic:08X}")
print(f"Timestamp: {timestamp}")
print(f"Size: {size}")
print(f"Hash: {hash.hex()}")

# Python 3.13 magic = 0x33550D0A
# Python 3.14 magic = 0x34560D0A
magic_versions = {
    0x33550D0A: "Python 3.13",
    0x34560D0A: "Python 3.14",
}

if magic in magic_versions:
    print(f"\nDetected Python version: {magic_versions[magic]}")
else:
    print(f"\nUnknown Python version for magic 0x{magic:08X}")
