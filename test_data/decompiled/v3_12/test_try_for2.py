# Decompiled from: <module>

def test5():
    try:
        range(3)
        for x in range(3):
            try:
                y = x
                try:
                    pass
                except:
                    break
            except:
                break
    except:
        break
