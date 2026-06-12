
# 文档二：Python反编译详细设计.md

## Python字节码反编译器详细设计

**版本**: v2.1
**日期**: 2026-06-13
**项目**: PyRebuilderSharp
**状态**: 开发阶段 — Lv0 ✅ · Lv1 ✅ · Lv2 ✅ · Lv3 ✅ (42/42 版本矩阵测试通过)

---

## 1. 解决方案结构（实际项目）

```
PyRebuilderSharp.slnx
├── Directory.Build.props           # 全局构建属性
├── src/
│   ├── PyRebuilderSharp.Core/      # 核心库 (net10.0)
│   │   ├── Builders/               # AST 构建
│   │   ├── Generators/             # 代码生成
│   │   ├── Models/                 # 数据模型
│   │   ├── Readers/                # 读取器
│   │   ├── Scanners/               # 扫描器
│   │   ├── Testing/                # 测试框架
│   │   └── Decompiler.cs           # 主入口
│   ├── PyRebuilderSharp.Cli/       # 命令行
│   └── PyRebuilderSharp.Gui/       # Avalonia GUI
└── tests/
    └── PyRebuilderSharp.Tests/
```

---

## 2. 核心数据模型（实际实现）

### 2.1 字节码模型

```csharp
// Models/Bytecode/Instruction.cs
public readonly record struct Instruction(
    int Offset,
    Opcode Opcode,
    int? Argument = null
);

// Models/Bytecode/Opcode.cs
public enum Opcode : byte
{
    POP_TOP = 1,
    ROT_TWO = 2,
    ...
    BINARY_ADD = 23,
    BINARY_SUBTRACT = 24,
    BINARY_MULTIPLY = 20,
    ...
    COMPARE_OP = 107,
    JUMP_FORWARD = 110,
    JUMP_ABSOLUTE = 113,
    POP_JUMP_IF_TRUE = 114,
    POP_JUMP_IF_FALSE = 115,
    POP_JUMP_IF_TRUE_PY38 = 117,  // Python 3.8+ 重编号
    POP_JUMP_IF_FALSE_PY38 = 118,
    GET_ITER = 68,
    FOR_ITER = 93,
    SETUP_FINALLY = 122,
    POP_EXCEPT = 89,
    ...
}
```

### 2.2 AST 模型

```csharp
// 表达式节点
public abstract record Expr : AstNode;
public record Constant(object? Value) : Expr;
public record Name(string Id, ExpressionContext Ctx = ExpressionContext.Load) : Expr;
public record BinOp(Expr Left, Operator Op, Expr Right) : Expr;
public record UnaryOp(UnaryOperator Op, Expr Operand) : Expr;
public record Compare(Expr Left, List<CmpOp> Ops, List<Expr> Comparators) : Expr;
public record Call(Expr Func, List<Expr> Args, List<Keyword> Keywords) : Expr;
public record Attribute(Expr Value, string Attr, ExpressionContext Ctx) : Expr;

// 语句节点
public abstract record Stmt : AstNode;
public record Pass() : Stmt;
public record Break() : Stmt;
public record Continue() : Stmt;
public record ExprStmt(Expr Value) : Stmt;
public record Assign(List<Expr> Targets, Expr Value) : Stmt;
public record AugAssign(Expr Target, Operator Op, Expr Value) : Stmt;
public record Return(Expr? Value) : Stmt;
public record If(Expr Test, List<Stmt> Body, List<Stmt>? Orelse = null) : Stmt;
public record While(Expr Test, List<Stmt> Body, List<Stmt>? Orelse = null) : Stmt;
public record For(Expr Target, Expr Iter, List<Stmt> Body, List<Stmt>? Orelse = null) : Stmt;
public record Try(List<Stmt> Body, List<ExceptHandler> Handlers,
    List<Stmt>? Orelse = null, List<Stmt>? Finalbody = null) : Stmt;
public record ExceptHandler(Expr? Type, string? Name, List<Stmt> Body) : Stmt;
public record CommentStmt(string CommentText) : Stmt;  // ← 注释兜底专用
```

**CommentStmt** — 这是逐块兜底策略的关键。当某个基本块反编译失败时：
1. `BlockDecompiler` 捕获异常，调用 `BlockResult.FallbackAsComment()`
2. `AstBuilder` 使用 `CommentStmt(commentText)` 节点代替失败块
3. `PythonCodeGenerator` 输出为 `# ...` 注释行，格式与代码一致

