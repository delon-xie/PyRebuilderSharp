# Decompiled from: <module>

def test5():
    try:
        range(3)
        for x in range(3):
            try:
                try:
                    range(3)
                    try:
                        pass
                    except:
                        break
                except:
                    break
                y = x
            except:
                break
    except:
        break
    # orphan @0x003E
    # [WARN] 1 instructions not decompiled
    #   @0x0024: JUMP_BACKWARD arg=26
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 6 instr
