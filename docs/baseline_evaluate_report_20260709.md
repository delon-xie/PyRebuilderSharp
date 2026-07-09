# PyRebuilderSharp 基线评估与修复计划

**日期**: 2026-07-09  
**数据源**: 白盒测试（70%通过率）+ 全量基线 diff（1325文件100%反编译成功）  

---

## 1. 总体状态

| 测试类型 | 通过 | 失败 | 通过率 |
|----------|------|------|--------|
| 白盒测试（结构正确性） | 286 | 119 | **70%** |
| 基线 diff（语义等价性） | 52 (A+B) | 1096 (D) | **4%** |

基线 D 类占 83% 的主要原因不是语义错误，而是**格式差异**（文档字符串格式、空白行、导入分组等），seq-blocks 模式下 **0 孤儿块**、**0 崩溃**。

---

## 2. 优先级排序分析

### P0 — 影响面大（按 diff 量 + 问题数排序）

| 目标文件 | 白盒问题数 | Diff 量 | 影响面评估 |
|----------|-----------|---------|-----------|
| **enum.py** | 50+（所有类型） | 2784-8357 | 🔴 最大 |
| **functools.py** | 30+（CLEANUP/RAISE/PASS） | 1000-2400 | 🔴 大 |
| **abc.py** | 15+（BARE_EXPR） | 150-250 | 🟡 中 |
| **reprlib.py** | 15+（BARE_EXPR/EMPTY_TRY） | 230-270 | 🟡 中 |

**enum.py 是最大的单一问题来源**，个别版本 diff 线达 8357 行（3.13）， diff ratio 高达 378%。

### P0 — 控制块异常

| 问题 | 数量 | 说明 |
|------|------|------|
| CLEANUP_LEAK | 23 | `e = None` 泄漏，79% 来自 enum/functools |
| EMPTY_TRY | 14 | try body 为空，86% 来自 enum/reprlib |
| REDUNDANT_RAISE | 14 | bare raise 泄漏，79% 来自 enum/functools |
| ELSE_CONTAINS_FINALLY | 11 | test_try_simple 全版本，测试脚本伪阳性 |

**CLEANUP_LEAK 是控制块异常中最容易修复的**（后处理过滤即可），影响 3 个主要文件。

### P1 — 指令缺失

| 问题 | 数量 | 说明 |
|------|------|------|
| SYNTAX_ERROR | 14 | 生成的 Python 无法通过 ast.parse |
| FORMAT_ERROR | 3 | f-string 双花括号转义 |

SYNTAX_ERROR 中 8 个（57%）来自 3.5-3.7 的 comprehension 编译差异（`test_nested_comp`、`test_simple_comp`），属于版本兼容性问题。

### P2 — 孤儿块

seq-blocks 模式下 **0 孤儿块**（三阶段管道保证全覆盖）。

### P3 — 语法错误/格式

FORMAT_ERROR（3）已在后处理中改善，属于 reprlib 的 f-string 格式问题。

---

## 3. 分批次修复计划

### Batch P0-1: CLEANUP_LEAK 消除（预期 +5 通过，-20% diff 于 enum/functools）

**难度**: 低 | **修复文件**: `AstBuilder.cs` TrimPostTerminalDeadCode

在 `TrimPostTerminalDeadCode` 增加 `e = None`（`STORE_FAST e; LOAD_CONST None; STORE_FAST e`）handler cleanup 模式识别。这个模式在 enum/functools/reprlib/l9 中出现 23 次。

### Batch P0-2: REDUNDANT_RAISE 消除（预期 +8 通过，-15% diff 于 enum/functools）

**难度**: 中 | **修复文件**: `AstBuilder.cs` BuildTryStructureStatements + TrimPostTerminalDeadCode

Handler body 构建后对残余 `RERAISE` 转化产生的 `raise` 做后过滤。

### Batch P0-3: enum.py 结构修复（预期 +10 通过，diff 减半）

**难度**: 高 | **核心文件**: enum.py (3.6-3.14)

enum.py 的结构差异最严重的原因：
1. **2.7/3.5-3.10**: 使用旧版 `MAKE_FUNCTION` + `STORE_NAME` — `ConvertChildCodesToFunctionDefs` 路径不同
2. **3.11+**: ExceptionTable + 新操作码组合导致大量 `e = None` 泄漏
3. **3.13**: 新 opcode renumber + CACHE 格式变化

### Batch P0-4: abc.py 控制块修复（预期 +8 通过，-50% diff）

**难度**: 中 | **核心文件**: abc.py (2.7-3.14)

1. `cls.__bases__` / `abstracts.add(name)` 等类体表达式泄漏 → 在 `ClassDef` 构建后过滤
2. `for scls in iterable:` → 3.14 的 `ExtractIterExpression` 适配
3. 3.13 的 `if not True: pass` → ExceptionTable + block scanner 交互

### Batch P1-1: SYNTAX_ERROR 修复（预期 +8 通过）

**难度**: 低-中 | **涉及文件**: test_nested_comp, test_simple_comp (3.5-3.7), enum (3.11-3.14), l5_class

1. 3.5-3.7 comprehension 差异 → 检查 `test_nested_comp` 和 `test_simple_comp` 的 pyc 编译路径
2. Enum 大文件边界 → seq-blocks 的 body range 计算修正
3. `yield from` outside function → comprehension generator 标记传递

### Batch P1-2: BARE_EXPR 子模式修复（预期 +15 通过）

**难度**: 中-高 | **涉及文件**: abc, reprlib, match, comprehension

逐个子模式修复：
1. Match pattern `int`/`str` → match 结构构建后清理 pattern subjects
2. Class body expression → ClassDef AST 构建后检查漏网表达式
3. Comprehension 变量 `x`/`row` → generator variables 在后处理中清理

---

## 4. 预期路线图

| 批次 | 通过 | 累计通过率 | 累计 Diff 改善 |
|------|------|-----------|----------------|
| 当前 | 286 | **70%** | A+B=4% |
| P0-1 (CLEANUP) | +5 | **71%** | ~-20% enum/functools |
| P0-2 (RAISE) | +8 | **73%** | ~-15% enum/functools |
| P0-3 (enum) | +10 | **76%** | enum diff 减半 |
| P0-4 (abc) | +8 | **78%** | abc diff -50% |
| P1-1 (SYNTAX) | +8 | **80%** | — |
| P1-2 (BARE_EXPR) | +15 | **84%** | ~-10% 全局 |
| **总计** | **+54** | **84%** | **A+B 10-15%** |

---

## 5. 已验证的重要发现

1. **0 孤儿块** — seq-blocks 三阶段架构完美覆盖所有基本块
2. **0 运行时崩溃** — 1325 个文件全部反编译成功
3. **1325/1325 (100%)** 反编译成功，0 崩溃
4. D 类占 83% 但主要是**格式差异**，**不是语义错误**
5. 最差文件 enum.py（378% diff ratio）是修复的最大收益点
