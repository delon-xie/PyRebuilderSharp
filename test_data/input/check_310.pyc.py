import marshal, dis, types, sys

f = open(sys.argv[1], 'rb')
magic = f.read(4)
f.read(12)
raw = f.read()
code = marshal.loads(raw)

def dump_bytecode(c, depth=0):
    p = '  ' * depth
    for const in c.co_consts:
        if hasattr(const, 'co_code') and isinstance(const, types.CodeType):
            print(f'{p}--- {const.co_name} ---')
            et = getattr(const, 'co_exceptiontable', None)
            print(f'{p}exception table: {et.hex() if et else "(none)"}')
            if et:
                for i in range(0, len(et), 8):
                    s=int.from_bytes(et[i:i+2],'little')
                    e=int.from_bytes(et[i+2:i+4],'little')
                    t=int.from_bytes(et[i+4:i+6],'little')
                    dl=int.from_bytes(et[i+6:i+8],'little')
                    print(f'{p}  [{s},{e}) -> {t} depth={dl & 3}')
            dis.dis(const)
            dump_bytecode(const, depth + 1)

dump_bytecode(code)
