# 布尔短路链 → 表达式折叠 修复方案

> 问题：3.13+ 短接布尔链（AND/OR）在 AstBuilder 中被重建为 if/elif 金字塔，
> 而非原始源中的 `return A and B and C` / `return A or B or C` 表达式形式。

---

## 现状

- 943/943 全过，0 崩溃
- `BuildIfElse` 行 2377-2393 已实现 AND/OR BoolOp 合并
  - AND 链：嵌套 If → `If(And(cond1, cond2, ...), body)`
  - OR 链：Partially working
- **最终输出仍有结构质量差距**：`if cond: return True; return False` 而非 `return cond`

---

## 问题 1：AND 链 — Return-Fold 缺失

**Bytecode 模式（3.13+ TO_BOOL + POP_JUMP_IF_FALSE）：**

```python
# 源头码
def _is_dunder(name):
    return (len(name) > 4 and
            name[:2] == name[-2:] == '__' and
            name[2] != '_' and
            name[-3] != '_')

# bytecode
len(name) > 4, TO_BOOL, POP_JUMP_IF_FALSE → return_False
name[:2] == ..., TO_BOOL, POP_JUMP_IF_FALSE → return_False
name[2] != '_', TO_BOOL, POP_JUMP_IF_FALSE → return_False
name[-3] != '_', TO_BOOL, POP_JUMP_IF_FALSE → return_False
return True
return_False: return False
```

**AstBuilder 当前处理：**

| 步骤 | 输入 | 输出 |
|:-----|:-----|:-----|
| AND 合并 (L2377) | `If(cond1, If(cond2, If(cond3, If(cond4, [Ret(T)]))))` + tail=[Ret(F)] | `If(And(cond1,cond2,cond3,cond4), [Ret(T)], null)` + tail=[Ret(F)] |
| **缺少的 fold** | `If(cond, [Ret(T)], null), Ret(F)` | → `Return(cond)` |

**当前输出：**

```python
def _is_dunder(name):
    if len(name) > 4 and name[:2] == name[-2:] == '__' and name[2] != '_' and name[-3] != '_':
        return True
    return False
```

**期望输出：**

```python
def _is_dunder(name):
    return len(name) > 4 and name[:2] == name[-2:] == '__' and name[2] != '_' and name[-3] != '_'
```

### 根因

`BuildIfElse` 行 2377-2386（AND 合并）正确合并了 BoolOp，
但行 2396-2399 将合并后的 `If(And(cond), [Return(True)], null)` 和 `Return(False)`（在 tailCode 中）
分别 emit，**没有做最终的 return 折叠**。

---

## 问题 2：OR 链 — 终端元素取反错误

**Bytecode 模式（3.13+ TO_BOOL + POP_JUMP_IF_TRUE）：**

```python
# 源头码
def _is_descriptor(obj):
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')

# bytecode
hasattr(__get__), TO_BOOL, POP_JUMP_IF_TRUE → return_True     ← or-chain element
hasattr(__set__), TO_BOOL, POP_JUMP_IF_TRUE → return_True     ← or-chain element
hasattr(__delete__), TO_BOOL, POP_JUMP_IF_TRUE → return_True  ← or-chain TERMINAL
return_False
return_True: RETURN True
```

**CFG 结构：**

```
Block A: hasattr(__get__), POP_JUMP_IF_TRUE → D(return_True)
  fallthrough: B
Block B: hasattr(__set__), POP_JUMP_IF_TRUE → D
  fallthrough: C
Block C: hasattr(__delete__), POP_JUMP_IF_TRUE → D
  fallthrough: E(return_False)
Block D: Return(True)
Block E: Return(False)
```

**Bug 位置 — `BuildIfElse` 行 2212-2214：**

```csharp
bool isOrChain = isJumpIfTrue && bodyBranch != null && IsConditionBranch(bodyBranch);
//                     ↑ Block C 的 bodyBranch = E，不是条件分支 → isOrChain = false
if (!isOrChain && isJumpIfTrue && testExpr != null)
    testExpr = new UnaryOp(UnaryOperator.Not, testExpr);  // ← Not(hasattr(__delete__))
```

对于 Block C（最后一个条件），`bodyBranch = E` 是简单的 `Return(False)` 块，
不是条件分支，所以 `isOrChain = false`，条件被取反为 `Not(hasattr(__delete__))`。

**OR 合并（行 2387-2393）产生错误的表达式：**

```
parent:  Or(hasattr(__set__), Not(hasattr(__delete__)))
          ↑ 正确         ↑ 错误（应该是 hasattr(__delete__)）
```

**当前输出：**

```python
def _is_descriptor(obj):
    if hasattr(obj, '__get__') or hasattr(obj, '__set__') or not hasattr(obj, '__delete__'):
        return True
    return False  # 语义错误！
```

### 根因

行 2212-2214 将 OR 链的**终端元素**视为非 OR 链条件，对其取反。
行 2387（OR 合并检查）接收了取反后的条件，产生 `Or(A, B, Not(C))`。

---

## 方案设计

### 阶段 A：OR 链终端修复（~40 行新增）

