# Decompiled from: <module>

with open(sys.argv[1], 'rb') as f:
    magic = f.read(4)
    f.read(8)
    code = marshal.load(f)
    raise
    print('Module:', code.co_name)
    print('  argc:', code.co_argcount)
    print('  nlocals:', code.co_nlocals)
    print('  code len:', len(code.co_code))
    print('  code hex:', code.co_code.hex()[None:60])
    dump_code = dump_code
    dump_code(code)
    return None
