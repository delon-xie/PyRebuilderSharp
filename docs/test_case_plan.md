## PYC 反编译测试用例覆盖规划

PYC 反编译的正确性验证远比想象中复杂，因为 CPython 编译器在生成字节码时会做大量优化和转换（如窥孔优化、栈缓存、异常表压缩等），反编译器必须能逆向还原这些操作。

以下是从简单到复杂的测试用例规划，按层级递进：

---

## Level 0：字面量与基本表达式

**目标**：验证最基本的常量、变量、运算符的反编译正确性

| 编号 | 测试内容 | Python 源码示例 | 反编译难点 |
|------|---------|----------------|-----------|
| 0-1 | 整数/浮点数/字符串常量 | `a = 42` / `b = 3.14` / `c = "hello"` | 常量缓存（`LOAD_CONST`）的还原 |
| 0-2 | 布尔值与 None | `x = True` / `y = None` | 布尔值在字节码中是常量而非关键字 |
| 0-3 | 基本算术运算 | `result = a + b * c` | 操作数顺序的还原（栈操作逆推） |
| 0-4 | 比较运算 | `a > b and c <= d` | 短路求值的还原（`JUMP_IF_FALSE_OR_POP` 等） |
| 0-5 | 列表/字典/集合字面量 | `lst = [1, 2, 3]` / `d = {"a": 1}` | `BUILD_LIST` / `BUILD_MAP` 的参数还原 |
| 0-6 | 切片操作 | `s[1:10:2]` | `BUILD_SLICE` 的三个参数推断 |
| 0-7 | 属性访问与方法调用 | `obj.method(arg)` | `LOAD_ATTR` + `CALL_FUNCTION` 的组合还原 |

---

## Level 1：基础控制块

**目标**：验证单层控制流的反编译正确性

| 编号 | 测试内容 | Python 源码示例 | 反编译难点 |
|------|---------|----------------|-----------|
| 1-1 | 简单 if-else | `if x > 0: pass else: pass` | 条件跳转目标的重建 |
| 1-2 | if-elif-else 链 | `if a: ... elif b: ... elif c: ... else: ...` | 多级跳转链的还原 |
| 1-3 | 单行 if（三元表达式） | `x = a if cond else b` | `POP_JUMP_IF_FALSE` 的两种语义区分 |
| 1-4 | 简单 while 循环 | `while i < 10: i += 1` | 回边（`JUMP_ABSOLUTE`）的识别 |
| 1-5 | for 循环（range） | `for i in range(10): print(i)` | `GET_ITER` + `FOR_ITER` 的配对 |
| 1-6 | for 循环（可迭代对象） | `for item in lst: process(item)` | 迭代器协议的还原 |
| 1-7 | break 与 continue | `while True: if cond: break else: continue` | 跳转目标的精确匹配 |
| 1-8 | for-else / while-else | `for x in lst: if match(x): break else: not_found()` | else 块的条件判断（循环正常结束） |

---

## Level 2：异常处理

**目标**：验证 try-except-finally 结构的反编译，这是最大的难点之一

| 编号 | 测试内容 | Python 源码示例 | 反编译难点 |
|------|---------|----------------|-----------|
| 2-1 | 裸 try-finally | `try: op() finally: cleanup()` | finally 块的复制展开（多个副本） |
| 2-2 | try-except（单异常） | `try: op() except ValueError: handle()` | 异常表条目的还原 |
| 2-3 | try-except（多异常） | `try: op() except (A, B): handle()` | 异常类型的合并与拆分 |
| 2-4 | try-except-else | `try: op() except E: h() else: success()` | else 块的定位（在 except 之后） |
| 2-5 | try-except-finally 全量 | `try: op() except: h() else: s() finally: clean()` | 四种块的组合与边界确定 |
| 2-6 | 嵌套 try | `try: try: inner() except: pass except: outer()` | 异常表的嵌套作用域 |
| 2-7 | try 中的 return | `def f(): try: return x finally: cleanup()` | return 与 finally 的交互（返回值暂存） |
| 2-8 | try 中的 yield | `def gen(): try: yield x finally: cleanup()` | generator 的异常传播特殊性 |
| 2-9 | with 语句（上下文管理器） | `with open(f) as fp: read(fp)` | `SETUP_WITH` / `WITH_CLEANUP` 的还原 |

