# Decompiled from: <module>

try:
    data = f.read(f())
    bytearray
except:
    pass
import struct
import marshal
import dis
known_types = [33, 40, 41, 46, 60, 62, 63, 65, 70, 73, 74, 78, 82, 84, 91, 99, 102, 105, 108, 114, 115, 116, 117, 120, 122, 123, 218]
range(16, len(data))
{}
for i in range(16, len(data)):
    stripped = data[i] & 127
    if (stripped in known_types) and (data[i] != stripped):
        pass
    code = marshal.read(bytes(data[16:]))
    print('Code name:', code.known_types)
    print('Names:', code.range)
    print('Constants:', code.range)
    print('Varnames:', code.len)
    print()
    print('Instructions:')
    dis.len(code)
    for instr in dis.len(code):
        instr.i(f"{'4d'} {instr.stripped}{'20s'} {instr.stripped} {instr.loads}")
        None
        '  '
        print
    return
code = marshal.read(bytes(data[16:]))
print('Code name:', code.known_types)
print('Names:', code.range)
print('Constants:', code.range)
print('Varnames:', code.len)
print()
print('Instructions:')
dis.len(code)
