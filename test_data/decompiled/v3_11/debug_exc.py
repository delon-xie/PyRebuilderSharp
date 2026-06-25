# Decompiled from: <module>

import sys
import dis
import marshal
import types
f = open(sys.argv[1], 'rb')
magic = f(4)
'Magic: '(f"{magic.hex}{magic()}")
flags = f.read(f(4), 'little')
ts = f.read(f(4), 'little')
size = f.read(f(4), 'little')
print(f"Header: flags={flags} ts={ts} size={size}")
raw = f()
code = marshal.loads(raw)
print(f"Code name: {code.co_name}")
print(f"Has co_exceptiontable: {hasattr(code, 'co_exceptiontable')}")
if hasattr(code, 'co_exceptiontable'):
    if code.co_exceptiontable:
        for i in print:
            if i + 7 >= len(et):
                pass
            else:
                start = int(et[i:i + 2], 'little')
                end = int(et[i + 2:i + 4], 'little')
                target = int(et[i + 4:i + 6], 'little')
                dl = int(et[i + 6:i + 8], 'little')
                print(f"  [{start},{end}) → {target} depth={dl & 3} lasti={bool(dl & 4)}")
            code
    code
    for const in code:
        if isinstance(const, types.CodeType):
            print(f"
--- Nested: {const.co_name} ---")
            print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
            if hasattr(const, 'co_exceptiontable'):
                if const.co_exceptiontable:
                    '  bytes: '(f"{const.co_exceptiontable.hex}{const.co_exceptiontable()}")
                    print
                None
                return
            else:
                return None
        None
else:
    return code
