# 研读记录④: uncompyle6 推导式/LIST_APPEND 处理

> 来源: `python-uncompyle6/uncompyle6/parsers/parse37.py` (行 725), `parse27.py` (行 29)
> 对应 PyRebuilderSharp: `AstBuilder.ConvertComprehensionCalls()` + BARE_EXPR 清理

---

## 1. uncompyle6 的推导式语法规则

### 1.1 核心规则

```python
# parse37.py:
lc_body   ::= expr LIST_APPEND                # list comprehension body
dict_comp_body ::= expr expr MAP_ADD           # dict comprehension body
genexpr_func ::= LOAD_ARG _come_froms FOR_ITER store comp_iter JUMP_BACK

# parse27.py:
lc_body ::= LOAD_NAME expr LIST_APPEND         # Python 2.7 版本（需 LOAD_NAME）
lc_body ::= LOAD_FAST expr LIST_APPEND         # Python 2.7 版本（局部变量版本）
```

**核心原则**：`LIST_APPEND` 指令**不能单独出现**——它必须跟在 `expr`（要添加的值）后面。语法规则将两者合为一个节点 `lc_body`，使其在 AST 中不产生独立的表达式语句。

### 1.2 推导式整体结构

```python
# 3.7+ 语法 (parse37.py):
list_comp ::= BUILD_LIST_0 load_listcomp expr COME_FROM_LOOP lc_body JUMP_LOOP

# 其中：
# BUILD_LIST_0     — 创建空列表
# load_listcomp    — 加载 listcomp 代码对象
# expr             — 迭代器表达式 (for ... in ...)
# COME_FROM_LOOP   — 循环入口标记
# lc_body          — 列表推导式 body: expr LIST_APPEND
# JUMP_LOOP        — 循环跳转
```

## 2. 与 PyRebuilderSharp 对比

### 2.1 现状分析

| 方面 | uncompyle6 | PyRebuilderSharp |
|------|-----------|-----------------|
| 推导式节点 | 语法规则直接生成 `list_comp` | `ConvertComprehensionCalls` 后处理转换 |
| LIST_APPEND 处理 | 语法规则消费，不作为独立语句 | 被 StackMachine 吃下但可能残留 |
| for-iter 变量 | 语法规则中的 `store` 节点消费 | StackMachine 消费但 for-else 歧义 |
| 变量名匹配 | 通过 `comp_iter` 规则链管理 | `IsInComprehensionContext` 启发式 |

### 2.2 关键差距

uncompyle6 的语法规则能在**解析阶段**就确定 LIST_APPEND 属于推导式。PyRebuilderSharp 的标注+模式目录在 Phase 5 才链接结构，此时 LIST_APPEND 指令已经被 StackMachine 转换了。

**实际难题**：PyRebuilderSharp 的 `ConvertComprehensionCalls` 已经生成了 `ListComp` AST 节点，但原始的 `.append()` 调用有时作为 `ExprStmt` 残留。这类似于生成 `ListComp` 后，编译器的 LIST_APPEND 循环体变成了"幽灵代码"。

## 3. 应用：BARE_EXPR 清理规则

### 3.1 安全的清理模式

**基于 uncompyle6 的语法规则，以下模式可以安全删除**：

```csharp
// B1: expr LIST_APPEND → 在 ListComp 上下文中可删除
// 条件：ExprStmt 的 .append() 调用与前面已生成的 ListComp 共享目标变量
if (stmt is ExprStmt { Value: Call { Func: Attribute { Attr: "append" } } } call
    && IsInComprehensionContext(stmt, siblings))
{
    continue; // 删除
}

// B2: expr expr MAP_ADD → 在 DictComp 上下文中可删除
if (stmt is ExprStmt { Value: Call { Func: Attribute { Attr: "__setitem__" } } } 
    && IsInComprehensionContext(stmt, siblings))
{
    continue;
}
```

### 3.2 安全检测（IsInComprehensionContext）

```csharp
/// <summary>
/// 检测 ExprStmt 是否在推导式上下文中。
/// 
/// 对应 uncompyle6 的规则匹配策略，但用启发式替代：
/// 1. 查找前面存在的 ListComp/SetComp/DictComp 节点
/// 2. 对比 .append() 的目标变量名与 ListComp 的赋值目标
/// 3. 如果匹配且两者在同级语句列表中 → 可删除
/// 
/// 例如:
///   result = [x for x in range(10)]    ← ListComp AST
///   result.append(x)                    ← BARE_EXPR（与上面对应）
///   
/// 这里 result 是共同变量 → 可安全删除 append
/// </summary>
private bool IsInComprehensionContext(Stmt stmt, List<Stmt> siblings)
{
    if (stmt is ExprStmt { Value: Call { Func: Attribute { Attr: "append" } } } call)
    {
        // 获取 .append() 的目标变量名
        var target = GetCallTargetName(call.Value);
        if (target == null) return false;
        
        // 在同级语句中查找前面的赋值目标为 target 的推导式
        int idx = siblings.IndexOf(stmt);
        for (int i = Math.Max(0, idx - 5); i < idx; i++)
        {
            if (siblings[i] is Assign { Targets: [Name n], Value: ListComp or SetComp or DictComp }
                && n.Id == target)
            {
                return true; // 推导式已存在，.append() 是残留
            }
        }
    }
    return false;
}
```

### 3.3 for-else 歧义的解决

uncompyle6 通过 `FOR_ITER store comp_iter` 规则链确保 for-else 的迭代变量正确消费。PyRebuilderSharp 中 BARE_EXPR `x` 的问题（test_comp 等）实际上是 for-else 的迭代变量在转换后残留。

**解决方案**：当发现 `x`（用于 FOR_ITER 的迭代变量名）作为 BARE_EXPR 出现在 for-else 循环之前，且后面的语句是 `for x in ...` → 可以删除 `x`。

```csharp
// test_comp 的 BARE_EXPR 清理:
//   x              ← 这个 x 是 for x in range(10) 的 iter 变量泄漏
//   for x in range(10):
//       pass
// 
// 检测: 如果 ExprStmt(Name "x") 后面紧跟 For(Target=Name "x") → 删除
if (stmt is ExprStmt { Value: Name n }
    && HasFollowingForLoopWithSameVar(n.Id, siblings, idx))
{
    continue;
}
```

---

> **研读日期**: 2026-07-10
> **服务于**: Step 3 (BARE_EXPR 清理 — 规则 B1/B2/B3)
