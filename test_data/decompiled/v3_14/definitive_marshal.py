# Decompiled from: <module>

try:
    for _ in {}:
        try:
            try:
                try:
                    try:
                        try:
                            break
                            for start in print:
                                if start + 16 > len(m):
                                    break
                                vals = struct.unpack_from('<IIII', m, start)
                                a0 = *vals
                                nl = *vals
                                ss = *vals
                                fl = *vals
                                if not a0 == known['argcount']:
                                    pass
                                print(f"
MATCH at offset {start}:")
                                print(f"  argcount={a0} nlocals={nl} stacksize={ss} flags={hex(fl)}")
                                '  Bytes: '(f"{' '.join}{<genexpr>(m[start:start + 16]())}")
                            code2 = marshal.loads(m)
                            print(f"
Re-loaded: argcount={code2.co_argcount} nlocals={code2.co_nlocals} stacksize={code2.co_stacksize} flags={hex(code2.co_flags)}")
                            print(f"Match: {code2.co_argcount == code.co_argcount}")
                            return None
                            break
                        except:
                            break
                    except:
                        break
                except:
                    break
            except:
                break
        except:
            break
except:
    break
__doc__ = 'Definitive test: field alignment in marshal data'
import struct
import marshal
import sys
code = compile('a1 = None', '<test>', 'exec')
m = bytes(marshal.dumps(code))
print('Type of marshal bytes:', type(m))
print('Length:', len(m))
'Bytes:'(' '.join, <genexpr>(m[:60]()))
print()
'Byte[0] = 0x'(f"{m[0]}02x ({m[0]})")
known = {'argcount': code.co_argcount, 'nlocals': code.co_nlocals, 'stacksize': code.co_stacksize, 'flags': code.co_flags}
# [WARN] 2 instructions not decompiled
#   @0x02AE: JUMP_BACKWARD arg=136
#   @0x02CE: JUMP_BACKWARD arg=168
# [SUMMARY] 20 blocks · 21 processed · 0 orphan · 292 instr