---

## 3. 逐块反编译引擎（BlockDecompiler）

### 3.1 BlockResult — 成功/失败统一返回

```csharp
public class BlockResult
{
    public bool IsSuccess { get; init; }
    public List<Stmt> Statements { get; init; } = new();
    public string CommentFallback { get; init; } = "";
    public string? ErrorMessage { get; init; }

    public static BlockResult Success(List<Stmt> stmts);
    public static BlockResult FallbackAsComment(
        List<Instruction> instructions, Exception exception, int blockId);
}
```

**FallbackAsComment 输出格式**：
```
# ════════════════════════════════════════
# [Block #{id} Decompilation Failed]
# Offsets: 0x{start:X4} - 0x{end:X4}
# Engine: StackMachine
# Error: {exception.Message}
# Raw bytes: {hex bytes}
# ════════════════════════════════════════
```

### 3.2 BlockDecompiler 完整流程

```csharp
/// <summary>
/// 反编译单个基本块
/// </summary>
public BlockResult DecompileBlock(
    List<Instruction> instructions,
    CodeObject codeObject,
    int blockId,
    HashSet<int> loopHeaderOffsets = null,
    bool isForLoop = false)
{
    try
    {
        // 1. 创建 StackMachine 实例
        var stackMachine = new StackMachine(codeObject);

        // 2. 设置循环上下文（break/continue 支持）
        stackMachine.SetIsForLoop(isForLoop);
        if (loopHeaderOffsets?.Count > 0)
            stackMachine.SetLoopHeaders(loopHeaderOffsets);

        // 3. 逐指令执行
        var stmts = new List<Stmt>();
        foreach (var instr in instructions)
        {
            var result = stackMachine.Execute(instr);
            if (result is Stmt stmt) stmts.Add(stmt);
        }

        // 4. 处理栈剩余表达式
        while (stackMachine.HasResults)
            stmts.Add(new ExprStmt(stackMachine.PopResult()));

        // 5. 死代码消除
        stmts = EliminateDeadCode(stmts);

        return BlockResult.Success(stmts);
    }
    catch (Exception ex)
    {
        // ❗ 核心：捕获异常→注释兜底
        return BlockResult.FallbackAsComment(instructions, ex, blockId);
    }
}
```

---

## 4. StackMachine 栈机模拟

### 4.1 指令处理对照表

| 指令 | 栈操作 | AST 输出 |
|------|--------|---------|
| `LOAD_CONST i` | push `Constant(code.Constants[i])` | — |
| `LOAD_NAME i` | push `Name(code.Names[i])` | — |
| `LOAD_FAST i` | push `Name(code.Varnames[i])` | — |
| `LOAD_ATTR i` | pop `obj`, push `Attribute(obj, code.Names[i])` | — |
| `STORE_NAME i` | pop `v` | `Assign([Name(n)], v)` |
| `STORE_FAST i` | pop `v` | `Assign([Name(v)], v)` |
| `STORE_ATTR i` | pop `v, obj` | `Assign([Attribute(obj, n)], v)` |
| `BINARY_ADD` | pop `r,l` push `BinOp(l, Add, r)` | — |
| `BINARY_SUBTRACT` | pop `r,l` push `BinOp(l, Sub, r)` | — |
| `BINARY_MULTIPLY` | pop `r,l` push `BinOp(l, Mul, r)` | — |
| `BINARY_DIVIDE(2.7)` | pop `r,l` push `BinOp(l, Div, r)` | — |
| `COMPARE_OP i` | pop `r,l` push `Compare(l, [cmp], [r])` | — |
| `UNARY_NEGATIVE` | pop `v` push `UnaryOp(USub, v)` | — |
| `UNARY_NOT` | pop `v` push `UnaryOp(Not, v)` | — |
| `CALL_FUNCTION n` | pop `args[n]..args[0], func` push `Call(func, args)` | — |
| `RETURN_VALUE` | pop `v` | `Return(v)` |
| `POP_TOP` | pop `v` (丢弃); for 体中→`Break()` | — / `Break()` |
| `JUMP_ABSOLUTE→循环头` | — | `Continue()` |
| `GET_ITER` | pop `v` push `v` (标记) | — |
| `YIELD_VALUE` | pop `v` | `Yield(v)` |
| `BUILD_TUPLE n` | pop `n` items push `Tuple(items)` | — |
| `BUILD_LIST n` | pop `n` items push `List(items)` | — |
| `BUILD_MAP n` | push `Dict([])` 或 pop k,v push `Dict(...)` | — |

