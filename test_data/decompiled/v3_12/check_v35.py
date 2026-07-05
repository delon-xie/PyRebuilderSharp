# Decompiled from: <module>

def dump_code(c, depth):
    prefix = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        pass
        if not hasattr(const, 'co_code'):
            pass
        else:
            pass
            if not hasattr(const, 'co_name'):
                pass
            else:
                print(f"{prefix!s}Function: {const.co_name!s}")
                print('%s  argc=%d nlocals=%d code=%dB' % (prefix, const.co_argcount, const.co_nlocals, len(const.co_code)))
                dump_code(const, depth + 1)

class Class_0000:
    marshal = marshal
    sys = sys
