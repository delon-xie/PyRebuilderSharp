def outer():
    lock = object()
    def inner():
        with lock:
            pass
        with lock as lk:
            print(lk)
    return inner
