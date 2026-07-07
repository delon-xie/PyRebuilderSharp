def test_try_except_else():
    try:
        x = 1 / 1
    except ZeroDivisionError:
        return "error"
    else:
        return "success"

def test_try_except_no_else():
    try:
        x = 1 / 1
    except ZeroDivisionError:
        return "error"
    return "success"

def test_try_finally():
    try:
        x = 1 / 1
    finally:
        return "finally"

def test_try_except_else_finally():
    try:
        x = 1 / 1
    except ZeroDivisionError:
        return "error"
    else:
        return "success"
    finally:
        pass

def test_try_finally_only():
    try:
        x = 1 / 0
    finally:
        return "finally"

def test_nested_try_else():
    try:
        try:
            x = 1 / 1
        except ZeroDivisionError:
            return "inner error"
        else:
            return "inner success"
    except Exception:
        return "outer error"