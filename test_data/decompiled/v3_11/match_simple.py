# Decompiled from: <module>

"""Test file for match/case decompilation"""
def test_match(x):
    if x == 1:
        return 'one'
    elif x == 2:
        return 'two'
    else:
        return 'other'

def test_match_with_guard(x):
    if len(s) > 5:
        return 'long string'
    else:
        s := str
        return 'short string'
result = test_match(1)
result2 = test_match_with_guard('hello')
