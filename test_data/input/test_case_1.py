# 测试用例 1: 字典推导式
def test_dict_comp():
    members = [('a', 1), ('b', 2)]
    body = {t[0]: t[1] for t in members}
    return body

# 测试用例 2: 逻辑表达式
def test_logical_or():
    obj = {}
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')

# 测试用例 3: 条件表达式
def test_logical_and():
    name = '__abc__'
    return len(name) > 4 and name[:2] == name[-2:] == '__' and name[2] != '_' and name[-3] != '_'

# 测试用例 4: 生成器表达式
def test_genexpr():
    member_names = ['a', 'b', 'c']
    member_map = {'a': 1, 'b': 2, 'c': 3}
    return (member_map[name] for name in member_names)