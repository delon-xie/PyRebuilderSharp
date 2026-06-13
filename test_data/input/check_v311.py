# Check v3.11 marshal format by comparing with Python's marshal
import marshal, struct, sys

with open(sys.argv[1], 'rb') as f:
    raw = f.read()

# Python reads everything
f = open(sys.argv[1], 'rb')
magic = f.read(4)
hdr_rest = f.read(12)  # flags(4)+ts(4)+size(4) for 3.11
code = marshal.load(f)
f.close()

print('Python marshal results:')
print(f'  argcount={code.co_argcount}')
print(f'  posonly={code.co_posonlyargcount}')
print(f'  kwonly={code.co_kwonlyargcount}')
print(f'  nlocals={code.co_nlocals}')
print(f'  stacksize={code.co_stacksize}')
print(f'  flags={code.co_flags:#x}')
print(f'  bytecode len={len(code.co_code)}')
print(f'  consts count={len(code.co_consts)}')
print(f'  names={list(code.co_names)}')

# Now manually find where each field is
print()
print('Header analysis:')
print(f'  magic: {raw[0:4].hex()}')
print(f'  hdr:   {raw[4:16].hex()}')

# Find a kwonlyargcount=0 in the raw bytes
# We know the value should be 0 for <module>
# Look for 4 zero bytes at a position after raw[16]
for off in range(17, 40):
    if raw[off:off+4] == b'\x00\x00\x00\x00':
        print(f'  4 zero bytes at offset {off}')

# Python's r_object for code objects reads:
# 1 byte type, then fields
# If FLAG is set, it reads an additional 4-byte ref-index FIRST
# But wait - does FLAG add a ref-index or just flag the object?

# Look at the bytes right after the type byte
print(f'\nBytes 16-50:')
for i in range(16, 50, 2):
    pair = raw[i:i+2]
    print(f'  {i:3d}: {pair.hex()}')
