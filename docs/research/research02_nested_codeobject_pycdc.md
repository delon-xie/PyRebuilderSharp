# 研读记录②: pycdc 嵌套 CodeObject 递归反编译

> 来源: `pycdc/ASTree.cpp` (3826 行)
> 关键函数: `BuildFromCode()` 行 85, `MAKE_FUNCTION_A` 行 1649, `decompyle()` 行 3723
> 对应 PyRebuilderSharp: `AstBuilder.cs` — `DecompileNestedCodeObjects()` 方法

---

## 1. pycdc 的架构概览

### 1.1 单一函数驱动一切

pycdc 使用**单一函数** `BuildFromCode()` 处理所有代码对象——从模块到嵌套函数：

```cpp
// 入口: decompyle() (行 3723)
void decompyle(PycRef<PycCode> code, PycModule* mod, ostream& pyc_output) {
    // 循环引用检测 ← 关键安全机制
    if (code_seen.find((PycCode *)code) != code_seen.end()) {
        fputs("WARNING: Circular reference detected\n", stderr);
        return;
    }
    code_seen.insert((PycCode *)code);
    
    PycRef<ASTNode> source = BuildFromCode(code, mod);
    // ... 后处理 + 输出
}
```

### 1.2 MAKE_FUNCTION / MAKE_CLOSURE 的处理 (行 1649)

```cpp
case Pyc::MAKE_CLOSURE_A:
case Pyc::MAKE_FUNCTION_A:
{
    PycRef<ASTNode> fun_code = stack.top();
    stack.pop();

    // 取 qualified name (如果 TOS 不是 code object，再 pop 一次)
    int tos_type = fun_code.cast<ASTObject>()->object().type();
    if (tos_type != PycObject::TYPE_CODE && tos_type != PycObject::TYPE_CODE2) {
        fun_code = stack.top();
        stack.pop();
    }

    // 收集默认参数
    ASTFunction::defarg_t defArgs, kwDefArgs;
    const int defCount = operand & 0xFF;
    const int kwDefCount = (operand >> 8) & 0xFF;
    for (int i = 0; i < defCount; ++i) {
        defArgs.push_front(stack.top());
        stack.pop();
    }
    for (int i = 0; i < kwDefCount; ++i) {
        kwDefArgs.push_front(stack.top());
        stack.pop();
    }
    // 创建 ASTFunction 节点（不递归调用 BuildFromCode）
    stack.push(new ASTFunction(fun_code, defArgs, kwDefArgs));
}
```

**关键发现**：pycdc **不**在 MAKE_FUNCTION 处递归反编译子 code object。`fun_code` 被包裹在 `ASTFunction` 节点中，实际的函数体反编译**在代码生成阶段**（AST 遍历）完成。

### 1.3 代码生成阶段的递归（在 AST 遍历时）

在 `ASTree.cpp` 中没有直接看到——实际的递归发生在代码生成阶段。当 `ASTFunction` 被序列化时，它访问其内部的 `PycCode` 对象并调用 `BuildFromCode()` 来解析函数体。

## 2. 对比 PyRebuilderSharp 现状

| 方面 | pycdc | PyRebuilderSharp 现状 | 差距 |
|------|-------|----------------------|------|
| 嵌套处理时机 | 代码生成时递归（AST 遍历阶段） | `PostProcessFunctionDefs` + `ConvertChildCodesToFunctionDefs`（后处理阶段） | 类似，但 pycdc 是懒加载 |
| 循环引用保护 | `code_seen` unordered_set | 无 | 应添加 |
| 函数标识 | `ASTObject` 检查 code type | `FunctionRef` + `CodeObject.Name` | 已有 |
| 默认参数收集 | MAKE_FUNCTION 时从栈上 pop | `StackMachine` 已有 | ✅ 已实现 |
| 递归深度 | 无显式限制 | 需限制为 ≤10 | 需添加 |

## 3. 在 PyRebuilderSharp 中的应用

### 3.1 递归反编译设计

借鉴 pycdc 的"单一函数驱动一切"理念，在 `AstBuilder` 中新增：

