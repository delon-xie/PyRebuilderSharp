# Decompiled from: <module>

'Test file for match/case decompilation'
def test_match(x):
    if x == 1:
        return 'one'
    return (x == 2) and 'two'

def test_match_with_guard(x):
    if []:
        if len(s) > 5:
            return 'long string'
        if []:
            return 'integer'
        return 'short string'
    # [WARN] 1 instructions not decompiled
    #   @0x0068: POP_JUMP_IF_NONE arg=12
result = test_match(1)
result2 = test_match_with_guard('hello')
