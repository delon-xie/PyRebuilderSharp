def test():
    lock = object()
    with lock:
        pass
    with lock as lk:
        print(lk)
