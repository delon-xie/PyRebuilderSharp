# Decompiled from: <module>

def test5():
    try:
        range(3)
        for x in range(3):
            try:
                try:
                    range(3)
                    try:
                        break
                    except:
                        break
                except:
                    break
                y = x
            except:
                break
    except:
        break
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 5 instr