### 4.2 break/continue 识别

```
break 识别 (for 循环体):
  FOR_ITER → 循环体 block
  POP_TOP 在 for loop body 中 → Break()

continue 识别:
  JUMP_ABSOLUTE → _loopHeaderOffsets.Contains(target) → Continue()
```

### 4.3 2.7 版本差异

```
Python 2.7 操作码：
  STOP_CODE = 0,  DELETE_SLICE = 23,
  BINARY_DIVIDE = 21,  INPLACE_DIVIDE = 29,
  SLICE_0 = 39, SLICE_1 = 40, SLICE_2 = 41, SLICE_3 = 42,
  BUILD_SLICE = 133  (3.x 相同但操作数不同)

2.7 除法特殊处理：BINARY_DIVIDE(21) → BinOp(FloorDiv)
                          BINARY_TRUE_DIVIDE  → BinOp(Div)
```

---

## 5. AstBuilder — 控制结构构建

### 5.1 控制结构识别算法

```
GetStructuredBlockStmts(block, visited):
  1. if visited.Contains(block) → return []
  2. visited.Add(block)
  3. if block.Flags.HasFlag(LoopHeader) → BuildLoop(block, visited)
  4. if IsConditionBranch(block) → BuildRestrictedIfElse(block, visited)
  5. if BuildTryFromBlock(block) != null → return tryResult
  6. else → GetBlockStmts(block)  (平坦语句)
```

### 5.2 循环构建（BuildLoop → BuildWhileLoop / BuildForLoop）

```
BuildWhileLoop(header, visited):
  1. ExtractCondition(header) → testExpr
  2. CollectBodyBlocks(bodyEntry, header, bodyBlocks, visited)
  3. 将 bodyBlocks 从 visited 中移除   ← 关键：防止嵌套 StackOverflow
  4. foreach bodyBlock:
       GetStructuredBlockStmts(bodyBlock, visited)  ← 同一 visited
  5. return While(testExpr, bodyStmts, null)

BuildForLoop(header, visited):
  1. ExtractIterExpression(header) → iterExpr
  2. CollectBodyBlocks(bodyEntry, header, bodyBlocks, visited)
  3. 将 bodyBlocks 从 visited 中移除
  4. foreach bodyBlock:
       GetStructuredBlockStmts(bodyBlock, visited)
  5. ExtractLoopVariable(header, bodyBlocks) → target
  6. return For(target, iterExpr, bodyStmts, null)
```

### 5.3 嵌套循环 StackOverflow 修复（关键变更）

**问题**：原有的独立 `bodyVisited` 导致嵌套循环时，
内层循环的 body 块不在外层 bodyVisited 中，
外层循环的迭代处理到这些块时再次进入 GetStructuredBlockStmts，
形成无限递归。

**修复**：
```csharp
// 旧代码（有 Bug）
var bodyVisited = new HashSet<BasicBlock>();
foreach (var bodyBlock in bodyBlocks)
    var stmts = GetStructuredBlockStmts(bodyBlock, bodyVisited);  // ✗ 空集合

// 新代码（正确的）
foreach (var bb in bodyBlocks)
    visited.Remove(bb);  // 先从 visited 移除，让 GetStructuredBlockStmts 重新管理
foreach (var bodyBlock in bodyBlocks)
    var stmts = GetStructuredBlockStmts(bodyBlock, visited);  // ✓ 同一 visited
```

**原理**：`CollectBodyBlocks` 把所有 body 块都标记在 `visited` 中，
直接调用 `GetStructuredBlockStmts` 会由于 `visited.Contains(block)` 而跳过。
先把 body 块从 `visited` 移除，再逐个用同一个 `visited` 调用，
内层循环的栈机模拟会把自己的 body 块重新标记到 `visited` 中，
外层循环的后续迭代就能正确跳过已处理块。

### 5.4 try/except 构建（BuildTryFromBlock）

