import struct

# Read the .pyc file manually
with open('test_data/compiled/abc.3.14.pyc', 'rb') as f:
    data = f.read()

# 3.14 expected header size: 16 bytes
print(f"File size: {len(data)}")
print(f"Header: {data[:16].hex()}")

# Try to find the update_abstractmethods code object
# The .pyc format: header then a marshal'd CodeObject
# Let me try a different approach - check if Python 3.14 can read it
