# Phase 4 收尾总结 — PyRebuilderSharp

**版本**: v1.0
**日期**: 2026-06-14
**项目**: PyRebuilderSharp (.NET 10 + Avalonia GUI)

---

## 一、核心成就

### 🏆 从 `name_0 = CodeObject` 到完整可读的 Python 源码

```
Phase 3 最终:      name_0 = CodeObject: <module> (5 instrs)  ← 垃圾
Phase 4 P0-1:     def greet(name):                         ← ✅ 函数定义
                  def add(a, b):                           ← ✅
                  def factorial(n):                        ✅
Phase 4 P0-2:     class __name__:                           ← ✅ 类定义 (首次!)
                      def __init__(self, value):             ✅ 方法
                          pass
Phase 4 P0-3:     yield x / yield from iter               ← ✅ 生成器
Phase 4 P1-1:     @property / @staticmethod                 ← ✅ 装饰器
Phase 4 P1-2:     async def f(): / await ...                ← ✅ 异步
```

### ✅ Phase 4 覆盖语法

| 语法 | 状态 | 说明 |
|:-----|:------|:------|
| `def` 函数定义 | ✅ | 参数、返回值、闭包 |
| `class` 类定义 | ✅ | 方法、类级属性、`__init__` |
| `return` | ✅ | 返回值 |
| `yield` / `yield from` | ✅ | 生成器 |
| `@decorator` | ✅ | 装饰器链 |
| `async def` / `await` | ✅ | AST 节点+代码生成 |
| `if/elif/else` | ✅ | Phase 3 |
| `for/while` | ✅ | Phase 3 |
| `try/except/finally` | ✅ | Phase 3 |
| `a, b = ...` 展开 | ❌ | UNPACK_SEQUENCE 未实现 |
| `match/case` | ❌ | 3.10+ 待支持 |
| 类型注解 `x: int` | ❌ | 待支持 |
| `:=` walrus | ❌ | 待支持 |

---

## 二、8 个 marshal 3.11+ 修复（Phase 4 关键技术突破）

Phase 4 发现 Python 3.11+ marshal 格式发生根本性变化，逐一修复：

| # | 问题发现 | 修复 | 文件 |
|:-:|:---------|:------|:-----|
| 1 | 3.11+ 去掉 `varnames/freevars/cellvars` | 改为 `localsplusnames + localspluskinds` | `PycReader.cs` |
| 2 | `localspluskinds` 存为 TYPE_STRING(0x73) | 用 `ReadRawMarshalBytes` 代替 `ReadMarshalObject` | `PycReader.cs` |
| 3 | `ReadRawMarshalBytes` 不预留 ref slot | 加 FLAG_REF 预插槽 | `PycReader.cs` |
| 4 | `ReadMarshalObjectAsStrList` 容器 FLAG_REF 未处理 | 容器预留 + 填充 | `PycReader.cs` |
| 5 | `exceptiontable` 用 TYPE_REF(0x72) | PEEK 检查 + 读 TYPE_REF | `PycReader.cs` |
| 6 | 0x73 在 names 上下文中被当 TYPE_CODE_SIMPLE | `ReadOneMarshalString` 单独处理 | `PycReader.cs` |
| 7 | `HandleUnknownMarshalType` type<4 跳到 EOF | 直接 return null, 不跳过 | `PycReader.cs` |
| 8 | `MAKE_FUNCTION` 在 3.12 只 pop 1 项 | `_isPython312` + pop 1 项 | `StackMachine.cs` |

### 核心发现：Python 3.11+ marshal Code Object 格式

```
3.10-格式:                   3.11+格式:
  argcount                     argcount
  posonlyargcount              posonlyargcount
  kwonlyargcount               kwonlyargcount
  nlocals                      stacksize
  stacksize                    flags
  flags                        code
  code                          consts
  consts                       names
  names                        localsplusnames ← 合并 varnames+freevars+cellvars
  varnames                     localspluskinds ← 0x20=local 0x40=cell 0x80=free
  freevars                     filename
  cellvars                     name
  filename                     qualname ← 新增
  name                         firstlineno
  firstlineno                  linetable ← 替代 lnotab
  lnotab                       exceptiontable ← 新增
```

---

## 三、版本矩阵测试

### 2.7 → 3.14 全覆盖

| 套件 | 版本 | 通过率 |
|:-----|:-----|:-------|
| Lv0_Expressions | 2.7, 3.5-3.14 (11) | ✅ 11/11 |
| Lv1_Sequential | 2.7, 3.5-3.14 (11) | ✅ 11/11 |
| Lv2_ControlFlow | 2.7, 3.5-3.14 (11) | ✅ 11/11 |
| Lv3_NestedDepth(5层) | 2.7-3.14 (11) | ✅ 11/11 |
| Lv3_NestedMixed | 2.7-3.14 (11) | ✅ 11/11 |
| Lv3_NestedMatrix | 2.7-3.14 (11) | ✅ 11/11 |
| Lv3-1_NestedDepth9(九层塔) | 2.7-3.14 (11) | ✅ 11/11 |
| **版本矩阵合计** | **77/77** | **✅ 100%** |

