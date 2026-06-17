# Decompiled from: <module>

# orphan @0x0000
import sys
import dis
import marshal
import types
f = open(sys.argv[1], 'rb')
magic = f.read(4)
print(f"Magic: {magic.hex()}")
flags = int.from_bytes(f.read(4), 'little')
ts = int.from_bytes(f.read(4), 'little')
size = int.from_bytes(f.read(4), 'little')
print(f"Header: flags={flags} ts={ts} size={size}")
raw = f.read()
code = marshal.loads(raw)
print(f"Code name: {code.co_name}")
print(f"Has co_exceptiontable: {hasattr(code, 'co_exceptiontable')}")
# orphan @0x0242
# orphan @0x0268
print(f"co_exceptiontable bytes ({len(code.co_exceptiontable)}): {code.co_exceptiontable.hex()}")
et = code.co_exceptiontable
# orphan @0x0312
# orphan @0x033A
start = int.from_bytes(et[i:i + 2], 'little')
end = int.from_bytes(et[i + 2:i + 4], 'little')
target = int.from_bytes(et[i + 4:i + 6], 'little')
dl = int.from_bytes(et[i + 6:i + 8], 'little')
print(f"  [{start},{end}) → {target} depth={dl & 3} lasti={bool(dl & 4)}")
# orphan @0x04C4
# orphan @0x04F6
print(f"
--- Nested: {const.co_name} ---")
print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
# orphan @0x0568
# orphan @0x0590
print(f"  bytes: {const.co_exceptiontable.hex()}")
return None
# [SUMMARY] 23 blocks · 15 processed · 22 orphan · 319 instr
