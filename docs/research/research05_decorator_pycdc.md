# 研读记录⑤: pycdc Decorator 检测 (MAKE_FUNCTION + CALL_FUNCTION)

> 来源: `pycdc/ASTree.cpp` 行 439~537 (CALL_FUNCTION), 行 1649~1675 (MAKE_FUNCTION)
> 对应 PyRebuilderSharp: `AstBuilder.FoldDecoratorCalls()` 方法

---

## 1. pycdc 的 Decorator 检测算法

### 1.1 检测时机：CALL_FUNCTION 指令

pycdc 在 `CALL_FUNCTION` 指令处理时检测 decorator，而非单独的 pass：

```cpp
case Pyc::CALL_FUNCTION_A:
{
    // ... 解析参数 ...
    
    for (int i=0; i<pparams; i++) {
        PycRef<ASTNode> param = stack.top();
        stack.pop();
        if (param.type() == ASTNode::NODE_FUNCTION) {
            // ← 参数是函数定义 → 可能是 decorator
            PycRef<ASTNode> fun_code = param.cast<ASTFunction>()->code();
            PycRef<PycCode> code_src = fun_code.cast<ASTObject>()->object().cast<PycCode>();
            PycRef<PycString> function_name = code_src->name();
            if (function_name->isEqual("<lambda>")) {
                // lambda 参数 → 不是 decorator，作为普通参数
                pparamList.push_front(param);
            } else {
                // ★ 非 lambda 函数传入 → 是 decorator！
                // 生成: @decorator_name
                //        def func(): ...
                PycRef<ASTNode> decor_name = new ASTName(function_name);
                curblock->append(new ASTStore(param, decor_name));
                pparamList.push_front(decor_name);
            }
        } else {
            pparamList.push_front(param);
        }
    }
    // ... 创建 ASTCall ...
}
```

### 1.2 检测条件

| 条件 | 判定 | 处理 |
|------|------|------|
| 参数是 `NODE_FUNCTION` 且 name 是 `<lambda>` | ❌ 不是 decorator（是 lambda 参数） | 作为普通参数 |
| 参数是 `NODE_FUNCTION` 且 name 不是 `<lambda>` | ✅ 是 decorator | 存储为 `ASTStore` + 替换为 `ASTName` |
| 参数不是 `NODE_FUNCTION` | ❌ 不是 decorator | 作为普通参数 |

### 1.3 输出模式

```python
# pycdc 对 @decorator 的输出:
def decorator(func):
    ...

@decorator                # ← 这是由 ASTStore + ASTName 生成的
def target():
    ...
```

pycdc 不尝试还原多层 decorator 的嵌套顺序——它直接把 decorator 展开为裸赋值 + 引用。

## 2. 对比 PyRebuilderSharp

| 方面 | pycdc | PyRebuilderSharp |
|------|-------|-----------------|
| 检测时机 | CALL_FUNCTION 指令处理时 | 后处理 `FoldDecoratorCalls` |
| 识别依据 | 参数类型是 NODE_FUNCTION | `FunctionRef` + 调用模式匹配 |
| 多层 decorator | 展开为多个 ASTStore | `FoldDecoratorCalls` 从后向前匹配 |
| lambda 区分 | 检查 name 是否为 `<lambda>` | 通过 `FunctionRef.Name` 检查 |

### 2.1 pycdc 的优势

- **在指令处理时检测**，不需要后处理 pass
- 不需要启发式——栈上已经有了 `ASTFunction` 节点，直接检查

### 2.2 PyRebuilderSharp 的优势

- **StackMachine 已经吃下了 MAKE_FUNCTION**，后处理可以更灵活地折叠
- 对于多层装饰器（`@A @B @C`），后处理更容易从最内层向外折叠

## 3. 在 PyRebuilderSharp 中的应用

### 3.1 FoldDecoratorCalls 算法

```csharp
/// <summary>
/// 将 ExprStmt(Call(func, FunctionDef)) 模式折叠为 FunctionDef.Decorators。
/// 
/// 对应 pycdc 的 CALL_FUNCTION 检测，但在后处理阶段执行。
/// 
/// 算法（从后向前贪婪匹配）：
/// 1. 扫描 stmts 中的 ExprStmt(Call { Args: [FunctionDef] })
/// 2. 检查 Call.Func 是否为装饰器名称（不是 <lambda>）
/// 3. 将 Call.Func 加入 FunctionDef.Decorators
/// 4. 删除 ExprStmt
/// 5. 继续向前匹配更多装饰器（@A @B @C 链）
/// </summary>
private List<Stmt> FoldDecoratorCalls(List<Stmt> stmts)
{
    var result = new List<Stmt>(stmts.Count);
    int i = 0;
    while (i < stmts.Count)
    {
        if (stmts[i] is ExprStmt { Value: Call call })
        {
            // 检测模式: decorator(defn) 或 decorator_A(decorator_B(defn))
            if (TryExtractDecoratedFunction(call, out var funcDef, out var decorators))
            {
                // 找到装饰器链，生成带有 Decorators 的 FunctionDef
                result.Add(funcDef with { Decorators = decorators });
                i++;
                continue;
            }
        }
        result.Add(stmts[i]);
        i++;
    }
    return result;
}

/// <summary>
/// 尝试从 Call 表达式中提取装饰器+函数定义。
/// 递归解析 @A @B @C 链。
/// </summary>
private bool TryExtractDecoratedFunction(
    Call call, out FunctionDef funcDef, out List<Expr> decorators)
{
    decorators = new List<Expr>();
    
    // 基本情况: Call(func, [FunctionDef])
    if (call.Args.Count == 1 && call.Args[0] is FunctionDef fd)
    {
        if (call.Func is Name decoratorName && decoratorName.Id != "<lambda>")
        {
            funcDef = fd;
            decorators.Add(new Name(decoratorName.Id, ExpressionContext.Load));
            return true;
        }
        // 也处理 Attribute（如 @module.decorator）
        if (call.Func is Attribute attr)
        {
            funcDef = fd;
            decorators.Add(attr);
            return true;
        }
    }
    
    // 递归情况: Call(func, [Call(func2, [FunctionDef])])
    // @A @B == Call(A, [Call(B, [FunctionDef])])
    if (call.Args.Count == 1 && call.Args[0] is Call innerCall)
    {
        if (TryExtractDecoratedFunction(innerCall, out funcDef, out var innerDecorators))
        {
            decorators.AddRange(innerDecorators);
            if (call.Func is Name decoratorName && decoratorName.Id != "<lambda>")
            {
                decorators.Insert(0, new Name(decoratorName.Id, ExpressionContext.Load));
                return true;
            }
        }
    }
    
    funcDef = null!;
    return false;
}
```

---

> **研读日期**: 2026-07-10
> **服务于**: Step 3 (表达式折叠 — `FoldDecoratorCalls` pass)
