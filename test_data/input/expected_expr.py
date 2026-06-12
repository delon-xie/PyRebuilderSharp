# ---- Lv0-A: 基本表达式（无短路运算/条件表达式）----
# 这些表达式只涉及栈操作，不触发 JUMP_IF_xxx_OR_POP

# 常量
a1 = None
a2 = True
a3 = False
a4 = 42
a5 = 3.14
a6 = "hello"

# 变量访问
b1 = x
b2 = obj.attr

# 切片
b3 = items[0]
b4 = items[1:10]
b5 = items[1:]

# 一元运算
c1 = not x
c2 = ~x
c3 = -x

# 二元运算
d1 = x + y
d2 = x - y
d3 = x * y
d4 = x / y
d5 = x // y
d6 = x % y
d7 = x ** y

# 位运算
e1 = x & y
e2 = x | y
e3 = x ^ y
e4 = x << y
e5 = x >> y

# 比较运算
f1 = x < y
f2 = x > y
f3 = x <= y
f4 = x >= y
f5 = x == y
f6 = x != y
f7 = x is y
f8 = x is not y
f9 = x in y
f10 = x not in y

# 函数调用
i1 = func()
i2 = func(x)
i3 = func(x, y)

# 链式属性
o1 = obj.attr.sub
o2 = obj.method()

# 复合表达式（无and/or/条件）
n1 = (a + b) * (c - d)
n2 = -x ** 2 + y / 3
n3 = x + y * z
n4 = x * y + z
n5 = a + b + c
n6 = a * b * c
