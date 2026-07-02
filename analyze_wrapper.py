import marshal

with open('test_data/compiled/reprlib.3.11.pyc', 'rb') as f:
    f.read(16)
    code = marshal.load(f)

def find_func(code, name):
    for c in code.co_consts:
        if hasattr(c, 'co_name') and c.co_name == name:
            return c
    return None

recursive_repr = find_func(code, 'recursive_repr')
decorating_function = find_func(recursive_repr, 'decorating_function')
wrapper = find_func(decorating_function, 'wrapper')

def parse_varint(data, offset):
    result = 0
    shift = 0
    while True:
        byte = data[offset]
        offset += 1
        result |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            break
        shift += 7
    return result, offset

print('=== Parsed Exception Table ===')
et_data = wrapper.co_exceptiontable
offset = 0
while offset < len(et_data):
    start, offset = parse_varint(et_data, offset)
    end, offset = parse_varint(et_data, offset)
    target, offset = parse_varint(et_data, offset)
    depth, offset = parse_varint(et_data, offset)
    print('Entry: Start=%04X, End=%04X, Target=%04X, Depth=%d' % (start, end, target, depth))

print()
print('=== Instructions (raw) ===')
code_bytes = wrapper.co_code
i = 0
while i < len(code_bytes):
    op = code_bytes[i]
    if op >= 90:
        arg = code_bytes[i+1]
        print('  %04X: op=%d, arg=%d' % (i, op, arg))
        i += 2
    else:
        print('  %04X: op=%d' % (i, op))
        i += 1