在 `BuildIfElse` 中，当 `isJumpIfTrue && !isOrChain` 时，不取反条件。
新增一个 OR 链终端分支，保持条件原始形态：

```
if (isJumpIfTrue && !isOrChain
    && bodyStmts.Count == 1 && bodyStmts[0] is Return)
{
    // OR 链终端：if cond: return True（不取反）
    result.Add(new If(testExpr, bodyStmts, null));
    // tailCode 已有 [Return(False)]
}
else
{
    result.Add(new If(testExpr, bodyStmts, orelse));
}
```

**效果：**

```
Before: Or(hasattr(__get__), Not(hasattr(__delete__)))    ← 错误
After:  Or(hasattr(__get__), Or(hasattr(__set__), hasattr(__delete__)))    ← 正确
```

---

### 阶段 B：PostProcessReturnFold（~40 行新增）

新增 `FoldReturnIf(statements)` 方法，在 `PostProcessFunctionDefs` 末尾调用。

**规则 1 — 基础 Return 折叠：**

```
模式: If(cond, [Return(True)], null), Return(False)
变换: → Return(cond)
```

**规则 1b — 反转 Return 折叠：**

```
模式: If(cond, [Return(False)], null), Return(True)
变换: → Return(UnaryOp(Not, cond))
```

**规则 2 — else 分支 Return 折叠（扩展）：**

```
模式: If(cond, [Return(True)], [Return(False)])
变换: → Return(cond)
```

```
模式: If(cond, [Return(False)], [Return(True)])
变换: → Return(Not(cond))
```

**实现要点：**

- 从后向前扫描（`i = count - 2` → `0`），因为折叠会缩短列表
- 只处理 `body[0] is Return` 且下一个顶层语句是 `Return` 的情况
- 不触及非 `Return` 的 body（有副作用的代码保持 if/else 结构）
- 在 `PostProcessFunctionDefs` 末尾调用，作用于每个函数的 `functionStmts`

**效果（以 `_is_dunder` 为例）：**

```python
# 折叠前
def _is_dunder(name):
    if len(name) > 4 and name[:2] == name[-2:] == '__' and name[2] != '_' and name[-3] != '_':
        return True
    return False

# 折叠后
def _is_dunder(name):
    return len(name) > 4 and name[:2] == name[-2:] == '__' and name[2] != '_' and name[-3] != '_'
```

---

## 受影响函数清单

| 函数 | 版本 | 模式 | 当前问题 | 阶段 A 修复 | 阶段 B 修复 |
|:-----|:-----|:-----|:---------|:-----------|:-----------|
| `_is_dunder` | 2.7-3.14 | AND 链 | if→return True/False | — | ✅ return cond |
| `_is_sunder` | 2.7-3.14 | AND 链 | if→return True/False | — | ✅ return cond |
| `_is_descriptor` | 2.7-3.14 | OR 链 | Not(C) 语义错误 | ✅ 修正表达式 | ✅ return cond |
| `_is_single_bit` | all | if/else | 已正确 | — | — |
| `_power_of_two` | all | if/else | 待验证 | — | 可能折叠 |
| `_check_foruse_class` | ≤3.12 | 混合 | 待验证 | — | 可能折叠 |
| `_make_class_unpicklable` | all | 非 return | — | — | 无影响 |
| `__format__` | all | 复杂 | 待验证 | — | 无影响 |
| `_create_` | all | 混合 | 待验证 | — | 可能折叠 |

---

## 回归风险评估

| 风险 | 说明 | 缓解 |
|:----|:-----|:-----|
| **崩溃风险** | 零 — 纯 AST 变换，不触 CFG/bytecode | 无 CFG/bytecode 路径变更 |
| **语义风险** | 极低 — 仅对 `If(cond, [Ret(T)], null), Ret(F)` 模式操作 | 全版本回归测试（943 文件） |
| **非目标函数影响** | 无 — 只匹配精确的 If-Return 模式 | 其他控制流完全不变 |
| **尾代码误吞** | 低 — 从后向前扫描确保不跳过中间语句 | 只有连续 if→ret; ret 才触发 |

---

## 验证步骤

```
1. 阶段 A 编码 → dotnet build
2. 验证 _is_descriptor 输出 hasattr(__get__) or hasattr(__set__) or hasattr(__delete__)
3. 批量回归 943/943
4. 阶段 B 编码 → dotnet build  
5. 验证 _is_dunder / _is_sunder 输出 return cond
6. 批量回归 + 基线报告更新
7. 提交 + 推送
```

---

## 代码位置总览

| 修改点 | 文件 | 行号 | 变更类型 |
|:-------|:-----|:-----|:---------|
| OR 终端修复 | `AstBuilder.cs` | L2212-2214 | 修改逻辑，不取反 terminal OR element |
| OR 终端分支 | `AstBuilder.cs` | L2395 附近 | 新增分支，emit `If(cond, [Ret(T)], null)` |
| FoldReturnIf | `AstBuilder.cs` | 新建方法 | ~40 行新代码 |
| 调用入口 | `AstBuilder.cs` | PostProcessFunctionDefs 末尾 | 调用 FoldReturnIf |
