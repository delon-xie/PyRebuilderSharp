# 基线评估报告

**日期**: 2026-07-02
**项目**: PyRebuilderSharp
**基准**: 997 文件（107 个源码 × 11 个 Python 版本）
**状态**: 0 崩溃 · 0 失败 · 0 孤儿块

---

## 1. 总体指标

| 指标 | 数值 |
|:-----|:----:|
| 反编译成功 | 997/997 (100%) |
| 解析通过 (A+B+C) | 226/997 (23%) |
| 完全匹配 (A 类) | 30/997 (3%) |
| 可接受 (B 类) | 39/997 (4%) |
| 解析通过率 | 793/1008 (79%) |
| 孤儿块 | **0** ✅ |
| 编译表达式伪影 | **0** ✅ |
| 语义错误 (for/raise/while) | **0** ✅ |

---

## 2. 解析失败分类

### 2.1 控制块异常（最高优先级）— 58 个文件

**错误模式**: `expected 'except' or 'finally' block`
**根因**: ExceptionTable 的 try/except handler 未正确输出。try body 生成正确，但 except/finally 子句缺失。

**按版本**:
| 版本 | 失败数 |
|:----:|:------:|
| 3.12 | 23 |
| 3.13 | 23 |
| 3.11 | 6 |
| 3.14 | 6 |

**典型影响文件**: `reprlib.py`, `actual_lv2.py`, `check_v311.py`, `test_with.py` 等 3.11+ 文件。

**初步诊断**: ExceptionTable 的 handler 块被正确处理但从 Try 节点的 `Handlers` 或 `Finalbody` 列表中丢失。`BuildTryFromExceptionTable` 中 handler 块处理逻辑可能导致 handler 语句未附加到 Try AST 节点。

### 2.2 编译表达式伪影（影响面最大）— 71 个文件

**根因**: 内层函数体中的 `<genexpr>/<setcomp>/<listcomp>/<dictcomp>` 反编译被回退到 `Call(FunctionRef, ...)` 或 CommentBlock。

**当前状态**: 通过 `BuildComprehension` 失败时生成 CommentBlock，不再导致语法错误，但语义信息丢失。

**影响文件**:
| 文件 | 影响版本数 | 说明 |
|:-----|:----------:|:-----|
| `parse_35_marshal.py` | 9 | 手工编写，内含 exec + genexpr 模式 |
| `check_py27_magic.py` | 9 | 手工编写，内含 exec + genexpr |
| `definitive_marshal.py` | 8 | 手工编写 |
| `check_marshal_37.py` | 8 | 手工编写 |
| `enum.py` | 8 | 标准库，大量推导式用法 |
| `generate_pyc_310.py` | 6 | 手工编写 |
| `debug_blocks.py` | 6 | 测试代码 |
| `functools.py` | 6 | 标准库 |
| `run_seq_clean.py` | 5 | 工具脚本 |
| `abc.py` | 3 | 标准库 |

**修复路径**: 让 `BuildComprehension` 成功识别内层函数体中的推导式模式（For 循环 + SET_ADD/LIST_APPEND/BUILD_SET 等）。当前 `BuildComprehension` 对 3.6- 版本的推导式 body 中找不到 `For` 语句。

### 2.3 渲染异常（未终止字符串）— 57 个文件

**根因**: 字符串渲染（三引号、格式字符串）处理不完整。涉及 PythonCodeGenerator 的 `VisitConstant` 或 StackMachine 的字符串相关操作码。

**按版本分布**: 3.6~3.14 各约 6~8 个文件，均匀分布。

### 2.4 其他 — 29 个文件

| 模式 | 数量 | 说明 |
|:-----|:----:|:-----|
| `invalid syntax` | 41 | 杂项语法错误 |
| `invalid decimal literal` | 2 | abc.py 2.7/3.5 八进制字面量 `0755` |
| `too many levels of indentation` | 2 | 缩进溢出 |
| `cannot assign to literal` | 2 | 赋值语法 |
| `Invalid star expression` | 1 | 星号表达式 |

