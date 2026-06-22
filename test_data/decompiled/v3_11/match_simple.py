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
    if [] is None:
        if len(s) > 5:
            return 'long string'
        return 'short string'
    # [WARN] 2 instructions not decompiled
    #   @0x001A: POP_JUMP_IF_NONE arg=50
    #   @0x0068: POP_JUMP_IF_NONE arg=12
result = test_match(1)
result2 = test_match_with_guard('hello')
