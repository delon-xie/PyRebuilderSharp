# Decompiled from: <module>

def test_match(x):
    return 'one'
    return 'two'

def test_match_with_guard(x):
    if len(s) > 5:
        return 'long string'
    return 'short string'
    # [WARN] 2 instructions not decompiled
    #   @0x001A: POP_JUMP_IF_NONE arg=74
    #   @0x0064: POP_JUMP_IF_NONE arg=116
result = test_match(1)
result2 = test_match_with_guard('hello')
