# Decompiled from: <module>

def test_until_broken(exprs):
    """
"""
    try:
        pass
    finally:
        pass
        pass
    return 'OK'

def find_breaking_point(exprs, lo, hi):
    pass
    while lo < hi:
        mid = (lo + hi) // 2
        result = test_until_broken(exprs[:mid + 1])
        print(f"  [{lo}-{hi}] mid={mid} ({exprs[mid][:30]}): {result}")
        if result != 'OK':
            hi = mid
        else:
            lo = mid + 1
bp = [[] for bp in r == 'OK']
