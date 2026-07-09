import dis
import sys

src = '''
def test():
    lock = object()
    with lock:
        pass
    with lock as lk:
        print(lk)
'''

print(f"Python version: {sys.version}")
print()

code = compile(src, '<test>', 'exec')
print(f"co_consts: {code.co_consts}")
func_code = None
for const in code.co_consts:
    if hasattr(const, 'co_code'):
        func_code = const
        break

print("Function bytecode:")
dis.disassemble(func_code)

print("\n\nException table:")
if hasattr(func_code, 'co_exceptiontable'):
    import struct
    et = func_code.co_exceptiontable
    print(f"Raw: {et.hex()}")
    i = 0
    while i < len(et):
        if sys.version_info >= (3, 11):
            start = struct.unpack('<H', et[i:i+2])[0]
            end = struct.unpack('<H', et[i+2:i+4])[0]
            target = struct.unpack('<H', et[i+4:i+6])[0]
            depth = struct.unpack('<B', et[i+6:i+7])[0]
            kind = struct.unpack('<B', et[i+7:i+8])[0]
            i += 8
        else:
            start = struct.unpack('<H', et[i:i+2])[0]
            end = struct.unpack('<H', et[i+2:i+4])[0]
            target = struct.unpack('<H', et[i+4:i+6])[0]
            depth = struct.unpack('<B', et[i+6:i+7])[0]
            i += 7
        print(f"  start=0x{start:X}, end=0x{end:X}, target=0x{target:X}, depth={depth}, kind={kind}")
