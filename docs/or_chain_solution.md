# OR 链修复方案（AstBuilder CFG 扫描法）

> 问题：3.13+ `return A or B or C` 的 bytecode 使用 COPY/TO_BOOL/POP_JUMP_IF_TRUE/POP_TOP/共享 RETURN_VALUE
> 模式，现有 BlockScanner + BuildIfElse 无法正确处理。

## 根因

3.13+ OR 链 bytecode：

```
LOAD_FAST a
COPY 1              ← 为可能的 return 复制
TO_BOOL             ← 转 bool
POP_JUMP_IF_TRUE → L1  ← a 为 True 时跳转到共享 RETURN_VALUE
POP_TOP             ← a 为 False：丢弃复制值
LOAD_FAST b         ← 第二个条件
COPY 1
TO_BOOL
POP_JUMP_IF_TRUE → L1
POP_TOP
LOAD_FAST c         ← 终端条件：无 POP_JUMP！
L1: RETURN_VALUE    ← 共享返回点
```

三个问题：

1. **POP_JUMP_IF_TRUE 后跟 POP_TOP**：POP_TOP 产生新的块 leader，分裂 fallthrough 链
2. **终端块无 POP_JUMP**：`LOAD_FAST c` 是最后条件，不含条件跳转 → `IsConditionBranch` = false
3. **共享 RETURN_VALUE**：L1 块有独立 StackMachine，空栈 → `Return(null)`

## 方案：AstBuilder CFG 扫描替换

不修改 BlockScanner/StackMachine，在已有 AST 输出上做模式匹配。

### 步骤 1：检测 OR 链签名

在 `PostProcessFunctionDefs`（或新增 `PostProcessControlFlow`）中扫描函数体的 statement 列表。

**OR 链签名**：
```
[If(cond1, [], null), ..., If(condN, [], null), Return(lastExpr), ...]
```
- 连续多个 `If(cond, [], null)`（空 body，render 为 `pass`）
- 紧随一个 `Return(expr)`（终端表达式）
- 没有 else 分支

**AND 链签名**：
```
[If(cond1, [Return(expr1)], null), If(cond2, [Return(expr2)], null), ..., Return(lastExpr)]
```
- 目前已被 FoldReturnIf 部分处理

### 步骤 2：跨版本兼容

- **3.13+**：模式如上（COPY/TO_BOOL/POP_JUMP_IF_TRUE/POP_TOP）
- **3.12-**：使用旧版 POP_JUMP_IF_TRUE（无 COPY/TO_BOOL/POP_TOP），但结构类似

两种模式都产生 `[If(cond, [], null), ..., Return(last)]`。

### 步骤 3：合并为 BoolOp

检测到 OR 链后：
```
- If(cond1, [], null)       → 移除
- If(cond2, [], null)       → 移除
- Return(last)              → Return(BoolOp(Or, [cond1, cond2, last]))
```

同样处理 AND 链：
```
- If(cond1, [Return(expr1)], null)
- If(cond2, [Return(expr2)], null)
- ...
- Return(last)
```

## 影响范围

| 函数 | 版本 | 当前输出 | 修复后 |
|:-----|:-----|:---------|:-------|
| `_is_descriptor` | 3.13-3.14 | `if A: pass; return C` | `return A or B or C` |
| `_is_dunder` | 3.13-3.14 | 已正确（FoldReturnIf） | — |
| reprlib/abc/etc. | 3.13-3.14 | OR 链类似问题 | 修复 |

## 实现

在 `AstBuilder.cs` 中新增 `RebuildOrChain` 方法，在 `PostProcessFunctionDefs` 末尾调用：

```csharp
private List<Stmt> RebuildOrChain(List<Stmt> stmts)
{
    for (int i = 0; i < stmts.Count - 1; i++)
    {
        // 收集连续的空-boday if 链
        var ifChain = new List<(If ifStmt, int idx)>();
        int j = i;
        while (j < stmts.Count && stmts[j] is If ifNode
               && ifNode.Orelse == null
               && ifNode.Body.Count == 0)  // empty body = pass
        {
            ifChain.Add((ifNode, j));
            j++;
        }
        
        if (ifChain.Count >= 2 && j < stmts.Count && stmts[j] is Return retStmt)
        {
            // OR chain detected: cond1, cond2, ..., return last
            var conditions = ifChain.Select(ic => ic.ifStmt.Test).ToList();
            conditions.Add(retStmt.Value ?? new Constant(true));
            
            // Remove all if-statements, replace return with BoolOp
            foreach (var (_, idx) in ifChain.Reverse<...>())
                stmts.RemoveAt(idx);
            
            stmts[i] = new Return(new BoolOp(BoolOperator.Or, conditions));
        }
    }
    return stmts;
}
```
