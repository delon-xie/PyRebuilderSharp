# Phase 5 工程增强计划

**版本**: v1.0
**日期**: 2026-06-14
**前提**: Phase 3 ✅ · Phase 4 ✅ — def/class/yield/@decorator/async 全部覆盖

---

## 一、Phase 5 目标

从"语法覆盖"到**工程完善**：补齐剩余语法、将 benchmark 文件纳入矩阵测试、完善输出质量。

---

## 二、Python 语法覆盖清单

### ✅ 已支持

| 语法 | 版本支持 | 测试 |
|:-----|:---------|:-----|
| 算术/比较/逻辑表达式 | 2.7→3.14 | Lv0 |
| 赋值、复合赋值 | 2.7→3.14 | Lv1 |
| 函数调用、返回 | 2.7→3.14 | Lv1 |
| `if/elif/else` | 2.7→3.14 | Lv2 |
| `for` / `while` | 2.7→3.14 | Lv2 |
| `try/except/finally` | 2.7→3.14 | Lv2 |
| `def` 函数定义 | 2.7→3.14 | P0-1 |
| `class` 类定义 | 2.7→3.14 | P0-2 |
| `yield` / `yield from` | 2.7→3.14 | P0-3 |
| `@decorator` | 2.7→3.14 | P1-1 |
| `async def` / `await` | 3.5→3.14 | P1-2 |
| `raise` / `assert` | 2.7→3.14 | Lv2 |
| `import` / `from X import` | 2.7→3.14 | Lv1 |
| `lambda` | 2.7→3.14 | Built-in |
| 列表/字典/集合推导式 | 2.7→3.14 | Lv0 |
| `with` 语句 | 2.7→3.14 | Lv2 |
| f-string (3.6+) | 3.6→3.14 | Lv1 |
| 类型注解 (3.5+) | 3.5→3.14 | Lv0 (解析) |

### ❌ 未支持

| # | 语法 | 版本 | 复杂度 | 优先级 |
|:-:|:-----|:-----|:-------|:------:|
| 1 | **展开赋值** `a, b = ...` | 2.7→3.14 | 🟡 中 | P5-1 |
| 2 | **`match/case`** (3.10+) | 3.10→3.14 | 🔴 高 | P5-2 |
| 3 | **类型注解渲染** `x: int = 1` | 3.5→3.14 | 🟢 低 | P5-3 |
| 4 | **walrus 运算符** `:=` (3.8+) | 3.8→3.14 | 🟢 低 | P5-4 |
| 5 | **`global` / `nonlocal`** | 2.7→3.14 | 🟢 低 | P5-5 |
| 6 | **`del` 语句** | 2.7→3.14 | 🟢 低 | P5-6 |
| 7 | **`breakpoint()`** (3.7+) | 3.7→3.14 | 🟢 低 | P5-7 |
| 8 | **赋值表达式在推导式中** | 3.8→3.14 | 🟡 中 | P5-8 |
| 9 | **`except*`** (3.11+) | 3.11→3.14 | 🔴 高 | P5-9 |

---

## 三、Benchmark 文件矩阵测试

### 现状

`test_data/compiled/` 有 182 个文件（91 × v3.11/v3.12），当前仅作为 marshal 基准使用（验证不崩溃），未纳入 AST 语义比较。

### 目标

将 benchmark 文件加入 xUnit 版本矩阵测试：

```csharp
[Theory]
[InlineData("abc.3.12.pyc")]
[InlineData("typing.3.12.pyc")]
public void Benchmark_V312(string pycFile) { ... }
```

### 步骤

1. 按语法复杂度对 benchmark 文件分类（简单/中等/复杂）
2. 简单文件直接纳入 AST 语义比较
3. 中等/复杂文件先标记为 `known_issue`，逐步收敛

---

## 四、任务拆解

### P5-1: 展开赋值 `a, b = ...` 🟡 中

| 子任务 | 预估 | 依赖 |
|:-------|:-----|:------|
| 添加 `Starred` AST 节点 | 1 call | — |
| StackMachine: `UNPACK_SEQUENCE` 展开 | 2 calls | Starred 节点 |
| StackMachine: `UNPACK_EX` 支持 `*rest` | 1 call | — |
| 生成 `Assign(Tuple([a,b]), Call)` | 1 call | 展开逻辑 |
| 测试: `a, b = func()`, `a, *rest = iter` | 1 call | — |

### P5-2: `match/case` (3.10+) 🔴 高

| 子任务 | 预估 | 依赖 |
|:-------|:-----|:------|
| 添加 3.10+ MATCH opcodes 映射 | 2 calls | Opcode.cs |
| 添加 `Match` / `Case` AST 节点 | 1 call | — |
| StackMachine: MATCH 指令处理 | 3 calls | AST 节点 |
| 代码生成: `match x:\n case y:` | 2 calls | AST → codegen |
| 测试 | 1 call | — |

### P5-3 到 P5-9: 其他语法

| 任务 | 预估调用数 |
|:-----|:----------|
| 类型注解 `x: int` 渲染 | 2 |
| walrus `:=` | 1 |
| `global` / `nonlocal` | 1 |
| `del` 语句 | 1 |
| `except*` (3.11+) | 3 |

---

## 五、Phase 5 执行顺序

```
Phase 5 ──┬── P5-1: 展开赋值 (2-3 calls)  ← 最优先
          ├── P5-2: match/case (8-9 calls) ← 影响 3.10+ 输出完整性
          ├── P5-3: 类型注解 (2 calls)
          ├── P5-4~P5-9: 其余语法 (8 calls)
          └── Benchmark 矩阵纳入 (3 calls)
```

---

## 六、Benchmark 文件分类

### 简单（可直接纳入 AST 比较）

| 文件 | 说明 |
|:-----|:------|
| `test_seq_clean.py` | 顺序代码 |
| `test_expr_basic.py` | 表达式 |
| `test_control_flow.py` | 控制流 |
| `test_simple_def.py` | 简单函数 |
| `test_yield_simple.py` | yield |
| `test_yield_gen.py` | 生成器 |
| `test_async.py` | async |

### 中等（需先验证关键语法）

| 文件 | 说明 |
|:-----|:------|
| `abc.py` | ABC 元类 |
| `test_syntax.py` | 语法覆盖测试 |
| `decompiled_depth_5.py` | 嵌套函数 |
| `mixed5_out.py` | 混合嵌套 |

### 复杂（需逐项修复）

| 文件 | 说明 |
|:-----|:------|
| `typing.py` | typing 模块（138KB） |
| `enum.py` | enum 模块 |
| `dataclasses.py` | dataclasses 模块 |
| `functools.py` | functools 模块 |
| `pprint.py` | pprint 模块 |
| `contextlib.py` | contextlib 模块 |
| `ast.py` | ast 模块 |
| `reprlib.py` | reprlib 模块 |

---

## 七、测试基准

```bash
# 完整测试
dotnet test tests/PyRebuilderSharp.Tests -c Release

# Phase 5 专项
dotnet test --filter "Benchmark"
dotnet test --filter "P5"

# marshal 基准
dotnet run --project tools/MarshalDiag
```
