"""Directly read and dump the marshal data structure of a .pyc file"""
import struct, sys

path = 'test_data/compiled/abc.3.11.pyc'

with open(path, 'rb') as f:
    data = f.read()

print(f"File: {path}, {len(data)} bytes")
print(f"Magic: {data[0]:02x} {data[1]:02x} {data[2]:02x} {data[3]:02x}")
print(f"Flags: {struct.unpack('<I', data[4:8])[0]}")
print(f"Timestamp: {struct.unpack('<I', data[8:12])[0]}")
print(f"Size: {struct.unpack('<I', data[12:16])[0]}")
print(f"Hash: {data[16:24].hex()}")

# Skip header - 3.11 format
# Magic(4) + Flags(4) + Hash(4) + BitField(4) + Size(4) = 20? No, let me check
# 3.11 .pyc header: magic(4) + flags(4) + hash_or_timestamp(4) + source_size(4)
# If flags & 1 (hash-based), the hash is 8 bytes? Let me just skip variable header

# The marshal data starts at position 16 for some files
# Let me check by looking for TYPE_CODE (0x63)
pos = data.find(b'\x63', 16)
print(f"TYPE_CODE (0x63) found at position: {pos}")
print(f"Bytes at positions 16-40: {data[16:40].hex()}")

# Check header more carefully
# Python 3.11 .pyc format:
# 4 bytes: magic (A7 0D 0D 0A)
# 4 bytes: flags bit field (bit 0: 1 = hash-based)
# if hash-based: 8 bytes source hash (SipHash)
# 4 bytes: source size (optional?)
# then marshal data

magic = data[0:4]
flags = struct.unpack('<I', data[4:8])[0]
print(f"Flag bit 0 (hash?): {bool(flags & 1)}")
print(f"Flag bit 1 (source size present?): {bool(flags & 2)}")

# Try to find the marshal stream start
# After header: marshal starts with c (TYPE_CODE = 0x63)
# Try different offsets
for offset in [12, 16, 20, 24]:
    if offset < len(data) and data[offset] == 0x63:
        print(f"\nMarshal data seems to start at offset {offset}")
        print(f"  Type: {data[offset]} = 0x63 = TYPE_CODE (c)")
        print(f"  Next 4 bytes (argcount?): {struct.unpack('<i', data[offset+1:offset+5])}")

# Let me just look at the hex dump of the header area
print(f"\nFull hex dump (first 80 bytes):")
for i in range(0, min(80, len(data)), 16):
    hex_str = ' '.join(f'{b:02x}' for b in data[i:i+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
    print(f"  {i:04x}: {hex_str:<48s} {ascii_str}")