```csharp
// 基于 SETUP_FINALLY 指令检测 try/except
1. 在 block 中查找 SETUP_FINALLY 指令
2. 读取参数（异常处理器偏移量）
3. 划分 try body 块（从 SETUP_FINALLY 之后到异常处理器之前）
4. 划分 handler 块（异常处理器区域）
5. 对每个 handler 块：
   a. 跳过 POP_TOP×3（异常对象入栈后的清理）
   b. 用 StackMachine 反编译 handler body
   c. 提取到 POP_EXCEPT 之前的语句
6. 构建 Try(Body, Handlers, Orelse, Finalbody)
```

---

## 6. PythonCodeGenerator — 代码生成

### 6.1 访问者模式实现

```csharp
public class PythonCodeGenerator
{
    private int _indentLevel;
    private readonly StringBuilder _sb = new();

    public string Generate(Module module)
    {
        Visit(module.Body);
        return _sb.ToString();
    }

    private void Visit(List<Stmt> stmts)
    {
        foreach (var stmt in stmts) Visit(stmt);
    }

    private void Visit(Stmt stmt) => stmt switch
    {
        // 控制结构
        If(var test, var body, var orelse) => EmitIf(test, body, orelse),
        While(var test, var body, var orelse) => EmitWhile(test, body, orelse),
        For(var target, var iter, var body, var orelse) => EmitFor(target, iter, body, orelse),
        Try(var body, var handlers, var orelse, var final) => EmitTry(body, handlers, orelse, final),

        // 语句
        Assign(var targets, var value) => EmitAssign(targets, value),
        Return(var value) => EmitReturn(value),
        ExprStmt(var value) => EmitExprStmt(value),
        Break() => EmitBreak(),
        Continue() => EmitContinue(),
        CommentStmt(var text) => EmitComment(text),  // ← 注释兜底

        // ...
    };
}
```

### 6.2 缩进管理

```csharp
private void WriteLine(string text = "")
{
    _sb.Append(new string(' ', _indentLevel * 4));
    _sb.AppendLine(text);
}

private IDisposable Indent()
{
    _indentLevel++;
    return new IndentDisposable(this);  // Dispose 时 _indentLevel--
}
```

### 6.3 注释块输出

```csharp
private void EmitComment(string text)
{
    // 将多行注释文本逐行输出
    foreach (var line in text.Split('\n', StringSplitOptions.None))
    {
        if (string.IsNullOrWhiteSpace(line))
            WriteLine("#");
        else
            WriteLine(line);  // 每行已包含 "# " 前缀
    }
}
```

---

## 7. Decompiler 主入口

```csharp
public class Decompiler
{
    public string Decompile(byte[] pycData)
    {
        // Phase 1: .pyc → CodeObject
        var reader = new PycReader();
        var codeObject = reader.Read(pycData);

        // Phase 2: CodeObject → 基本块 → 结构化 CFG
        var blockScanner = new BlockScanner();
        var blocks = blockScanner.Scan(codeObject);
        var cfScanner = new ControlFlowScanner();
        var structuredCFG = cfScanner.Analyze(blocks);

        // Phase 3: 结构化 CFG → AST（含 BlockDecompiler + 注释兜底）
        var astBuilder = new AstBuilder(codeObject);
        var ast = astBuilder.Build(structuredCFG);

        // Phase 4: AST → Python 源码
        var generator = new PythonCodeGenerator();
        return generator.Generate(ast);
    }
}
```

---

## 8. 版本矩阵读差异

### 8.1 .pyc 头部格式

| 版本 | 头部大小 | 字段 |
|------|---------|------|
| 2.7 | 8 字节 | magic(4) + timestamp(4) |
| 3.0-3.6 | 12 字节 | magic(4) + timestamp(4) + size(4) |
| 3.7+ | 16 字节 | magic(4) + flags(4) + hash/timestamp(8) |

实现中的三路分支：
```csharp
// 简化的 header 读取
var magic = br.ReadUInt32();
// 根据 magic 已知版本：
if (isPython27)  // skip 8B header
else if (isPre37) // skip 12B header
else  // skip 16B header (flags + hash)
```

### 8.2 pre-3.8 ref_index

Python 3.8 之前的 marshal 格式中，`TYPE_CODE` 之后有一个 `ref_index` 字段：
```csharp
if (version < 3.8)
    br.ReadInt32();  // 跳过 ref_index
```

### 8.3 3.11+ 变化（暂缓支持）

