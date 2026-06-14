# Phase 5 收尾总结 — PyRebuilderSharp

**版本**: v1.0
**日期**: 2026-06-14
**项目**: PyRebuilderSharp (.NET 10 + Avalonia GUI)

---

## 一、核心成就

### ✅ 展开赋值 (P5-1)

`a, b = func()` 和 `a, *rest = iter` 的基础支持：

| 组件 | 文件 | 说明 |
|:-----|:------|:------|
| `Starred` AST 节点 | `Expr.cs` | `*expr` 表达式，支持 Load/Store 上下文 |
| `UNPACK_SEQUENCE` 处理器 | `StackMachine.cs` | 展开序列到栈，每个元素生成 Starred |
| `UNPACK_EX` 处理器 | `StackMachine.cs` | `a, *rest = ...` 含 `ExpressionContext.Store` 标记 |
| `VisitStarred()` 代码生成 | `PythonCodeGenerator.cs` | `*expr` 输出渲染 |

### ✅ 版本矩阵编译脚本全覆盖

`tools/compile_test_data.py` 从仅支持 3.11-3.14 扩展到 **2.7→3.14 共 11 个版本**，覆盖两个目录：

| 目录 | 版本 | 文件数 |
|:-----|:------|:-------|
| `test_data/compiled/` (Benchmark) | 2.7→3.14 (11) | **938** ✅ |
| `tests/.../TestData/compiled/` (测试矩阵) | 2.7→3.14 (11) | 1323 ✅ |

```bash
python3 tools/compile_test_data.py   # 一键编译全部
```

| 版本 | 路径 | 状态 |
|:-----|:------|:------|
| 2.7 | `2.7.18/bin/python2.7` | ✅ 938 编译 · 0 失败 |
| 3.5 | `3.5.10/bin/python3.5` | ✅ |
| 3.6 | `3.6.15/bin/python3.6` | ✅ |
| 3.7 | `3.7.17/bin/python3.7` | ✅ |
| 3.8 | `3.8.20/bin/python3.8` | ✅ |
| 3.9 | `3.9.25/bin/python3.9` | ✅ |
| 3.10 | **`3.10.20`/bin/python3.10** | ✅（用户指定版本） |
| 3.11 | `3.11.15/bin/python3.11` | ✅ |
| 3.12 | `3.12.13/bin/python3.12` | ✅ |
| 3.13 | `3.13.12/bin/python3.13` | ✅ |
| 3.14 | `3.14.3/bin/python3.14` | ✅ |

### ✅ 语法覆盖清单完成

| 语法 | 状态 |
|:-----|:------|
| `def` 函数定义 · 参数 · 返回值 · 闭包 | ✅ |
| `class` 类定义 · 方法 · `__init__` · 级属性 | ✅ |
| `yield` / `yield from` 生成器 | ✅ |
| `@decorator` 装饰器链 | ✅ |
| `async def` / `await` 异步 | ✅ |
| `if/elif/else` · `for/while` · `try/except/finally` | ✅ |
| `lambda` · `raise` · `assert` · `del` | ✅ |
| `import` / `from X import` | ✅ |
| 列表/字典/集合推导式 | ✅ |
| f-string (3.6+) | ✅ |
| 类型注解 (3.5+) | ✅ |
| `with` 语句 | ✅ |
| 展开赋值 `a, b = ...` · `a, *rest = ...` | ✅ **P5-1 新增** |
| `match/case` (3.10+) | ❌ |
| `except*` (3.11+) | ❌ |
| walrus `:=` (3.8+) | ❌ |

---

## 二、项目最终状态

### 测试

| 指标 | 数值 | 状态 |
|:-----|:-----|:------|
| xUnit 测试总数 | 109 | — |
| 通过 | 102 | ✅ |
| 失败（预存） | 7 | 🔧 |
| 通过率 | 93.6% | ✅ |
| Marsha警告 | 0/182 | ✅ |
| 版本矩阵 | 77/77 (2.7→3.14) | ✅ |
| 编译版本数 | 11 | ✅ |

### 预存失败 (7)

| 测试 | 原因 |
|:-----|:------|
| PycReaderTests ×4 | `simple_const.3.8.pyc` 文件路径 |
| StackMachineTests ×2 | BinaryAdd opcode 映射 |
| TokenDumperTests ×1 | Token 格式预期值 |

### 文档

| 文档 | 版本 | 说明 |
|:-----|:------|:------|
| `docs/Python反编译总体设计.md` | v2.6 | 架构设计 |
| `docs/Python反编译详细设计.md` | v2.5 | 组件详细设计 |
| `docs/plan_phase4.md` | v2.0 | Phase 4 计划 |
| `docs/plan_phase5.md` | v1.0 | Phase 5 计划 |
| `docs/code_viewer_design.md` | v2.0 | GUI 设计 |
| `docs/summary_phase3_close.md` | v1.0 | Phase 3 关闭 |
| `docs/summary_phase4_begin.md` | v1.0 | Phase 4 启动 |
| `docs/summary_phase4_end.md` | v1.0 | Phase 4 关闭 |
| **`docs/summary_phase5_end.md`** | **v1.0** | **Phase 5 关闭（本文）** |
| `docs/TESTING_BASELINE.md` | v2.1 | 测试基准 |
| `docs/pyc-format-reference.md` | v1.0 | Python marshal 格式 |
| `README.md` | — | 中英双语 |

### 代码规模

```
PyRebuilderSharp (~30000 行 C# 13 · .NET 10 · Avalonia 11)
├── src/PyRebuilderSharp.Core/   ~25000 行  8 命名空间
├── src/PyRebuilderSharp.Cli/     ~500 行   命令行入口
├── src/PyRebuilderSharp.Gui/    ~1000 行   Avalonia 桌面
├── tests/                        ~5000 行   109 xUnit 测试
└── tools/                         ~200 行   编译/诊断工具
```

---

## 三、技术债务与后续方向

### 已知阻塞

| 问题 | 影响范围 | 根因 |
|:-----|:---------|:------|
| Module `co_names` 读完 | 类名/导入名为 `name_X` | marshal TYPE_REF 节省使 consts 填满文件 |
| `class __name__:` | 类名显示 `__name__` | 同上 |
| `from name_8 import name_9` | abc.3.12 导入名丢失 | 7 个嵌套代码对象累积偏移 |

### 建议后续

1. **修复 marshal 累积偏移** — 在 `ReadMarshalCodeObject` 的 exceptiontable 后加位置校验
2. **`match/case` (3.10+)** — 影响 Python 3.10→3.14 的语法完整性
3. **`except*` (3.11+)** — 3.11+ 异常组语法
4. **walrus `:=` (3.8+)** — DUP_TOP + STORE_FAST 模式检测
5. **展开赋值 AST 组合** — 将多个 STORE_FAST 合并为单一 `Assign(Tuple(...), Call(...))`

---

> **PyRebuilderSharp** — 从 `name_0 = CodeObject: <module>` 到 `def factorial(n):`
>
> Python 字节码反编译器 · .NET 10 · Avalonia UI · 2.7→3.14 · 块级容错
