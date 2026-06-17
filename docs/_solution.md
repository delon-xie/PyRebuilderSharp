# 布尔短路链 → 表达式折叠 修复方案（修订版）

> 问题：AND 短路链在 AstBuilder 中被重建为 `if cond: return True; return False`，
> 而非原始源中的 `return A and B and C` 表达式形式。

---

## 现状（2026-06-17 修订）

- 943/943 全过，0 崩溃
- AND 链 BoolOp 合并已工作：`BuildIfElse` 行 2377-2386 将嵌套 `if cond1: if cond2: ...` 合并为 `If(And(cond1, cond2, ...), body)`
- **最终输出仍有代码质量问题**：`if cond: return True; return False` 而非 `return cond`

### ⛔ OR 链已延迟（3.13+ 结构问题）

3.13+ 中 `return A or B or C` 的 bytecode 使用了以下模式：
```
COPY 1 + TO_BOOL + POP_JUMP_IF_TRUE → shared RETURN_VALUE
POP_TOP (discard on short-circuit failure)
```
这导致终端条件块（最终的 `C`）**没有 POP_JUMP_IF_TRUE** 作为最后一条指令
（仅以 CALL 结尾），因此 `IsConditionBranch` 返回 false，破坏了 OR 链检测。

同时 `NOT_TAKEN` 伪指令和 `COPY 1 + POP_TOP` 的操作码序列需要在
BlockScanner 层面支持（Leader 标记 + 块合并），是更大范围的改造。

**OR 链修复列为独立任务**，不在本次提交中处理。

---

## 受影响函数（仅 AND 链）

| 函数 | 版本 | 当前输出 | 理想输出 |
|:-----|:-----|:---------|:---------|
| `_is_dunder` | 2.7-3.14 | `if A and B and C: return D` | `return A and B and C and D` |
| `_is_sunder` | 2.7-3.14 | 同上 | `return ...` |
| `_is_single_bit` | all | 已正确（含 side-effect） | — |
| `_power_of_two` | all | 待验证 | 可能折叠 |

---

## 解决方案：PostProcessReturnFold（~50 行）

新增 `FoldReturnIf(statements)` 方法，在 `PostProcessFunctionDefs` 末尾调用。

### 规则 1 — Return-Fold（核心）

```
检测: If(cond, [Return(True)], null), Return(False)
变换: → Return(cond)
```

```
检测: If(cond, [Return(False)], null), Return(True)
变换: → Return(UnaryOp(Not, cond))
```

### 规则 2 — else 分支 Return-Fold（扩展）

```
检测: If(cond, [Return(True)], [Return(False)])
变换: → Return(cond)
```

```
检测: If(cond, [Return(False)], [Return(True)])
变换: → Return(Not(cond))
```

### 实现要点

- 从后向前扫描（`i = count - 2` → `0`）
- 只处理 `body[0] is Return` 且下一个顶层语句是 `Return` 的情况
- 不触及非 `Return` 的 body（有副作用的代码保持 if/else）
- 在 `PostProcessFunctionDefs` 末尾调用
- 全版本受益（2.7-3.14 的 AND 短路链）

### 效果

```python
# 折叠前
def _is_dunder(name):
    if len(name) > 4 and name[:2] == name[-2:] == '__' and name[2] != '_':
        return name[-3] != '_'
    return False

# 折叠后  
def _is_dunder(name):
    return len(name) > 4 and name[:2] == name[-2:] == '__' and name[2] != '_' and name[-3] != '_'
```

---

## 回归风险评估

| 风险 | 说明 | 缓解 |
|:----|:-----|:-----|
| **崩溃风险** | 零 — 纯 AST 变换 | 无 CFG/bytecode 路径变更 |
| **语义风险** | 极低 — 仅对 If-Return-False 模式 | 全版本回归 943 文件 |
| **非目标函数** | 无影响 | 其他控制流完全不变 |

---

## 实现与验证步骤

1. ✅ 在 `AstBuilder.cs` 添加 `FoldReturnIf` 方法（~50 行）
2. ✅ `dotnet build` 零错误
3. ✅ 验证 `_is_dunder` / `_is_sunder` 输出 `return cond`
4. ✅ 批量回归 943/943
5. ✅ 更新基线报告
6. ✅ 提交 + 推送

## 代码位置

| 修改点 | 文件 | 行号 | 说明 |
|:-------|:-----|:-----|:-----|
| `FoldReturnIf` | `AstBuilder.cs` | 新增方法 | ~50 行 |
| 调用入口 | `AstBuilder.cs` | `PostProcessFunctionDefs` 末尾 | 遍历函数体 |

---

## 附录：OR 链问题说明（后续任务）

3.13+ OR 链 bytecode 结构：

```
LOAD_GLOBAL hasattr+NULL
LOAD_FAST_BORROW obj
LOAD_CONST '__get__'
CALL 2              # hasattr(obj, '__get__')
COPY 1              # duplicate for possible return
TO_BOOL             # convert to bool
POP_JUMP_IF_TRUE → L1 (shared RETURN_VALUE)
NOT_TAKEN           # pseudo-instruction
POP_TOP             # discard duplicate
LOAD_GLOBAL ...
...                 # second condition
POP_JUMP_IF_TRUE → L1
NOT_TAKEN
POP_TOP
LOAD_GLOBAL ...     # terminal: NO POP_JUMP_IF_TRUE
...                 # just CALL → L1
L1: RETURN_VALUE    # shared return point
```

**待解决问题**：
1. `NOT_TAKEN` 伪指令在 `MarkLeaders` 中产生不必要的 leaders
2. 终端条件块没有 `POP_JUMP_IF_TRUE`，`IsConditionBranch` 返回 false
3. 共享 `RETURN_VALUE` 块导致表达式栈跨块传播问题
4. `COPY 1 + POP_TOP` 的表达式匹配
