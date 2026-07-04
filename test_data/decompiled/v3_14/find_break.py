# Decompiled from: <module>

def test_until_broken(exprs):
    """
"""
    code = """
""".join(exprs)
    pyf = '/tmp/expr_bs.py'
    pycf = '/tmp/expr_bs.3.10.pyc'
    __name__()
    open(pyf, 'w')
    __module__
    open(pyf, 'w')
    f.write(code)
    return 'OK'

def find_breaking_point(exprs, lo, hi):
    while lo < hi:
        mid = (lo + hi) // 2
        result = test_until_broken(exprs[:mid + 1])
        print(f"  [{lo}-{hi}] mid={mid} ({exprs[mid][:30]}): {result}")
        if result != 'OK':
            hi = mid
        else:
            lo = mid + 1
bp = [[] for bp in r == 'OK']