```
- CACHE 条目：每操作码后 1-4 字节的缓存区
- RESUME=90：与旧版 STORE_NAME=90 冲突
  → 通过 IsPython311Plus() && rawOp == 90 区分
- BINARY_OP 统一：BINARY_ADD/BINARY_SUB 合并为 BINARY_OP
- 异常表：从指令编码改为异常表条目
```

---

## 9. 测试体系

### 9.1 版本矩阵测试

```csharp
// 6 层级 × 7 版本 = 42 测试 (当前)
[Theory]
[InlineData("2.7"), InlineData("3.5"), ..., InlineData("3.10")]
public void Lv0_Expressions(string version) { ... }

[Theory]
[InlineData("2.7"), InlineData("3.5"), ..., InlineData("3.10")]
public void Lv1_Sequential(string version) { ... }

[Theory]
[InlineData("2.7"), InlineData("3.5"), ..., InlineData("3.10")]
public void Lv2_ControlFlow(string version) { ... }

// === Lv3 嵌套控制块 (Phase 3 新增) ===
[Theory]
[InlineData("2.7"), InlineData("3.5"), ..., InlineData("3.10")]
public void Lv3_NestedDepth(string version)    // 5 层同类型嵌套压力

[Theory]
[InlineData("2.7"), InlineData("3.5"), ..., InlineData("3.10")]
public void Lv3_NestedMixed(string version)    // 5 层混合类型嵌套

[Theory]
[InlineData("2.7"), InlineData("3.5"), ..., InlineData("3.10")]
public void Lv3_NestedMatrix(string version)   // 12 对偶 + 8 三重组合
```

### 9.2 比较方案

**方案 A：AST 语义比较（首选）**
```bash
python3 -c "import ast; print(ast.dump(ast.parse(open('out.py').read()), indent=2))"
```
- 忽略空白、注释、格式差异
- 等价于 `ast.dump()` 输出一致

**方案 B：Token 比较（回退）**
- 当没有 .py 源文件时使用
- 比较 token 序列（去除 INDENT/OUTDENT/ENDLINE）
- 用于 pycdc 测试套件中的 pre-tokenized 文件

### 9.3 测试文件编译

`compile_pyc_matrix.py` 使用 pyenv 管理多版本：
```bash
VERSIONS=("2.7.18" "3.5.10" "3.6.15" "3.7.17" "3.8.18" "3.9.18" "3.10.14")
for v in "${VERSIONS[@]}"; do
    pyenv local $v && python3 -m py_compile "$input.py" &&
    mv "__pycache__/input.cpython-*.pyc" "compiled/input.${v}.pyc"
done
```

---

## 10. 常见问题与故障排除

### 10.1 NullReferenceException — 12 字节 header

**症状**：Python 3.5/3.6 pyc 反编译时空引用异常。
**原因**：3.5/3.6 使用 12 字节头部，误读为 16 字节导致数据偏移 4 字节。
**修复**：根据 magic number 判断 header 大小。

### 10.2 FOR_ITER 后 body 为空

**症状**：for 循环体为空。
**原因**：`FindLastIndex` 获取了最后一个 LOAD 指令而非第一个；
`CollectBodyBlocks` 污染了 `visited`。
**修复**：改为 `FindIndex`（找第一个）；嵌套循环改用 `visited.Remove(bb)`。

### 10.3 无限递归/StackOverflow — 嵌套循环

**症状**：嵌套 while 循环导致 StackOverflow。
**原因**：每个 `BuildWhileLoop` 创建独立 `bodyVisited`，嵌套后 body 块被重复处理。
**修复**：移除 body 块从 visited，用同一 visited 直传（详见 5.3 节）。

### 10.4 `else :` 有额外空格

**症状**：生成的 `else :` 而非 `else:`。
**原因**：`PythonCodeGenerator.cs` 中字面量为 `"else :"`。
**修复**：改为 `"else:"`，同理 `try:`、`finally:`。

### 10.5 POP_TOP 在 for 循环体中不生效

**症状**：for 循环中的 break 被忽略。
**原因**：FOR_ITER 不压栈，POP_TOP 的 SafePop() 返回 null。
**修复**：添加 `_isForLoop` 标志，POP_TOP 在 for 体中返回 `Break()`。

---

## 11. Lv3 嵌套控制块测试设计

### 11.1 设计目标

Lv3 的核心目标是验证 **AstBuilder 在大量嵌套控制块时的稳定性**。通过对偶矩阵（depth 2）、三重/四重组合（depth 3-4）、同类型 5 层深嵌套（depth 5）的全面覆盖，确保：

