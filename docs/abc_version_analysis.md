# abc.py 各版本对照分析及修复

> 基于白盒 339/405 基线和实际输出对比

---

## 1. 2.7 版本

| 问题 | 当前 | 正确 | 影响 | 可修? |
|:-----|:-----|:-----|:----:|:-----:|
| `class _C:` 不应该出现 | `class _C: pass` | 无（# Python 2 兼容） | 语义错误 | 🔴 难 |
| `def ABCMeta():` | 函数定义 | `class ABCMeta(type):` | 语义错误 | 🔴 难 |

**根因**: Python 2.7 的编译格式与 3.x 不同（无 `__build_class__`），`LOAD_BUILD_CLASS` 在 2.7 字节码中对应 `__build_class__` 的调用，但 StackMachine 处理路径与 3.x 不同。

**建议**: 不修复 2.7。Python 2.7 已经 EOL，白盒 86% 通过率已足够。

---

## 2. 3.5-3.7 版本

| 问题 | 当前 | 正确 | 影响 | 可修? |
|:-----|:-----|:-----|:----:|:-----:|
| `def ABC():` | 函数定义 | `class ABC(metaclass=ABCMeta):` | 语义错误 | 🟡 中 |
| 裸 docstring | `'Abstract Base...'` | 应消失或被吸收 | 噪声 | 🟢 易 |
| `inheritance.` | 裸字符串 | 应消失 | 噪声 | 🟢 易 |

**3.5-3.7 KW_NAMES 字节码结构**:
```
LOAD_BUILD_CLASS        ← 创建 class builder
LOAD_CONST <code_obj>  ← 类体代码
MAKE_FUNCTION 0
LOAD_CONST 'ABC'       ← 类名
LOAD_GLOBAL ABCMeta    ← 关键字参数值 (metaclass=)
LOAD_CONST ('metaclass',) ← KW_NAMES 元组
CALL_FUNCTION_KW 3     ← 3个参数 + KW_NAMES
STORE_NAME ABC
```

因 CALL_FUNCTION_KW 的 KW_NAMES 使 StackMachine 难以正确解析关键字参数。

**修复方向**: 在 `ConvertChildCodesToFunctionDefs` 中添加对 CALL_FUNCTION_KW 的支持——检测 LOAD_BUILD_CLASS + LOAD_CONST + MAKE_FUNCTION + LOAD_CONST(name) + LOAD_* + CALL_FUNCTION_KW 模式。

---

## 3. 3.8-3.10 版本

| 问题 | 当前 | 正确 | 影响 | 可修? |
|:-----|:-----|:-----|:----:|:-----:|
| 模块级 `try:` | 整个文件包裹在 try 内 | 无 try | BARE+BARE+TRY_NO | 🟡 中 |
| `inheritance.` 片段 | 裸字符串 | 应消失 | 噪声 | 🟢 易 |
| `cls.__dict__.items()` | BARE_EXPR | 应消失 | BARE | 🟢 已修 |

**3.8-3.10 模块级 try 根因**: abc.py 用一个 `try: ... except NameError: pass` 包裹整个模块（为了兼容 `_py_abc` 导入）。SETUP_FINALLY 在 3.8-3.10 中被误解析为模块级 try 结构，且 handler body 为空（仅 POP_TOP×3 无实际 except 语句）。

**修复**: 在 `ParseTryStructure` 中检测模块级 try（header 在偏移 0 且覆盖 90%+ 代码）→ 跳过该结构。

---

## 4. 3.11+ 版本

最佳状态。`class ABCMeta(type):` 正确解析，`class ABC(metaclass=ABCMeta):` 正确。仅剩：
- `inheritance.` 片段（已在短字符串规则中清理）
- `update_abstractmethods` 控制流分裂 BARE_EXPR（Phase 9-4 目标）

---

## 5. `_DOC_` 问题分析

未在 abc.py 任何版本输出中检测到字面 `_DOC_`。用户所指可能是：

1. **Docstring 顺序错乱**: abc.3.5 中 `abstractclassmethod.__init__` 的 docstring 在 `super().__init__` 后出现
2. **裸字符串作为文档**: `'Abstract Base Classes (ABCs) according to PEP 3119.'` 在模块级作为裸表达式
3. **`__doc__` 赋值暴露**: `__doc__ = '...'` 在函数/类体内出现

上述均为已有规则可处理的范围。

---

## 6. 分版本输出对照表

| 版本 | `class ABCMeta` | `class ABC` | 模块级 try | BARE | TRY_NO | SYNTAX |
|:----:|:---------------:|:-----------:|:----------:|:----:|:------:|:------:|
| 2.7 | ❌ `def ABCMeta()` | — | ❌ class _C | 3 | 0 | 0 |
| 3.5 | ✅ | ❌ def ABC | ❌ 裸docstring | 4 | 0 | 1 |
| 3.6 | ✅ | ❌ def ABC | ✅ | 3 | 0 | 0 |
| 3.7 | ✅ | ❌ def ABC | ✅ | 2 | 1 | 0 |
| 3.8 | ✅ | ✅ | ❌ module try | 1 | 1 | 0 |
| 3.9 | ✅ | ✅ | ❌ module try | 1 | 1 | 0 |
| 3.10 | ✅ | ✅ | ❌ module try | 1 | 1 | 0 |
| 3.11 | ✅ | ✅ | ✅ | 1 | 0 | 0 |
| 3.12 | ✅ | ✅ | ✅ | 2 | 0 | 0 |
| 3.13 | ✅ | ✅ | ✅ | 1 | 0 | 0 |
| 3.14 | ✅ | ✅ | ✅ | 1 | 0 | 0 |

(✅ = 正确, ❌ = 有误)

---

## 7. 修复优先级建议

| 优先级 | 问题 | 版本 | 方法 | 工期 | 白盒预期 |
|:------:|:-----|:----:|:-----|:----:|:--------:|
| **P0** | 模块级 try | 3.8-3.10 | `ParseTryStructure` 跳过模块级 | 4h | +3 |
| **P1** | `def ABC()` → `class ABC` | 3.5-3.7 | `ConvertChildCodesToFunctionDefs` CALL_FUNCTION_KW | 4h | — |
| **P2** | 2.7 `class _C` | 2.7 | 跳过 Python 2 兼容类 | 2h | — |
| **P3** | docstring 顺序 | 所有 | `PostProcessFunctionDefs` 移动 docstring | 1h | — |
