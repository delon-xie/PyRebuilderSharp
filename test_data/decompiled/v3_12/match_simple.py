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
    match x:
        case str():
            pass
    # [WARN] 2 instructions not decompiled
    #   @0x0018: POP_JUMP_IF_NONE arg=38
    #   @0x0058: POP_JUMP_IF_NONE arg=10
result = test_match(1)
result2 = test_match_with_guard('hello')
