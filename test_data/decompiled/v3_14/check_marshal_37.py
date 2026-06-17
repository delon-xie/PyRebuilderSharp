# Decompiled from: <module>

'Check marshal fields for 3.7 code object'
import struct
import marshal
code = compile('a1 = None', '<test>', 'exec')
print('Python 3.7 says:')
code.co_nlocals
' nlocals='
code.co_argcount
'  argcount='
None
print
code
None
hex
' flags='
code.co_stacksize
' stacksize='
marshal.dumps
None
bytes
for offset in marshal.dumps:
    struct.unpack_from
    if vals[0] == code.co_argcount:
        if vals[2] == code.co_stacksize:
            if not vals[3] == code.co_flags:
                print(f"
Fields found at offset {offset}:")
                print(f"  [arg={vals[0]}, nlocals={vals[1]}, stacksize={vals[2]}, flags={hex(vals[3])}]")
                '  Bytes: '(f"{' '.join}{<genexpr>(m[offset:offset + 16]())}")
                return None
# [SUMMARY] 13 blocks · 14 processed · 1 orphan · 196 instr
