import marshal, struct, io

with open('/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/abc.3.12.pyc', 'rb') as f:
    header = f.read(16)
    marshal_data = f.read()

stream = io.BytesIO(marshal_data)

# Find all occurrences of 0x64 in the raw marshal stream
print('=== Looking for 0x64 in raw marshal stream ===')
buf = marshal_data
positions = [i for i, b in enumerate(buf) if b == 0x64]
for pos in positions[:20]:
    context_start = max(0, pos-4)
    context = buf[context_start:min(len(buf), pos+12)]
    hex_str = " ".join(f"{b:02x}" for b in context)
    print(f"  0x64 at raw pos {pos}: ... {hex_str}")

# Now let's check what type would be read at those positions
print()
print("=== Context analysis ===")
# The marshal stream top-level offset is 0 (we skipped the header)
# When C# reads, it starts at position 0 in the header-skipped data
# Let's check what should be at the positions of 0x64

# For each 0x64 occurrence, check: is this after a TYPE_CODE that we might have
# misread field counts for?
for pos in positions[:20]:
    # Look at what type flag preceded this position
    # Walk back to find the nearest type byte (values 0-127, excluding data bytes)
    preceding = buf[max(0,pos-20):pos]
    # Find the nearest type marker
    markers = [i for i, b in enumerate(preceding) if b in (0x63, 0x73, 0x28, 0x29, 0x7a, 0x5a, 0x61, 0x74, 0x75, 0x7c, 0x6e, 0x70, 0x71, 0x72)]
    marker_pos = pos - len(preceding) + markers[-1] if markers else 0
    marker_type = preceding[markers[-1]] if markers else 0
    print(f"  0x64 at pos {pos}: preceded by type 0x{marker_type:02x} at +{pos-len(preceding)+ (markers[-1] if markers else 0)}")

# Now marshal.load successfully - let's check if the issue is with
# TYPE_SHORT_ASCII_INTERNED = 0x5A ('Z') - we have it defined as 90
# but 0x5A is 90, so that should be correct

# Let me check: does Python 3.12 marshal use TYPE_SHORT_ASCII_DATA = 0x64?
# Actually, let me check Python 3.12 marshal source
print()
print("=== Checking TYPE_SHORT_ASCII_DATA ===")
# In Python 3.12, marshal.c defines:
# TYPE_SHORT_ASCII_DATA = 'd' (0x64)
# TYPE_SHORT_ASCII_INTERNED_DATA = 'D' (0x44)
# TYPE_ASCII_DATA = 'a' (0x61) -- already have this
# TYPE_ASCII_INTERNED_DATA = 'T' (0x54)
# TYPE_DATA = 'd' (100)
# Actually, these are only in internal marshal, not in .pyc files.

# Check: is 0x64 used at all in valid marshal?
# Let's check the positions more carefully with the marshal cursor approach
stream.seek(0)
try:
    code = marshal.load(stream)
    print(f"Marshal load succeeded. Total marshal data: {len(marshal_data)} bytes, read: {stream.tell()}")
except Exception as e:
    print(f"Marshal load failed: {e}")
    print(f"Stopped at pos {stream.tell()}")
