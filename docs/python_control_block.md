Python 中的控制块（通常指控制流语句的结构化块）主要分为以下几大类：

---

### 1. 条件控制

| 关键字 | 说明 |
|---|---|
| `if` | 基本条件判断 |
| `elif` | 多重条件分支 |
| `else` | 默认分支 |

```python
if condition:
    pass
elif another_condition:
    pass
else:
    pass
```

---

### 2. 循环控制

| 关键字 | 说明 |
|---|---|
| `for` | 遍历可迭代对象 |
| `while` | 基于条件重复执行 |
| `else`（与循环搭配） | 循环正常结束（未 break）时执行 |

```python
# for 循环
for item in iterable:
    pass
else:
    pass

# while 循环
while condition:
    pass
else:
    pass
```

---

### 3. 异常处理

| 关键字 | 说明 |
|---|---|
| `try` | 尝试执行的代码块 |
| `except` | 捕获并处理异常 |
| `else` | 无异常发生时执行 |
| `finally` | 无论是否异常都执行 |

```python
try:
    pass
except SomeException as e:
    pass
else:
    pass
finally:
    pass
```

---

### 4. 上下文管理

| 关键字 | 说明 |
|---|---|
| `with` | 管理资源（文件、锁等），自动调用 enter / exit |

```python
with open('file.txt', 'r') as f:
    content = f.read()
```

---

### 5. 函数与类定义

| 关键字 | 说明 |
|---|---|
| `def` | 定义函数 |
| `class` | 定义类 |
| `async def` | 定义异步函数（协程） |

```python
def func():
    pass

class MyClass:
    pass

async def async_func():
    pass
```

---

### 6. 模块与包

| 关键字 | 说明 |
|---|---|
| `import` | 导入模块 |
| `from ... import` | 从模块导入特定内容 |

```python
import os
from math import sqrt
```

---

### 7. 匹配模式（Python 3.10+）

| 关键字 | 说明 |
|---|---|
| `match` | 结构化模式匹配 |
| `case` | 匹配的分支 |

```python
match value:
    case pattern1:
        pass
    case pattern2 if condition:
        pass
    case _:
        pass
```

---

### 8. 循环内部控制关键字

| 关键字 | 说明 |
|---|---|
| `break` | 跳出当前循环 |
| `continue` | 跳过本次循环剩余语句，进入下一次迭代 |
| `pass` | 空操作，占位符 |

---

### 总结表

| 类别 | 关键字 |
|---|---|
| 条件 | `if` `elif` `else` |
| 循环 | `for` `while` `else`（循环版） |
| 异常 | `try` `except` `else` `finally` |
| 上下文 | `with` |
| 定义 | `def` `class` `async def` |
| 模块 | `import` `from` |
| 模式匹配 | `match` `case` |
| 流程控制 | `break` `continue` `pass` |

以上就是 Python 中所有构成控制块的语法结构。