def nested():
    a = [x for row in [[1,2,3], [4,5,6]] for x in row]
    return a