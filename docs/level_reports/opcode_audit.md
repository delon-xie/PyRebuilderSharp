# Opcode 基准验证报告

## 方法

从 CPython 官方 GitHub 仓库 (python/cpython) 的 tag `v3.5.0` 到 `v3.14.0` 获取 `Include/opcode.h`，
与 PyRebuilderSharp 的 `Opcode.cs` 进行比较。

---

## 关键发现

### 问题 1：3.5-3.10 DEREF/CLOSURE 操作码偏移

PyRebuilderSharp 使用 3.11+ 的 opcode 映射，但 `VersionStrategyPre311` 对 raw bytes 做直接投射 `(Opcode)rawOp`，
导致 3.5-3.10 的 DEREF/CLOSURE/PUSH_EXC 操作码全部映射错误：

| Raw Byte | CPython 3.5-3.10 | PyRebuilder 设为 | 含义 |
|:--------:|:-----------------|:-----------------|:-----|
| 135 | LOAD_CLOSURE | MAKE_CELL | 闭包加载→make cell |
| 136 | LOAD_DEREF | LOAD_CLOSURE | 自由变量加载→闭包加载 |
| 137 | STORE_DEREF | LOAD_DEREF | cell 变量存储→自由变量加载 |
| 138 | DELETE_DEREF | PUSH_EXC_INFO | cell 变量删除→异常压栈 |

**已修复**：`ExtractLoopVariable` 和 `ExtractUnpackNames` 已添加 `MAKE_CELL` 作为 `STORE_DEREF` 的别名。

**未修复**：StackMachine 中 3.5-3.10 的 `STORE_DEREF`/`LOAD_DEREF`/`DELETE_DEREF` 跳转到错误的 handler。

### 问题 2：3.5-3.9 的 SETUP_LOOP/BREAK_LOOP/CONTINUE_LOOP 操作码

| Raw Byte | CPython 3.5-3.9 | PyRebuilder 设为 |
|:--------:|:----------------|:-----------------|
| 119 | CONTINUE_LOOP | RERAISE |
| 120 | SETUP_LOOP | COPY |
| 121 | SETUP_EXCEPT | JUMP_IF_NOT_EXC_MATCH |

未验证。

### 问题 3：内部操作码（PyRebuilder 自创）

PyRebuilder 定义了一组不在任何 CPython 版本中的内部操作码（值 181-262），
包括 `_312` 和 `_313` 后缀的版本特定映射，这些是正常的内部抽象。

---

## 各版本对照表

以下仅列出 PyRebuilder 与 CPython 在同一 raw byte value 上有不同名字的操作码，
按版本分组。

### 3.5-3.10 共有问题

| 值 | PyRebuilder | 3.5 | 3.6 | 3.7 | 3.8 | 3.9 | 3.10 |
|:--:|:------------|:----|:----|:----|:----|:----|:-----|
| 49 | STORE_SUBSCR | − | − | − | − | WITH_EXCEPT_START | WITH_EXCEPT_START |
| 50 | DELETE_SLICE_0 | GET_AITER | GET_AITER | GET_AITER | GET_AITER | GET_AITER | GET_AITER |
| 53 | DELETE_SLICE_3 | − | − | − | BEGIN_FINALLY | − | − |
| 87 | YIELD_FROM | POP_BLOCK | POP_BLOCK | POP_BLOCK | POP_BLOCK | POP_BLOCK | POP_BLOCK |
| 103 | DELETE_NAME | BUILD_LIST | BUILD_LIST | BUILD_LIST | BUILD_LIST | BUILD_LIST | BUILD_LIST |
| 119 | RERAISE | CONTINUE_LOOP | CONTINUE_LOOP | CONTINUE_LOOP | − | − | − |
| 120 | COPY | SETUP_LOOP | SETUP_LOOP | SETUP_LOOP | − | − | − |
| 121 | JUMP_IF_NOT_EXC_MATCH | SETUP_EXCEPT | SETUP_EXCEPT | SETUP_EXCEPT | − | − | − |
| 135 | MAKE_CELL | LOAD_CLOSURE | LOAD_CLOSURE | LOAD_CLOSURE | LOAD_CLOSURE | LOAD_CLOSURE | LOAD_CLOSURE |
| 136 | LOAD_CLOSURE | LOAD_DEREF | LOAD_DEREF | LOAD_DEREF | LOAD_DEREF | LOAD_DEREF | LOAD_DEREF |
| 137 | LOAD_DEREF | STORE_DEREF | STORE_DEREF | STORE_DEREF | STORE_DEREF | STORE_DEREF | STORE_DEREF |
| 138 | PUSH_EXC_INFO | DELETE_DEREF | DELETE_DEREF | DELETE_DEREF | DELETE_DEREF | DELETE_DEREF | DELETE_DEREF |

### 3.11+ 上 PyRebuilder 新增的映射

3.11+ 版本重新分配了操作码编号，PyRebuilder 大部分匹配。以下例外：

| 值 | 3.11 | 3.12 | PyRebuilder |
|:--:|:-----|:-----|:------------|
| 166 | PRECALL | UNPACK_SEQUENCE_TUPLE | PRECALL_311 |
| 167 | STORE_FAST__STORE_FAST | UNPACK_SEQUENCE_TWO_TUPLE | CALL_311 |
| 173 | POP_JUMP_BACKWARD_IF_NOT_NONE | − | CALL_INTRINSIC_1 |
| 255 | DO_TRACING | − | LOAD_FAST_BORROW_314 |

---

## 影响范围

| 问题 | 影响版本 | 严重度 | 当前状态 |
|:-----|:---------|:------:|:--------|
| DEREF/CLOSURE 偏移 | 3.5-3.10 | **高** | 部分修复（循环变量提取已修补，StackMachine 未修复） |
| 消逝操作码（SLICE_x、DELETE_SLICE_x） | 3.5-3.12 | 中 | 2.x 遗留，现代版本不使用 |
| SETUP_LOOP/CONTINUE_LOOP 混淆 | 3.5-3.7 | 中 | 3.8+ 已废弃，不影响 3.10+ |
| WITH_EXCEPT_START 共享 49 | 3.9-3.12 | 中 | STORE_SUBSCR 在不同版本有不同编号 |

---

## 建议修复优先级

1. **StackMachine 的 LOAD_DEREF/STORE_DEREF 版本感知** — 减少 `_cell` 变量名错误
2. **VersionStrategyPre311 添加显式 MapOpcode 覆写** — 解决整个偏移族
3. **通用 opcode 处理框架** — 无版本检查的 handler 使用 switch/case 按版本分发
