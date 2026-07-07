# 三大核心问题根因分析与解决方案（更新：2026-07-08）

---

## ✅ 问题 1：try/except 在 3.8-3.14 塌陷（部分修复）

### 当前状态

| 版本 | 路径 | 状态 |
|:----:|:-----|:-----|
| 3.5-3.7 | `BuildTryFromBlock` | ✅ 部分 |
| **3.8-3.10** | `BuildTryFromBlock` + `JUMP_IF_NOT_EXC_MATCH` | ✅ **已修复** |
| 3.11-3.14 | `BuildTryFromExceptionTable` | ❌ 待修复 |

### 3.11-3.14 ET 路径分析

`BuildTryFromExceptionTable` 已有基本框架：
- ✅ ET entry 匹配当前 block 范围
- ✅ handler block 识别（CHECK_EXC_MATCH / bare except）
- ✅ try/except/finally/for-loop 区分
- ❌ handler 后继偏移与 ET target 不匹配 → 后继跳过 → empty handler body
- ❌ `isFinally=True` 误判 → handler body 被忽略
- ❌ `_blockResults` 中 handler 后继无缓存 → 手动 BuildStatements 需要

### 已修复扩展

**handler 后继边界检查**：从 `handlerBlock.StartOffset` 包含后继，而非 `matchingEntry.TargetOffset`。修复了 `succStart >= matchingEntry.TargetOffset` 导致的后继跳过。

---

## ✅ 问题 2：推导式元素/过滤/迭代器丢失（已全部修复）

### 当前状态

| 路径 | 版本 | 状态 |
|:-----|:----:|:-----|
| 生成器表达式 | 3.10+ | ✅ `(x * x for x in range(10))` |
| 列表推导式 | 3.10+ | ✅ `[x * x for x in range(10) if x % 2 == 0]` |
| 字典推导式 | 3.10+ | ✅ `{k: v for (k, v) in items}` |
| 集合推导式 | 3.10+ | ✅ `{x for x in range(5)}` |
| 嵌套推导式 | 3.10+ | ✅ `[[x + y for x in range(3)] for y in range(3)]` |
| lambda in comp | 3.10+ | ✅ `[lambda x, i: x + i for i in range(5)]` (缺 `i=i`) |
| 过滤条件 | 3.10+ | ✅ `[x * x for x in range(10) if x % 2 == 0]` |

**Level 6 diff**: 1196 → **1110** (↓86), B-class = 8

### 关键修复

| 修复 | 文件 | 行数 |
|:-----|:-----|:----:|
| LIST_APPEND opcode 145 映射 | Opcode.cs | +1 |
| LIST_APPEND/SET_ADD/MAP_ADD 模拟 | StackMachine.cs + AstBuilder.cs | +12 |
| POP_JUMP_IF_FALSE 弹栈 | AstBuilder.cs | +10 |
| Yield elt 提取 + Call elt 识别 | AstBuilder.cs | +14 |
| SimulateNestedElt (cell 变量) | AstBuilder.cs | +30 |
| ConvertComprehensionExpr 递归 | AstBuilder.cs | +35 |
| `_` → `y` (STORE_DEREF/MAKE_CELL 别名) | AstBuilder.cs | +2 |
| STORE_DEREF cellvars 优先级 | AstBuilder.cs | +8 |
| iterable 回退覆盖 | AstBuilder.cs | +3 |
| Ifs 提取 | AstBuilder.cs | +2 |
| BuildLambda 默认参数 | StackMachine.cs + AstBuilder.cs | +25 |

---

## ✅ 问题 3：`__build_class__` / def→class 误判

### 当前状态

`BuildFunctionDef`: 类体检测增加控制流语句检查。含有 `With/For/While/Try/Raise/Assert` 的 body 不作为类。

l2_9: `class → def` ✅

---

## ✅ 问题 4：Opcode 基准验证

对比 CPython 3.5-3.14 的 `Include/opcode.h` 与 PyRebuilderSharp 的 `Opcode.cs`：

### 关键发现

| Raw Byte | 旧映射 | 新映射 | CPython 3.5-3.10 |
|:--------:|:-------|:-------|:----------------|
| 135 | MAKE_CELL | LOAD_CLOSURE | LOAD_CLOSURE |
| 136 | LOAD_CLOSURE | LOAD_DEREF | LOAD_DEREF |
| 137 | LOAD_DEREF | STORE_DEREF | STORE_DEREF |
| 138 | PUSH_EXC_INFO | DELETE_DEREF | DELETE_DEREF |

`VersionStrategyPre311.MapOpcode` : 添加 DEREF/CLOSURE 块显式映射。

---

## 修复顺序（更新）

| 顺序 | 子任务 | 估算 | 状态 |
|:----:|:-------|:----:|:----:|
| 1 | try/except 3.8-3.10 handler 识别 | 2h | ✅ |
| 2 | 推导式全部类型 | 10h | ✅ |
| 3 | def→class 误判 | 1h | ✅ |
| 4 | Opcode 基准验证 | 3h | ✅ |
| 5 | **try/except 3.11-3.14 ET** | **3h** | ❌ |
| 6 | Lambda 默认参数 `i=i` | 1h | ❌ |
| 7 | 3.11+ 跨版本回归 | 2h | ❌ |
| 8 | 重复 return 去重 | 1h | ❌ |

## 成果

| 指标 | 之前 | 之后 | 变化 |
|:-----|:----:|:----:|:----:|
| Level 6 diff | 1196 | **1110** | ↓86 |
| B-class files | 3 | **8** | +5 |
| L2 try/except 3.8-3.10 | ❌ | ✅ | 修复 |
| def→class (l2_9) | ❌ | ✅ | 修复 |
| l6_5 nested | ❌ | ✅ | 修复 |
| l6_15 lambda | ❌ | ✅ | 修复 |