---

## Level 3：Lambda 与匿名函数

**目标**：验证闭包和作用域链的反编译

| 编号 | 测试内容 | Python 源码示例 | 反编译难点 |
|------|---------|----------------|-----------|
| 3-1 | 简单 lambda | `f = lambda x: x + 1` | `MAKE_FUNCTION` 的参数还原 |
| 3-2 | lambda 捕获外部变量 | `f = lambda: outer_var` | 闭包单元格（cell variable）的识别 |
| 3-3 | lambda 默认参数 | `f = lambda x, y=10: x + y` | 默认参数的常量提取 |
| 3-4 | lambda 作为参数传递 | `sorted(lst, key=lambda x: x.name)` | 内联 lambda 的命名 |
| 3-5 | lambda 嵌套 lambda | `f = lambda x: lambda y: x + y` | 多重闭包的层级关系 |
| 3-6 | lambda 中的可变参数 | `f = lambda *args, **kwargs: sum(args)` | `*` 和 `**` 参数的还原 |

---

## Level 4：函数定义与嵌套

**目标**：验证函数声明、参数处理、作用域的还原

| 编号 | 测试内容 | Python 源码示例 | 反编译难点 |
|------|---------|----------------|-----------|
| 4-1 | 无参函数 | `def f(): return 42` | 函数头信息的重建 |
| 4-2 | 位置参数与默认值 | `def f(a, b=10): return a + b` | 默认值的存储方式（`LOAD_CONST` + `MAKE_FUNCTION`） |
| 4-3 | 关键字参数与可变参数 | `def f(*args, **kwargs): pass` | `*` 和 `**` 的标志位还原 |
| 4-4 | 参数注解 | `def f(x: int, y: str) -> bool: ...` | 注解的存储位置（`__annotations__`） |
| 4-5 | 嵌套函数（闭包） | `def outer(x): def inner(y): return x + y; return inner` | cell/free 变量的追踪 |
| 4-6 | nonlocal 声明 | `def outer(): x = 1; def inner(): nonlocal x; x += 1` | `DEREF` / `STORE_DEREF` 的语义还原 |
| 4-7 | global 声明 | `x = 0; def f(): global x; x += 1` | `LOAD_GLOBAL` / `STORE_GLOBAL` 的区分 |
| 4-8 | 递归函数 | `def fact(n): return 1 if n <= 1 else n * fact(n-1)` | 自身引用的识别 |
| 4-9 | 装饰器 | `@decorator; def f(): pass` | `CALL_FUNCTION` 包装的还原 |

---

## Level 5：类定义与面向对象

**目标**：验证类定义、继承、方法解析的反编译

| 编号 | 测试内容 | Python 源码示例 | 反编译难点 |
|------|---------|----------------|-----------|
| 5-1 | 空类 | `class A: pass` | `LOAD_BUILD_CLASS` 的识别 |
| 5-2 | 带属性的类 | `class A: x = 1; def __init__(self): self.y = 2` | 类体与实例体的区分 |
| 5-3 | 继承 | `class B(A): pass` | 基类的参数还原 |
| 5-4 | 方法重写与 super | `class B(A): def method(self): return super().method()` | `super()` 的隐式参数传递 |
| 5-5 | 类方法与静态方法 | `@classmethod` / `@staticmethod` | 装饰器的还原 |
| 5-6 | 属性描述符 | `@property` / `@x.setter` | property 对象的构建还原 |
| 5-7 | 元类 | `class A(metaclass=Meta): pass` | 元类参数的传递方式 |
| 5-8 | 多重继承与 MRO | `class C(A, B): pass` | 基类列表的还原 |

---

## Level 6：高级特性

**目标**：验证 Python 特有高级特性的反编译