```csharp
private HashSet<int> _processedCodeObjectIds = new();  // 对应 pycdc code_seen
private const int MaxNestedDepth = 10;

/// <summary>
/// 对应 pycdc 的 BuildFromCode()。
/// 为子 CodeObject 单独起 AstBuilder，递归反编译。
/// 
/// 不同于 pycdc（代码生成时递归），我们在 AST 构建阶段递归。
/// </summary>
private List<Stmt> DecompileNestedCodeObjects(List<Stmt> stmts, CodeObject parentCode)
{
    foreach (var stmt in stmts)
    {
        if (stmt is FunctionDef fd)
        {
            // 只在 FunctionDef.Body 为空或仅含 pass/Comment 时触发
            if (fd.Body.Count == 0 || fd.Body.All(s => s is CommentBlock or Pass))
            {
                var childCode = FindChildCodeObject(fd.Name, parentCode);
                if (childCode != null && !_processedCodeObjectIds.Contains(childCode.Id))
                {
                    _processedCodeObjectIds.Add(childCode.Id);
                    
                    // 递归: 用子 CodeObject 重新 Build()
                    var childAstBuilder = new AstBuilder(childCode, _options);
                    var childCfg = BuildCFG(childCode);  // 需要传入子 code 的 CFG
                    var childModule = childAstBuilder.Build(childCfg);
                    
                    if (childModule is Module m && m.Body.Count > 0)
                        fd = fd with { Body = m.Body };
                }
            }
            
            // 递归处理嵌套函数中的嵌套函数
            DecompileNestedCodeObjects(fd.Body, FindChildCodeObject(fd.Name, parentCode) ?? parentCode);
        }
    }
    return stmts;
}
```

### 3.2 循环引用保护

```csharp
// 对应 pycdc 的 code_seen unordered_set
private HashSet<int> _processedCodeIds = new();

// 在 Build() 入口处检查
if (!_processedCodeIds.Add(_codeObject.Id))
{
    Console.Error.WriteLine($"[WARN] Circular reference: {_codeObject.Name}");
    return new Module(new List<Stmt> { new CommentBlock("# Circular reference") }, _codeObject.Name);
}
```

### 3.3 递归深度保护

```csharp
// 对应 pycdc 的隐含限制（无显式限制，但有 potential stack overflow）
private int _recursionDepth = 0;

// 在递归前++
_recursionDepth++;
if (_recursionDepth > MaxNestedDepth)
{
    Console.Error.WriteLine($"[WARN] Max nested depth exceeded for {codeObject.Name}");
    _recursionDepth--;
    return /* fallback */;
}
// 构建完成后--
_recursionDepth--;
```

---

## 4. 关键发现

### 4.1 pycdc 与 PyRebuilderSharp 的嵌套处理时机不同

| pycdc | PyRebuilderSharp |
|-------|-----------------|
| `BuildFromCode()` 对所有 code object 都相同 | 顶层用 `Build()`, 子层用 `PostProcessFunctionDefs` |
| 函数体在代码生成阶段惰性递归 | 函数体在 AST 后处理阶段扁平匹配 |
| 无深度限制（依赖 C++ 栈） | 需要有显式深度限制 |

### 4.2 pycdc 的"单一入口"设计更简洁

`BuildFromCode()` 处理任何层级的 code object——模块、函数、lambda。这使得嵌套处理天然是递归的。PyRebuilderSharp 的 `Build()` 和 `PostProcessFunctionDefs()` 分离增加了复杂度。

**改进方向**：让 `AstBuilder.Build()` 接受可选的 `CodeObject` 参数，使它能处理任意层级的 code object，而不只是顶层模块。

### 4.3 循环引用保护 === 代码对象去重

pycdc 的 `code_seen` 既是循环引用保护，也是**去重机制**（同一个 code object 不会重复处理）。PyRebuilderSharp 的 `ConvertChildCodesToFunctionDefs` 没有去重，可能重复处理同一个 code object。

---

> **研读日期**: 2026-07-10
> **服务于**: Step 5 (嵌套 CodeObject 递归 + ET 严格映射)
