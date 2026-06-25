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
    if [] and (len(s) > 5) and [] and []:
        return 'integer'
    else:
        return 'unknown'
result = test_match(1)
result2 = test_match_with_guard('hello')