| 编号 | 测试内容 | Python 源码示例 | 反编译难点 |
|------|---------|----------------|-----------|
| 6-1 | 生成器函数 | `def gen(): yield 1; yield 2` | `YIELD_VALUE` 的状态机还原 |
| 6-2 | 生成器表达式 | `g = (x*x for x in range(10))` | 隐式生成器函数的创建 |
| 6-3 | 列表推导式 | `[x*x for x in range(10) if x % 2 == 0]` | `LIST_APPEND` + 循环的还原 |
| 6-4 | 字典/集合推导式 | `{k:v for k,v in items}` / `{x for x in lst}` | `MAP_ADD` / `SET_ADD` 的识别 |
| 6-5 | async/await | `async def f(): await g()` | `GET_AWAITABLE` / `YIELD_FROM` 的特殊处理 |
| 6-6 | 异步生成器 | `async def gen(): yield x` | `ASYNC_GENERATOR` 标志位的识别 |
| 6-7 | 海象运算符（:=） | `if (n := len(x)) > 0: use(n)` | `DUP_TOP` + `STORE_FAST` 的模式匹配 |
| 6-8 | match-case（3.10+） | `match value: case 1: ... case _: ...` | 模式匹配的字节码序列还原 |
| 6-9 | dataclass | `@dataclass; class Point: x: int; y: int` | 自动生成方法的还原 |

---

## Level 7：边界情况与极端场景

**目标**：验证反编译器在处理非标准代码时的健壮性

| 编号 | 测试内容 | 说明 | 反编译难点 |
|------|---------|------|-----------|
| 7-1 | 空函数 / 空类 | `def f(): pass` | 空的代码对象处理 |
| 7-2 | 极深嵌套（>20层） | 20层以上的 if/for/try 嵌套 | 递归深度的限制 |
| 7-3 | 超长表达式（单行>1000字符） | 复杂的链式调用 | 表达式树的平衡与还原 |
| 7-4 | 死代码（unreachable code） | `return 1; x = 2` | 死代码的识别与丢弃 |
| 7-5 | 优化后的常量折叠 | `x = 1 + 2` → 字节码直接是 `LOAD_CONST 3` | 常量折叠的逆向推理 |
| 7-6 | 优化后的窥孔优化 | `NOT ROT_TWO` 等优化序列 | 优化模式的逆向匹配 |
| 7-7 | 不同 Python 版本生成的 pyc | 3.8 vs 3.10 vs 3.12 的字节码差异 | 版本兼容性处理 |
| 7-8 | 带中文/Unicode 标识符 | `def 函数(): return "你好"` | Unicode 名称的保留 |
| 7-9 | 动态执行（exec/eval） | `exec("print(1)")` | 字符串内容的保留（不反编译字符串内代码） |
| 7-10 | 魔改/损坏的 pyc | 人为修改字节码 | 容错与报错机制 |

---

## 测试用例组织建议

### 按优先级分层

```
P0 - 基础功能（必须通过）：Level 0-2
P1 - 重要功能（应通过）：Level 3-4
P2 - 高级功能（争取通过）：Level 5-6
P3 - 边缘情况（长期维护）：Level 7
```

### 自动化测试框架设计

```python
# 测试用例的通用结构
@pytest.mark.parametrize("source, expected", [
    ("a = 1", "a = 1"),                              # 最简单的常量赋值
    ("if x: pass", "if x:\n    pass"),                # 单层控制流
    ("try: pass\nexcept: pass", "try:\n    pass\nexcept:\n    pass"),
])
def test_basic(source, expected):
    # 1. 编译源码为字节码
    code = compile(source, '<test>', 'exec')
    
    # 2. 模拟 pyc 文件格式（添加 magic number + 时间戳）
    pyc_data = marshal.dumps(code)
    
    # 3. 调用反编译器
    result = decompile_pyc(pyc_data)
    
    # 4. 验证反编译结果与原始源码等价（注意格式化差异）
    assert normalize(result) == normalize(expected)
```

### 验证策略

1. **精确匹配**：对于简单代码，反编译结果应与源码逐字符一致
2. **语义等价**：对于复杂代码（如常量折叠后），验证反编译后再编译得到的字节码与原字节码一致
3. **执行等价**：反编译后的代码应能正确执行，输出与原代码相同

---

## 反编译器开发路线图建议

```
Phase 1: Level 0-1 → 能处理基本表达式和控制流
Phase 2: Level 2   → 异常处理（最难的部分）
Phase 3: Level 3-4 → 函数与闭包
Phase 4: Level 5-6 → 类与高级特性
Phase 5: Level 7   → 边界情况与稳定性
```

这个规划涵盖了从简单到复杂的全部场景，可以作为 PYC 反编译器开发和测试的系统性参考。