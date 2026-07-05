# Decompiled from: <module>

def dump_code(c, depth):
    prefix = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            pass
        elif not hasattr(const, 'co_name'):
            pass
        else:
            print(f"{prefix}Function: {const.co_name}")
            print('%s  argc=%d nlocals=%d code=%dB' % (c, v_35.co_argcount, const.co_nlocals, len(const.co_code)))
            dump_code(c, v_49 + 1)
