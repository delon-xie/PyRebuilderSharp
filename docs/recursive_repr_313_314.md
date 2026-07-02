## 一、`recursive_repr` 源码（Lib/reprlib.py）

CPython 3.13/3.14 中 `recursive_repr` 定义在 `Lib/reprlib.py`，核心逻辑：

```python
def recursive_repr(fillvalue="..."):
    def decorating_function(user_function):
        _repr_running = "__repr_running_" + id(user_function).__format__("x")

        @wraps(user_function)
        def wrapper(self):
            if hasattr(self, _repr_running):
                return fillvalue
            setattr(self, _repr_running, True)
            try:
                result = user_function(self)
            finally:
                delattr(self, _repr_running)
            return result
        return wrapper
    return decorating_function
```

关键点：`wrapper(self)` 是一个**带闭包（closure）的函数**，闭包捕获 `user_function`、`fillvalue`、`_repr_running`（字符串常量）。

---

## 二、wrapper 函数的字节码结构（Python 3.13 / 3.14）

用 `dis.dis(wrapper)` 可看到典型输出（3.13/3.14 格式，隐藏 CACHE 行）：

```
  0  RESUME                  0

  2  LOAD_GLOBAL              (hasattr)             # 或 INLINE_CACHE
  4  LOAD_FAST                0 (self)
  6  LOAD_CONST               1 ('__repr_running_xxxx')
  8  CALL                     2
 16  POP_JUMP_IF_FALSE      38

 18  LOAD_CONST               2 ('...')              # fillvalue
 20  RETURN_VALUE

 22  LOAD_FAST                0 (self)
 24  LOAD_CONST               1 ('__repr_running_xxxx')
 26  LOAD_CONST               3 (True)
 28  LOAD_ATTR               (setattr) -- 或 PUSH_NULL + LOAD_GLOBAL
 30  CALL                     3                      # setattr(self, key, True)

  -- try block: call user_function(self) --
 34  LOAD_DEREF               0 (user_function)      # 闭包 cell
 36  LOAD_FAST                0 (self)
 38  PUSH_NULL                                     # 3.11+ 实例方法调用惯例
 40  CALL                     1
 42  STORE_FAST               1 (result)

  -- finally: delattr --
 44  LOAD_GLOBAL             (delattr)
 46  LOAD_FAST                0 (self)
 48  LOAD_CONST               1 ('__repr_running_xxxx')
 50  CALL                     2

 52  LOAD_FAST                1 (result)
 54  RETURN_VALUE
```

> 注：3.13/3.14 中 `CALL(argc)` 统一替代旧版 `CALL_FUNCTION`/`CALL_METHOD`，`MAKE_FUNCTION` 的属性设置改为 `SET_FUNCTION_ATTRIBUTE(flag)`（3.13 新增），但 wrapper 本身编译出的字节码不受此影响。

---

## 三、关键字节码指令解读（3.13 vs 3.14 差异点）

| 位置 | 指令 | 含义 |
|------|------|------|
| `RESUME 0` | 3.11+ 入口帧标记，3.13/3.14 无变化 |
| `LOAD_CONST (key_str)` | 闭包捕获的 `_repr_running` 字符串来自 `co_consts` |
| `LOAD_DEREF (user_function)` | 从 closure cell 加载原始 `__repr__` |
| `PUSH_NULL + CALL 1` | 3.11+ 调用约定：NULL（method flag）+ 1 pos arg → 等价于 `user_function(self)` |
| `SETUP_FINALLY` / `PUSH_EXCEPT` | 隐含在 `try/finally` 编译中（3.11+ 用异常表 Exception Table 而非 `SETUP_FINALLY` 字节码） |
| `STORE_FAST (result)` → `RETURN_VALUE` | finally 块执行完后返回 |

**3.14 新增细节**：
- `LOAD_FAST_BORROW` / `LOAD_FAST_BORROW_LOAD_FAST_BORROW` 可能替代部分 `LOAD_FAST`，属解释器微优化，**不影响指令序列逻辑和栈深度**，dis 输出仍显示为 `LOAD_FAST` 语义。
- `dis` 新增 `-P/show_positions` 参数，不影响字节码本身。

---

## 四、装饰器应用时的字节码（模块级）

`@recursive_repr()` 触发 `CALL 0`（调用外层工厂）→ `MAKE_FUNCTION` → `SET_FUNCTION_ATTRIBUTE`（3.13+ 设 `__wrapped__`, `__doc__` 等）→ `STORE_NAME/STORE_ATTR __repr__`。

这部分在 **类体编译** 中产生，不属于 wrapper 自身的字节码。

---

## 五、总结

- `recursive_repr` 的字节码就是典型的**闭包函数 + try/finally + hasattr/setattr/delattr + CALL 原方法**模式。
- 3.13→3.14 在该 wrapper 上**无语义字节码变化**，仅 3.14 引入 borrow-load 微优化（`LOAD_FAST_BORROW` 族）。
- 真正有版本差异的是 `MAKE_FUNCTION` 侧（`SET_FUNCTION_ATTRIBUTE` 取代旧属性设置方式，3.13 新增）。
