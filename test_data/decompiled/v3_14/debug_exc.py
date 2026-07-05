# Decompiled from: <module>

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
if hasattr(code, 'co_exceptiontable'):
    pass
    if code.co_exceptiontable:
        for i in range(0, len(et), 8):
            pass
            if i + 7 >= len(et):
                pass
            else:
                start = int.from_bytes(et[i:i + 2], 'little')
                end = int.from_bytes(et[i + 2:i + 4], 'little')
                target = int.from_bytes(et[i + 4:i + 6], 'little')
                dl = int.from_bytes(et[i + 6:i + 8], 'little')
                print(f"  [{start},{end}) → {target} depth={dl & 3} lasti={bool(dl & 4)}")
            for const in code.co_consts:
                pass
                if not isinstance(const, types.CodeType):
                    pass
                else:
                    print(f"\n--- Nested: {const.co_name} ---")
                    print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
                    if not hasattr(const, 'co_exceptiontable'):
                        pass
                    else:
                        pass
                        if not const.co_exceptiontable:
                            pass
                        else:
                            print(f"  bytes: {const.co_exceptiontable.hex()}")
            pass
    code.co_consts
code.co_consts
print(f"\n--- Nested: {const.co_name} ---")
print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
