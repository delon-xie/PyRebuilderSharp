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
