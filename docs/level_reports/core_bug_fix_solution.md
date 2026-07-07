# 三大核心问题根因分析与解决方案（更新：2026-07-07）

---

## ✅ 问题 1：try/except 在 3.8-3.14 塌陷（部分修复）

### 当前状态

| 版本 | 路径 | 状态 |
|:----:|:-----|:-----|
| 3.5-3.7 | `BuildTryFromBlock` | ✅ 部分 |
| **3.8-3.10** | `BuildTryFromBlock` + `JUMP_IF_NOT_EXC_MATCH` | ✅ **已修复** |
| 3.11-3.14 | `BuildTryFromExceptionTable` | ❌ 待修复 |

### 已完成修复

| 修复 | 文件 | 行数 |
|:-----|:-----|:----:|
| `JUMP_IF_NOT_EXC_MATCH` StackMachine 处理 | StackMachine.cs | +5 |
| `DUP_TOP` 后向 `i+1` 类型检测 (3.8+) | AstBuilder.cs | +20 |
| `CHECK_EXC_MATCH`/`CHECK_EG_MATCH` 处理 | AstBuilder.cs | +20 |
| `POP_EXCEPT` break→continue (保留 handler return) | AstBuilder.cs | +2 |
| SETUP_EXCEPT 移出 BlockScanner（避免污染 JUMP_IF_NOT_EXC_MATCH） | BlockScanner.cs | ±1 |
| 内联 handler fallback（handler 与 try 同一块时） | AstBuilder.cs | +80 |

---

## ✅ 问题 2：推导式元素/过滤/迭代器丢失（部分修复）

### 当前状态

| 路径 | 版本 | 状态 |
|:-----|:----:|:-----|
| **生成器表达式** | 3.10+ | ✅ `(x * x for x in range(10))` |
| **列表推导式** | 3.10+ | ✅ `[x * x for x in range(10)]` |
| 字典推导式 | 3.10+ | ❌ `{(k,v):(k,v) for _ in iterable}` |
| 集合推导式 | 3.10+ | ❌ `{x for x in iterable}` |
| 嵌套推导式 | 3.10+ | ❌ 完全崩坏 |
| 过滤条件 | 3.10+ | ❌ `if x%2==0` 丢失 |

### 已完成修复

| 修复 | 文件 | 行数 |
|:-----|:-----|:----:|
| LIST_APPEND opcode 145 映射 (3.10) | Opcode.cs | +1 |
| LIST_APPEND StackMachine 处理同步 | StackMachine.cs | +1 |
| LIST_APPEND _313→_310 检测 6 处 | AstBuilder.cs | +12 |
| appendOpcode 选择逻辑 (bodyBlocks 检测) | AstBuilder.cs | +1 |
| elt 栈提取顺序 (BinOp→elt, 非 Name) | AstBuilder.cs | +9 |
| BuildComprehensionFallback Assign+ListComp 识别 | AstBuilder.cs | +6 |
| POP_JUMP_IF_FALSE 模拟弹栈 | AstBuilder.cs | +10 |
| Yield elt 提取 (generator) | AstBuilder.cs | +1 |

### 剩余难点

| 问题 | 根因 | 估算 |
|:-----|:-----|:----:|
| dict key/value | MAP_ADD 消耗 _exprStack，InnermostFor.Body 为空 | 2h |
| set iterable | SET_ADD 同上 | 1h |
| 过滤条件 | elt 模拟中条件被跳过（POP_JUMP_IF_FALSE 已修复） | 1h |
| 嵌套推导式 | 各层推导式的 target/iter 赋值混乱 | 3h |

---

## ❌ 问题 3：`__build_class__` 模式匹配失败（~10K diff）

未开始。

---

## 修复顺序（更新）

| 顺序 | 子任务 | 估算 | 状态 |
|:----:|:-------|:----:|:----:|
| 1 | try/except 3.8-3.10 handler 识别 | 2h | ✅ 完成 |
| 2 | 生成器表达式 `Yield` elt 提取 | 0.5h | ✅ 完成 |
| 3 | 列表推导式 LIST_APPEND + elt 模拟 | 3h | ✅ 完成 |
| 4 | 字典推导式 MAP_ADD body 提取 | 2h | ❌ |
| 5 | try/except 3.11-3.14 ET body 提取 | 2h | ❌ |
| 6 | `__build_class__` 优先检测 | 1h | ❌ |

## 成果

- **l6_2/3**：生成器和列表推导式正确恢复 ✅
- **Level 6 diff**: 1196 → 1158 ↓38, B 类维持
- **Level 2 diff**: try/except 3.8-3.10 结构正确
