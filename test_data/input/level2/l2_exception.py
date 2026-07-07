def l2_1_try_finally():
    try:
        x = 1
    finally:
        x = 2
    return x


def l2_2_try_except_single():
    try:
        x = 1 / 0
    except ValueError:
        x = 0
    return x


def l2_3_try_except_multiple():
    try:
        x = 1 / 0
    except (ValueError, ZeroDivisionError):
        x = 0
    return x


def l2_4_try_except_else():
    try:
        x = 1 / 1
    except ZeroDivisionError:
        return "error"
    else:
        return "success"


def l2_5_try_except_else_finally():
    try:
        x = 1 / 1
    except ZeroDivisionError:
        return "error"
    else:
        return "success"
    finally:
        pass


def l2_6_nested_try():
    try:
        try:
            x = 1 / 0
        except ZeroDivisionError:
            x = 1
    except Exception:
        x = 2
    return x


def l2_7_try_return():
    def f():
        try:
            return 1
        finally:
            return 2
    return f()


def l2_8_try_yield():
    def gen():
        try:
            yield 1
        finally:
            yield 2
    return list(gen())


def l2_9_with_statement():
    class ContextManager:
        def __enter__(self):
            return "value"
        def __exit__(self, *args):
            pass

    with ContextManager() as fp:
        result = fp
    return result


def l2_10_try_except_no_else():
    try:
        x = 1 / 1
    except ZeroDivisionError:
        return "error"
    return "success"


def l2_11_try_finally_only():
    try:
        x = 1 / 0
    finally:
        return "finally"


def l2_12_nested_try_else():
    try:
        try:
            x = 1 / 1
        except ZeroDivisionError:
            return "inner error"
        else:
            return "inner success"
    except Exception:
        return "outer error"


def l2_13_except_as():
    try:
        x = 1 / 0
    except ZeroDivisionError as e:
        return str(e)
    return "ok"


def l2_14_raise():
    try:
        raise ValueError("test")
    except ValueError:
        return "caught"


def l2_15_raise_from():
    try:
        try:
            1 / 0
        except Exception as e:
            raise ValueError("wrapped") from e
    except ValueError:
        return "caught"
