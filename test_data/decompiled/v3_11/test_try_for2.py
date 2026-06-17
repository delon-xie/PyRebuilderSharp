# Decompiled from: <module>

def test5():
    try:
        range(3)
        for x in range(3):
            try:
                try:
                    range(3)
                except:
                    break
                y = x
            except:
                break
        return
    except:
        break
    None
    # orphan @0x003E
    raise
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 6 instr