1. visited 集合不泄露（不丢失已处理块）
2. 嵌套循环不 StackOverflow
3. else 子句在各种嵌套深度下正确识别
4. try 的 body 收集在嵌套场景下不吞掉内层块
5. 空体（pass）在深层嵌套中正确生成

### 11.2 三层测试架构

#### 文件 A: `test_nested_depth_5.py` — 同类型 5 层深度压力

```
depth_5_if(x0, x1, x2, x3, x4):    if > if > if > if > if
  检验点: 5 层 if/else 链，每层都有 else，最终 result 值 = 42

depth_5_for():                       for > for > for > for > for
  检验点: 5 层 for range(2)，迭代次数 2^5=32，total 最终 = 32

depth_5_while():                     while > while > while > while > while
  检验点: 5 层 while，每层递减计数，total 最终 = 32

depth_5_try():                       try > try > try > try > try
  检验点: 5 层 try/except，最内层赋值 42，各层 except 捕获不到
```

#### 文件 B: `test_nested_mixed_5.py` — 混合类型 5 层嵌套

```
mixed_1():     if > for > while > try > if
  检验点: 条件中嵌循环，循环中嵌 while，while 中嵌 try，try 中嵌 if

mixed_2():     for > while > try > if > for
  检验点: 循环嵌循环，内层嵌 try，try 中嵌 if，if 中嵌 for

mixed_3():     while > try > if > for > while
  检验点: while 嵌 try，try 中嵌 if，if 中嵌 for，for 中嵌 while

mixed_4():     try > if > for > while > try
  检验点: try 中嵌 if，if 中嵌 for，for 中嵌 while，while 中嵌 try
```

#### 文件 C: `test_nested_matrix.py` — 12 对偶 + 8 三重组合

```
=== PAIR MATRIX (depth 2, 12 combos) ===
  pair_if_for           if > for         ← 如果条件成立，执行循环
  pair_if_while         if > while       ← 如果条件成立，执行 while
  pair_if_try           if > try         ← 如果条件成立，执行 try
  pair_for_if           for > if         ← 循环体内带条件
  pair_for_while        for > while      ← 循环体内嵌 while
  pair_for_try          for > try        ← 循环体内嵌 try
  pair_while_if         while > if       ← while 体内带条件
  pair_while_for        while > for      ← while 体内嵌 for
  pair_while_try        while > try      ← while 体内嵌 try
  pair_try_if           try > if         ← try 体内带条件
  pair_try_for          try > for        ← try 体内嵌 for
  pair_try_while        try > while      ← try 体内嵌 while

=== TRIPLE COMBOS (depth 3, 8 combos) ===
  triple_if_for_while       if > for > while
  triple_for_while_if       for > while > if
  triple_while_if_for       while > if > for
  triple_try_for_while      try > for > while
  triple_for_try_if         for > try > if
  triple_if_try_for         if > try > for
  triple_while_try_for      while > try > for
  triple_try_while_if       try > while > if

=== QUAD COMBOS (depth 4, 2 combos) ===
  quad_for_while_if_try     for > while > if > try
  quad_while_if_for_try     while > if > for > try
```

### 11.3 覆盖矩阵总览

| 维度 | 计算 | 数量 |
|------|------|------|
| 同类型深度 5 | 4 种类型 × 5 层 | 4 函数 |
| 混合深度 5 | 4 种排列 × 5 层 | 4 函数 |
| 对偶矩阵 | 4 种外 × 3 种内 (排除自身) | 12 函数 |
| 三重组合 | 4 选 3 × 排列 | 8 函数 |
| 四重组合 | 4 种类型各 1 × 2 排列 | 2 函数 |
| **总计** | | **30 函数** |

### 11.4 预期通过条件

- 每个函数的反编译输出经 `ast.dump()` 比较与原 .py 源一致
- 无 StackOverflow 异常
- 无 visited 泄露（不重复输出同一块）
- 所有 else 子句正确归属
- pass 在空体中正确生成

### 11.2 Lv4 函数/类

- def 语句识别
- lambda 表达式
- class 定义
- 参数与默认值
- 装饰器

### 11.3 GUI 完善

- AvaloniaEdit 语法高亮
- 注释块着色（红色）
- 版本选择器
- 批量反编译
- 统计面板
