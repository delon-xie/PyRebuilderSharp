def nested_comp():
    # 简单列表推导式
    simple = [x for x in range(5)]
    
    # 带条件的列表推导式
    filtered = [x for x in range(10) if x % 2 == 0]
    
    # 嵌套列表推导式（二维转一维）
    nested = [x for row in [[1,2,3], [4,5,6]] for x in row]
    
    # 带条件的嵌套列表推导式
    nested_filtered = [x for row in [[1,2,3], [4,5,6]] for x in row if x > 2]
    
    # 复杂表达式的列表推导式
    complex_expr = [x * 2 + 1 for x in range(5)]
    
    # 集合推导式
    set_comp = {x for x in range(5)}
    
    return simple, filtered, nested, nested_filtered, complex_expr, set_comp