### 全部测试

| 指标 | 数值 | 状态 |
|:-----|:-----|:------|
| xUnit 测试总数 | 109 | — |
| 通过 | 102 | ✅ |
| 失败（预存） | 7 | 🔧 |
| 通过率 | 93.6% | ✅ |
| Marsha警告 | 0/182 | ✅ |

---

## 四、九层塔测试（Lv3-1）

新增 `test_nested_depth_9.py` — 4 个函数 × 9 层混合嵌套：

| 函数 | 模式 | 版本 |
|:-----|:-----|:-----|
| `nine_level_if_for_while_try` | if > for > while > try 镜像 | 2.7→3.14 ✅ |
| `nine_level_try_except_finally` | 9 层 try-except-finally | 2.7→3.14 ✅ |
| `nine_level_all_control` | if/elif/else + for + while + try 全混合 | 2.7→3.14 ✅ |
| `nine_level_deep_assign` | 9 层 if 赋值链 | 2.7→3.14 ✅ |

编译脚本：`tools/compile_test_data.py` — 自动扫描本机 Python 版本，批量编译全部 .py 文件。

---

## 五、Phase 3 + 4 合并状态

### Phase 3 ✅

| C1 | C2 | C3 | C4 |
|:--:|:--:|:--:|:--:|
| Marshal 修复 | 测试矩阵 | CrashCollector | Lv3 嵌套 |
| ✅ 8 修复 0 警告 | ✅ 182/182 | ✅ JSON 收集 | ✅ 33/33 |

### Phase 4 ✅

| P0-1 | P0-2 | P0-3 | P1-1 | P1-2 | P1-3 | P2 |
|:----:|:----:|:----:|:----:|:----:|:----:|:--:|
| `def` ✅ | `class` ✅ | `yield` ✅ | `@` ✅ | `async` ✅ | ❌ | ❌ |

### 文档

| 文档 | 版本 |
|:-----|:------|
| `docs/Python反编译总体设计.md` | v2.6 |
| `docs/Python反编译详细设计.md` | v2.5 |
| `docs/plan_phase5.md` | — (待创建) |
| `docs/code_viewer_design.md` | v2.0 |
| `docs/summary_phase3_close.md` | v1.0 |
| `docs/summary_phase4_begin.md` | v1.0 |
| **`docs/summary_phase4_end.md`** | **v1.0 (本次)** |
| `docs/TESTING_BASELINE.md` | v2.1 |
| `docs/pyc-format-reference.md` | v1.0 |
| `quick_start.md` | — |
| `README.md` (中英双语) | — |

---

## 六、技术债务与阻塞

### 已知阻塞

| 问题 | 影响 | 根因 |
|:-----|:-----|:------|
| module `co_names` 读完 | 类名/导入名为 `name_X` | marshal TYPE_REF 节省使 consts 填满文件 |
| abc.3.12 co_names 空 | `from name_8 import name_9` | 同上，7 个嵌套代码对象累积偏移 |
| `class __name__:` | 类名显示 `__name__` 而非 `SimpleClass` | 同上 |

### 预存测试失败 (7)

| 测试 | 原因 |
|:-----|:------|
| PycReaderTests ×4 | `simple_const.3.8.pyc` 文件路径问题 |
| StackMachineTests ×2 | BinaryAdd opcode 映射 |
| TokenDumperTests ×1 | Token 输出格式预期值 |

---

## 七、项目结构

```
PyRebuilderSharp.slnx
├── src/
│   ├── PyRebuilderSharp.Core/
│   │   ├── Builders/       (AstBuilder + BlockDecompiler)
│   │   ├── Generators/     (PythonCodeGenerator)
│   │   ├── Models/          (AST + Bytecode + CFG)
│   │   ├── Readers/         (PycReader + Marshal)
│   │   ├── Scanners/        (BlockScanner + CFScanner)
│   │   ├── Services/        (CrashCollector)
│   │   └── Decompiler.cs
│   ├── PyRebuilderSharp.Cli/
│   └── PyRebuilderSharp.Gui/   (Avalonia)
├── tests/
│   └── PyRebuilderSharp.Tests/  (109 xUnit)
├── tools/
│   └── compile_test_data.py
└── docs/  (11 documents)
```

---

> **PyRebuilderSharp** — 从 Python 字节码中重建源码，块级容错。
>
> Block-by-block Python bytecode decompiler with fault tolerance.
>
> 从 `name_0 = CodeObject` → `def factorial(n):` 🚀
