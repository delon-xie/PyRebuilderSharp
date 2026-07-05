# Decompiled from: <module>

for (v, k) in known.items():
    if k == 'flags':
        pass
for start in range(0, 8):
    if start + 16 > len(m):
        pass
    code2 = marshal.loads(m)
    print(f"\nRe-loaded: argcount={code2.co_argcount} nlocals={code2.co_nlocals} stacksize={code2.co_stacksize} flags={hex(code2.co_flags)}")
    print(f"Match: {code2.co_argcount == code.co_argcount}")
vals = struct.unpack_from('<IIII', m, start)
a0 = *vals
nl = *vals
ss = *vals
fl = *vals