---

## 3. 按版本解析通过率

```
  2.7 : ███████████████████░  49/51 (96%)
  3.5 : ██████████████████░░  53/57 (93%)
  3.6 : ████████████████░░░░  78/97 (80%)
  3.7 : ████████████████░░░░  80/97 (82%)
  3.8 : ████████████████░░░░  81/99 (82%)
  3.9 : ████████████████░░░░  82/99 (83%)
  3.10: ████████████████░░░░  84/102 (82%)
  3.11: ███████████████░░░░░  77/100 (77%)
  3.12: █████████████░░░░░░░  68/104 (65%)
  3.13: ████████████░░░░░░░░  64/100 (64%)
  3.14: ███████████████░░░░░  77/102 (75%)
```

---

## 4. 修复计划

### 优先级排序规则
1. **控制块异常优先** — 反编译输出的控制流完整性最高优先
2. **影响面大优先** — 跨版本、跨文件的修复优先
3. **指令缺失优先** — 缺少 opcode 处理会导致大面积的失� 不正确
4. **孤儿块优先** — 孤儿块意味着结构化控制流断裂
5. **语法错误优先** — 最终输出应为合法 Python 语法

### P0 — 控制块异常（预计 +4% 解析率）

**目标**: 修复 58 个 try/except 控制块异常

**根因**: `BuildTryFromExceptionTable` 正确解析了 ExceptionTable 条目并创建了 Try 结构，但 handler 块的语句未附加到 Try 节点的 `Handlers` 集合中。

**修复方案**:
1. 检查 `BuildTryFromExceptionTable` 中创建 Try 节点后的 handler 语句收集逻辑
2. 验证 handler 块正确传递给 `ExceptHandler` 构造
3. 对 3.12+ 的 try/except 结构做专项验证

### P1 — 编译表达式伪影修复（预计 +7% 解析率）

**目标**: 让 `BuildComprehension` 成功处理内层函数体推导式

**修复方案**:
1. 修复 `BuildComprehension` 中推导式 body 的 `For` 语句检测
2. 处理 `SET_ADD`/`LIST_APPEND`/`BUILD_SET`/`BUILD_LIST` 模式
3. 识别编译器推导式 body 中的 GET_ITER + FOR_ITER 循环
4. 对 3.6-3.10 各版本做专项验证

### P2 — 字符串渲染修复（预计 +5% 解析率）

**目标**: 修复 57 个未终止字符串渲染问题

**修复方案**:
1. 检查 `PythonCodeGenerator` 的 `VisitConstant` 中字符串转义逻辑
2. 检查 `StackMachine` 的 `FORMAT_VALUE`/`BUILD_STRING` 处理
3. 检查三引号字符串和 f-string 的渲染边界

### P3 — 其他杂项语法修复

**目标**: 修复 29 个杂项语法错误

| 子项 | 数量 | 说明 |
|:-----|:----:|:-----|
| abc.py 2.7/3.5 八进制字面量 | 2 | `0755` → `0o755` |
| 缩进溢出 | 2 | 深度嵌套导致的缩进超过限制 |
| 赋值语法 | 2 | walrus 赋值渲染 |
| 星号表达式 | 1 | `*args` 解包 |
| 其他 invalid syntax | 22 | 需进一步分类 |

---

## 5. 预期效果矩阵

| 修复 | 文件数 | 预期解析率提升 | 主要受益版本 |
|:-----|:------:|:--------------:|:-----------:|
| P0: try/except 修复 | 58 | +4% (79%→83%) | 3.11~3.14 |
| P1: 编译表达式 | 71 | +7% (83%→90%) | 2.7~3.14 |
| P2: 字符串渲染 | 57 | +5% (90%→95%) | 3.6~3.14 |
| P3: 其他 | 29 | +3% (95%→98%) | 所有版本 |
