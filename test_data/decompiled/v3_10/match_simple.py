# Decompiled from: <module>

'Test file for match/case decompilation'
def test_match(x):
    pass
    if x == 1:
        return 'one'
    pass
    if x == 2:
        return 'two'
    return 'other'

def test_match_with_guard(x):
    pass
    if []:
        pass
        if len(s) > 5:
            return 'long string'
        pass
        if []:
            return 'short string'
        pass
        if []:
            return 'integer'
        return 'unknown'
    pass
result = test_match(1)
result2 = test_match_with_guard('hello')
