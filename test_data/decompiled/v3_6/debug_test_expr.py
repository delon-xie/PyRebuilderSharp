# Decompiled from: <module>

with open('/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions.38.pyc', 'rb') as f:
    data = bytearray(f.read())
for i in range(16, len(data)):
    stripped = data[i] & 127
    if (stripped in known_types) and (data[i] != stripped):
        pass
    break
    for instr in dis.get_instructions(code):
        instr.offset
        '  '
        print
        '20s'
        instr.opname
        ' '
        '4d'
    '20s'
    instr.opname
    ' '
    '4d'
code = marshal.loads(bytes(data[16:]))
print('Code name:', code.co_name)
print('Names:', code.co_names)
print('Constants:', code.co_consts)
print('Varnames:', code.co_varnames)
print()
print('Instructions:')
dis.get_instructions(code)
