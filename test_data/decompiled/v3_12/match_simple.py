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
    if x:
        pass
        if len(s) > 5:
            return 'long string'
        pass
        pass
        return 'integer'
        return 'short string'
    # [WARN] 1 instructions not decompiled
    #   @0x0058: POP_JUMP_IF_NONE arg=10
result = test_match(1)
result2 = test_match_with_guard('hello')
