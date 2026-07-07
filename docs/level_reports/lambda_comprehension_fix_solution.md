# Lambda in Comprehension 修复方案

## 问题描述

`l6_15_lambda_in_comprehension` 的源代码如下：

```python
def l6_15_lambda_in_comprehension():
    funcs = [lambda x, i=i: x + i for i in range(5)]
    return [f(1) for f in funcs]
```

当前输出：

```python
def l6_15_lambda_in_comprehension():
    funcs = [lambda: None for i in range(5)]
    return [iterable for f in funcs]
```

两个子问题：

1. **lambda 完全崩坏**: `lambda x, i=i: x + i` → `lambda: None`
   - Args 丢失（应该为 `x, i=i`）
   - Body 丢失（应该为 `x + i`）
   - Default 丢失

2. **第二个推导式错乱**: `[f(1) for f in funcs]` → `[iterable for f in funcs]`
   - 元素 `f(1)` → `iterable`（回退名）
   - 迭代器 `funcs` → `iterable`（回退名）

---

## 根因分析

### 子问题 1：lambda 崩坏

**字节码结构**：`[lambda x, i=i: x + i for i in range(5)]` 编译为：

```
外层函数 `<listcomp>`:
  LOAD_FAST .0  (iterable = range(5))
  FOR_ITER → exit
  STORE_FAST i   (loop variable)
  LOAD_CLOSURE i (cell variable for inner lambda)
  BUILD_TUPLE 1
  LOAD_CONST <code object '<lambda>'>
  LOAD_CONST '<lambda>'
  MAKE_FUNCTION <defaults>
  CALL_FUNCTION 0
  LIST_APPEND
  JUMP_ABSOLUTE

内层 `<lambda>`:
  LOAD_FAST .0 → MAKE_CELL → cell for .0 (the default `i`)
  LOAD_FAST x (arg)
  LOAD_DEREF i (cell var from .0)
  BINARY_ADD → x + i
  RETURN_VALUE
```

**`BuildLambda` 在 380951 行**的流程：

1. 参数提取：`childCode.ArgCount` → 仅提取 `.0` 之前的 args。但 lambda 参数 `x, i=i` 以特殊方式存储
2. 体反编译：`DecompileChildCode(childCode)` 返回空列表 `[]`
3. 返回 `new Lambda(args, new Constant(null))` = `lambda _: None`

**空体的根因**：lambda 的子代码结构为「单块 + RETURN_VALUE」。`DecompileChildCode` → `Build` 处理单块时，`BlockDecompiler` 将 `RETURN_VALUE` 处理为 `Return(BinOp(x, Add, ...))`。但该 `Return` 可能在 `BuildForLoop` 或 `PostProcessFunctionDefs` 中被消费。

更具体的断裂点：
- `STORE_FAST x`（参数赋值）在单块中被 `ExtractLoopTarget` 消费
- `LOAD_FAST .0`（MAKE_CELL 前导）让 BlockScanner 认为有循环结构
- Block 分割后，`return` 语句丢失

### 子问题 2：第二个推导式错乱

`[f(1) for f in funcs]` 的 `<listcomp>` 子代码：

```
LOAD_FAST .0 (funcs)
FOR_ITER → exit
STORE_FAST f
LOAD_FAST f
LOAD_CONST 1
CALL_FUNCTION 1 → Call(Name('f'), [Constant(1)])
LIST_APPEND
JUMP_ABSOLUTE
```

**断裂路径**：该推导式通过 `BuildComprehension` → For-loop 路径处理。
- `TryDetectInlinedComprehension` 检测到 LIST_APPEND，提取 elt = `Call(Name('f'), [Constant(1)])`
- 但 elt 提取后，`BuildComprehensionFallback` 未正确处理该复杂的 Call 表达式
- `.0` → `compCall.Args[0]` 替换失败，iterable 回退为 `Name("iterable")`

---

## 修复方案

### 方案 A：修复 `BuildLambda` 的空体问题（子问题 1）

**修改 `BuildLambda`**：

```csharp
// 当返回体为空时，尝试从原始子代码指令模拟提取
if (body.Count == 0)
{
    // 模拟执行指令提取 RETURN_VALUE 前的表达式
    var simExpr = SimulateLambdaReturn(childCode.Instructions);
    if (simExpr != null)
        return new Lambda(args, simExpr);
    // 原有回退
    if (args.Count == 0)
        args.Add(new Parameter("_"));
    return new Lambda(args, new Constant(null));
}
```

**新增 `SimulateLambdaReturn`**：
- 找到 `RETURN_VALUE` 指令
- 之前向模拟 StackMachine：定位 `LOAD_FAST` 和 `LOAD_DEREF` 的参数
- 计算返回表达式

**参数提取修正**：
- `ArgCount` 之后可能有 `.0`（MAKE_CELL 的前导参数）
- Defaults 从 `funcRef.Defaults` 或 `funcRef.Code.Consts` 提取

### 方案 B：修复 `BuildComprehensionFallback` 的 elt/iter 提取（子问题 2）

`BuildComprehensionFallback` 中，当从内层 `ListComp` 提取元素时：

```csharp
if (a.Value is ListComp lc)
{
    elt = lc.Elt;  // 对于 Call(f, [1])，lc.Elt 应该是完整的 Call 表达式
    target = lc.Generators[0].Target;
    iter = compCall.Args.Count > 0 ? compCall.Args[0] : null;  // 始终使用外层参数
    ifs = new List<Expr>(lc.Generators[0].Ifs);
}
```

**关键变更**：`iter` 应始终从 `compCall.Args[0]` 设置，不从内层 ListComp 读取。

### 方案 C：在处理 lambda 的 `ConvertComprehensionExpr` 中优先 `BuildLambda`

在 `ConvertComprehensionExpr` 的 lambda 回退路径中：

```csharp
if (compRef.Name == "<lambda>")
{
    var lambda = BuildLambda(compRef);
    if (lambda != null)
    {
        var newArgs = call.Args.Select(a => ConvertComprehensionExpr(a)).ToList();
        return new Call(lambda, newArgs, newKeywords);
    }
}
```

当前代码已存在该路径，问题在于 `BuildLambda` 返回了 `lambda: None`。

---

## 实现计划

| 步骤 | 任务 | 文件 | 行数 |
|:----:|:-----|:-----|:----:|
| 1 | 分析 lambda 子代码的 Displus 确认结构 | — | — |
| 2 | 修复 `BuildLambda` 的 args 提取（含 defaults） | AstBuilder.cs | +10 |
| 3 | 新增 `SimulateLambdaReturn` 方法 | AstBuilder.cs | +25 |
| 4 | 修复 `BuildComprehensionFallback` 的 iter 提取 | AstBuilder.cs | +3 |
| 5 | `dotnet build` + Level 6 测试 | — | — |

---

## 可能的风险

1. **回归**：`BuildLambda` 修改可能影响普通 lambda（非推导式）
2. **Defaults 提取**：`MAKE_FUNCTION` 的 defaults 可能以 `Tuple` 或 `Constant(None)` 形式存储
3. **Cell 变量名**：`LOAD_DEREF` 使用的 cell 变量名可能为 `i` 而非 `.0`

## 验证方法

1. `dotnet build -c Release` 无错误
2. `python3 tools/test_by_level.py 6` 的 l6_15 输出正确
3. 检查 l6_1/2/3/4 无回归
