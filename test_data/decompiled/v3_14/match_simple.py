# Decompiled from: <module>

'Test file for match/case decompilation'
def test_match(x):
    if x == 1:
        return 'one'
    return (x == 2) and 'two'

def test_match_with_guard(x):
    if x:
        if len(s) > 5:
            return 'long string'
        return 'unknown'
        pass
    pass
result = test_match(1)
result2 = test_match_with_guard('hello')
