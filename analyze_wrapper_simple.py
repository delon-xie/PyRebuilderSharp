import marshal
import dis

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

print(f"=== wrapper function ===")
print(f"Name: {wrapper.co_name}")
print(f"Argcount: {wrapper.co_argcount}")
print(f"Locals: {wrapper.co_varnames}")
print(f"Names: {wrapper.co_names}")
print(f"Constants: {wrapper.co_consts}")
print(f"Code length: {len(wrapper.co_code)} bytes")

print(f"\n=== Disassembly ===")
dis.dis(wrapper)

print(f"\n=== Exception Table raw bytes ===")
et_data = wrapper.co_exceptiontable
print(f"ET length: {len(et_data)} bytes")
print(f"ET hex: {et_data.hex()}")

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

print(f"\n=== Parsed Exception Table ===")
offset = 0
while offset < len(et_data):
    start, offset = parse_varint(et_data, offset)
    end, offset = parse_varint(et_data, offset)
    target, offset = parse_varint(et_data, offset)
    depth, offset = parse_varint(et_data, offset)
    print(f"Entry: Start={start:X4}, End={end:X4}, Target={target:X4}, Depth={depth}")
