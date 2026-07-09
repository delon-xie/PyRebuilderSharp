
# 文档二：Python反编译详细设计.md

## Python字节码反编译器详细设计

**版本**: v2.7
**日期**: 2026-07-09
**项目**: PyRebuilderSharp
**状态**: Phase 1–6 ✅ + Phase Fix ✅ + Phase 7 标注优先顺序块流水线 🚀 — 4 阶段标注链路 · 逐 ET 条目标注 · 回边标注 · 统一链接

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

## 3. CPython 源码研读指南

### 3.1 研读动机

反编译是编译的逆过程。只有深入理解 CPython 的编译步骤，才能写出精准的反编译器。以下是实际开发中通过研读 CPython 源码解决的关键问题清单：

| 问题 | CPython 源文件 | 行/函数 | 价值 |
|------|--------------|---------|------|
| v2.7 TYPE_STRINGREF vs TYPE_INTERNAL_REF | `Python/marshal.c` | `#define TYPE_STRINGREF 'R'` | **P0** — 直接决定 marshal 读取正确性 |
| v3.11+ TYPE_CODE_SIMPLE 格式 | `Python/marshal.c` | `case TYPE_CODE_SIMPLE:` | **P0** — 3.11+ 反编译前提 |
| FLAG_REF 的引入版本 | `Python/marshal.c` (3.4) | `r_object` 的参数改为 `flag` | **P1** — 版本分支判断 |
| for 循环的 FOR_ITER/GET_ITER 生成 | `Python/compile.c` | `compiler_for` | **P1** — 反解 loop variable |
| try/except 的 SETUP_FINALLY 生成 | `Python/compile.c` | `compiler_try_except` | **P1** — 反解 try body 范围 |
| v3.11+ ExceptionTable 格式 | `Python/marshal.c` | exceptiontable 读/写 | **P2** — 3.11+ try 反解 |
| v3.11+ linetable 编码 | `Objects/lnotab_notes.txt` | PEP 626 | **P2** — 行号映射 |
| with 语句编译模式 | `Python/compile.c` | `compiler_with` | **P2** — 反解 __enter__/__exit__ |
| match/case 编译 | `Python/compile.c` (3.10+) | `compiler_match` | **P3** — 3.10+ 新语法 |
| YIELD_FROM 的栈操作 | `Python/ceval.c` | `YIELD_FROM` case | **P1** — 生成器反解 |
| RESUME 指令歧义 (90) | `Include/opcode.h` (3.11+) | RESUME=90, STORE_NAME=90 | **P1** — 3.11+ 操作码冲突 |

### 3.2 compile.c — 核心编译流水线

```c
// compile.c 编译一个模块的入口
static PyCodeObject *
compiler_mod(struct compiler *c, mod_ty mod)
{
    // Step 1: 符号表分析 — 确定变量作用域
    //   结果在 c->u->u_ste->ste_... 中
    //   反编译: 看 co_names / co_varnames / co_freevars / co_cellvars
    
    // Step 2: 进入作用域
    compiler_enter_scope(c, ...);
    
    // Step 3: 根据 AST 类型分发编译
    switch (mod->kind) {
    case Module_kind:
        compiler_body(c, mod->v.Module.body);  // 编译所有语句
        break;
    }
    
    // Step 4: 汇编 → 字节码数组
    return assemble(c, 1);  // 关键函数
}
```

**assemble() 函数** 是学习反编译的宝库。它将编译器内部的 `basicblock` 链转换为最终字节码数组。反编译 Phase 2（分块）要做的就是反转 assemble 的步骤。

### 3.3 ceval.c — 字节码解释器

`Python/ceval.c` 的 `_PyEval_EvalFrameDefault` 函数是 Python 的解释器核心。StackMachine 栈机模拟就是对这个函数的**逻辑重演**。

```c
// ceval.c 的核心循环
PyObject *
_PyEval_EvalFrameDefault(PyFrameObject *f, int exc)
{
    // ... 各种准备工作
    
    main_loop:
    for (;;) {
        opcode = NEXTOPARG();  // 取下一条指令
        switch (opcode) {
        case LOAD_CONST:
            x = GETITEM(consts, oparg);
            Py_INCREF(x);
            PUSH(x);
            goto main_loop;
            
        case STORE_NAME:
            w = GETITEM(names, oparg);
            v = POP();
            PyDict_SetItem(f->f_globals, w, v);  // 全局赋值
            goto main_loop;
            
        case BINARY_ADD:
            w = POP();
            v = BINARY_OP1(v, w, NB_ADD);  // v + w
            PUSH(v);
            goto main_loop;
        }
    }
}
```

**对反编译的启发**：
- 每条指令的栈操作（POP/PUSH）都可以在 StackMachine 中模拟
- `LOAD_CONST` → `Constant()`, `LOAD_NAME` → `Name()`, `STORE_NAME` → `Assign()`
- 栈的深度和顺序必须精确模拟

### 3.4 marshal.c — 序列化格式权威参考

`Python/marshal.c` 是 PycReader 的**最高权威**。任何第三方工具的实现都可能错误，只有 CPython 的源码是可信的。

**研读重点**：

```c
// r_object() — 反序列化核心
// Python 2.7 版本: 无 flag 参数，无 refstack
// Python 3.4+ 版本: 有 flag 参数，有 refstack + FLAG_REF
static PyObject *
r_object(RFILE *p)
{
    int type = r_byte(p);  // 读取类型字节
    PyObject *v;
    
    switch (type) {
    case TYPE_CODE:     // 'c' (99)
        // v2.7: 直接进入读取
        // v3.4+: 先 r_ref_reserve() 预留槽位
        ...
        v = PyCode_New(argcount, ..., lnotab);
        // v3.4+: r_ref_set(p, v) 存入 refstack
        break;
    }
}
```

**关键发现（实际调试经验）**：
- v2.7 marshal.c 没有 `r_ref_reserve` / `r_ref_set` 调用
- v2.7 的 ref 机制完全依赖 `p->strings`（interned strings 列表）
- v2.7 `'R'` (0x52) = TYPE_STRINGREF，引用的是 interned string，不是代码对象
- v3.4+ 的 `FLAG_REF` (0x80) 和 `TYPE_REF` (0x52) 是全新的机制

### 3.5 编译过程调试方法

**工具链**：
```bash
# 1. 用 dis 查看字节码
python3 -m dis test.py

# 2. 查看代码对象结构
python3 -c "
import dis
with open('test.py') as f:
    code = compile(f.read(), 'test.py', 'exec')
print('names:', code.co_names)
print('varnames:', code.co_varnames)
print('consts:', [type(c).__name__ for c in code.co_consts])
print('flags:', bin(code.co_flags))
dis.dis(code)
"

# 3. 查看 .pyc 二进制结构
od -A x -t x1z -v test.pyc | head -20

# 4. 跨版本: pyenv 切换不同 Python 版本编译/比较
pyenv local 3.10.14
python3 -m py_compile test.py
```

---

## 4. 逐块反编译引擎（BlockDecompiler）

### 4.1 BlockResult — 成功/失败统一返回

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

### 4.2 BlockDecompiler 完整流程

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

## 5. StackMachine 栈机模拟

### 5.1 指令处理对照表

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

### 5.2 break/continue 识别

```
break 识别 (for 循环体):
  FOR_ITER → 循环体 block
  POP_TOP 在 for loop body 中 → Break()

continue 识别:
  JUMP_ABSOLUTE → _loopHeaderOffsets.Contains(target) → Continue()
```

### 5.3 2.7 版本差异

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

## 6. AstBuilder — 控制结构构建

### 6.1 控制结构识别算法

```
GetStructuredBlockStmts(block, visited):
  1. if visited.Contains(block) → return []
  2. visited.Add(block)
  3. if block.Flags.HasFlag(LoopHeader) → BuildLoop(block, visited)
  4. if IsConditionBranch(block) → BuildRestrictedIfElse(block, visited)
  5. if BuildTryFromBlock(block) != null → return tryResult
  6. else → GetBlockStmts(block)  (平坦语句)
```

### 6.2 循环构建（BuildLoop → BuildWhileLoop / BuildForLoop）

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

### 6.3 嵌套循环 StackOverflow 修复（关键变更）

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

### 6.4 try/except 构建（BuildTryFromBlock）

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

## 7. SequentialBlockBuilder — 顺序块构建（Phase 7 新架构）

### 7.1 职责

SequentialBlockBuilder 是 Phase 7 新架构的核心组件，负责将 `ControlFlowGraph.BasicBlock[]` 合并为 **SequentialBlock**（顺序块）列表。每个 SequentialBlock 代表一段不含控制流分支的线性指令序列。

### 7.2 MergeLinearChain — 线性链合并算法

```csharp
private SequentialBlock MergeLinearChain(BasicBlock start, List<BasicBlock> allBlocks, HashSet<int> processed)
{
    var seqBlock = new SequentialBlock();
    var current = start;

    while (current != null && !processed.Contains(current.Id))
    {
        // 终止条件（满足任一即停止合并）：
        // 1. 当前块以跳转指令结尾（JUMP/FOR_ITER/等）
        // 2. 当前块有多个后继（分支点）
        // 3. 下一块有多个前驱（汇聚点）
        // 4. 下一块以 with/try 头开始（控制结构边界）
        // 5. 检测到 with 清除模式（LOAD_CONST×3 + CALL + POP_TOP）
        // 6. 模块入口（StartOffset==0）无 LOAD_SPECIAL/SETUP_WITH

        processed.Add(current.Id);
        seqBlock.Instructions.AddRange(current.Instructions);

        if (IsJump(current) || current.Successors.Count != 1) break;

        var next = current.Successors.First();
        if (next.Predecessors.Count != 1 || processed.Contains(next.Id)) break;
        if (StartsWithControlHeader(next)) break;

        current = next;
    }
    return seqBlock;
}
```

### 7.3 AnnotateSequentialBlock — 块标注

每个 SequentialBlock 构建后，会扫描其指令序列标注属性：
- `IsLoopHeader` — 包含 FOR_ITER 或 POP_JUMP_IF_* 指令
- `HasSetupWith / HasBeforeWith / HasLoadSpecial` — with 语句相关
- `HasSetupFinally / HasSetupExcept` — try 语句相关
- `IsConditionHeader` — JUMP_IF_FALSE_OR_POP / JUMP_IF_TRUE_OR_POP
- `ExceptionTableEntries` — 从 CodeObject.ExceptionTable 匹配落入本块的条目

### 7.4 SequentialBlock 后继图构建

`BuildSequentialBlockGraph` 根据 SourceBlocks 的 CFG succ/pred 关系，将 BasicBlock 级别的边映射为 SequentialBlock 级别的边。

### 7.5 VerifyNoOrphanBlocks — 无孤儿块校验

```csharp
public bool VerifyNoOrphanBlocks(List<SequentialBlock> seqBlocks, ControlFlowGraph cfg)
{
    var allIds = cfg.Blocks.Where(b => b.Instructions.Count > 0).Select(b => b.Id);
    var processedIds = seqBlocks.SelectMany(sb => sb.SourceBlocks).Select(b => b.Id);
    return allIds.Except(processedIds).Count() == 0;
}
```

如果返回 false，则 `BuildWithSequentialBlocks` 自动降级到 BuildFallback。

---

## 8. ControlStructure Parser — 标注优先的解析架构（Phase 3b）

### 8.1 标注优先原则

Phase 7 的 ControlStructure Parser 遵循**标注优先**原则：先多轮扫描收集标注信息，再统一链接组装。整个流程分为四个子阶段：

```
Phase 2:  ExceptionTable 标注扫描
    ↓
Phase 3:  控制块起始标注扫描
    ↓
Phase 4:  回边标注扫描
    ↓
Phase 5:  统一链接（基于所有标注信息）
    ↓
Phase 3c: 混合遍历 AST 组装
```

### 8.2 Phase 2: ExceptionTable 标注扫描

**适用范围**: Python 3.11+（ExceptionTable 机制）

逐个遍历所有 SequentialBlock 的 `ExceptionTableEntries` 属性，为每个符合 `Depth == 0 && !Lasti && (IsExcept || IsFinally)` 的条目对应的 SequentialBlock 设置标注：

```csharp
// 扫描所有 ET 条目，收集唯一 try 起始偏移
var tryStartOffsets = new HashSet<int>();
foreach (var seqBlock in seqBlocks)
{
    foreach (var et in seqBlock.ExceptionTableEntries)
    {
        if (et.Depth == 0 && !et.Lasti && (et.IsExcept || et.IsFinally))
            tryStartOffsets.Add(et.StartOffset);
    }
}

// 为每个 try 找到对应的 header seqBlock
var tryHeaders = new HashSet<SequentialBlock>();
foreach (var tryStart in tryStartOffsets.OrderBy(x => x))
{
    var headerBlock = seqBlocks.FirstOrDefault(sb =>
        sb.StartOffset <= tryStart && sb.EndOffset > tryStart);
    if (headerBlock != null && tryHeaders.Add(headerBlock))
    {
        headerBlock.IsTryHeader = true;
        headerBlock.ExceptionTryStartOffset = tryStart;
        // 从 ET 条目推导 try body 结束偏移
        var primaryEntry = seqBlock.ExceptionTableEntries
            .FirstOrDefault(et => et.StartOffset == tryStart);
        if (primaryEntry != null)
            headerBlock.ExceptionTryEndOffset = primaryEntry.EndOffset;
    }
}
```

**关键**: 逐 ET 条目标注，而非全局合并。避免将多个 try/except 合并为一个。

### 8.3 Phase 3: 控制块起始标注扫描

遍历所有 SequentialBlock，扫描指令流，为控制块起始设置标注：

| 指令模式 | 标注 | 说明 |
|---------|------|------|
| `FOR_ITER` | `IsLoopHeader = true` | for 循环头 |
| `POP_JUMP_IF_*` + 回边 | `IsLoopHeader = true` | while 循环头 |
| `SETUP_FINALLY` / `SETUP_EXCEPT` | `IsTryHeader = true` | try 头（3.10-） |
| ET StartOffset 匹配 | `IsTryHeader = true` | try 头（3.11+） |
| `SETUP_WITH` / `BEFORE_WITH` / `LOAD_SPECIAL` | `IsWithHeader = true` | with 头 |
| `POP_JUMP_IF_*`（无回边） | `IsConditionHeader = true` | if/else 头 |
| `JUMP_IF_FALSE_OR_POP` / `JUMP_IF_TRUE_OR_POP` | `IsConditionHeader = true` | if/else 头（3.11+） |

**标注顺序**: 循环头优先标注（逆序，内层优先），然后是 try/with/if 头。

### 8.4 Phase 4: 回边标注扫描

遍历所有 SequentialBlock 的指令，识别回边和循环体：

```csharp
// 回边检测: JUMP_ABSOLUTE → 目标偏移指向已标注的 IsLoopHeader
foreach (var seqBlock in seqBlocks)
{
    foreach (var instr in seqBlock.Instructions)
    {
        if (instr.Opcode == Opcode.JUMP_ABSOLUTE && instr.Argument.HasValue)
        {
            var targetOffset = instr.Argument.Value;
            var target = seqBlocks.FirstOrDefault(sb =>
                sb.StartOffset <= targetOffset && sb.EndOffset >= targetOffset);
            if (target != null && target.IsLoopHeader)
            {
                seqBlock.IsBackEdgeTarget = true;  // 回边块
                target.IsLoopBody = true;           // 目标 → 循环体
            }
        }
    }
}

// FOR_ITER 的 JumpTarget 指向 else/exit 块
foreach (var seqBlock in seqBlocks.Where(b => b.IsLoopHeader))
{
    var forIter = seqBlock.Instructions.FirstOrDefault(i => i.Opcode == Opcode.FOR_ITER);
    if (forIter.Argument.HasValue)
    {
        // FOR_ITER 的目标 = 循环 else/exit 入口
        var forTarget = findSeqBlockByOffset(forIter.Argument.Value);
        if (forTarget != null)
            forTarget.IsForIterElseBlock = true;
    }
}
```

### 8.5 Phase 5: 统一链接

基于所有标注信息，统一创建控制结构对象：

```csharp
var structures = new List<ISequentialControlStructure>();

// 1. 先链接 Try 结构（ExceptionTable 定义了严格的 offset 边界）
foreach (var seqBlock in seqBlocks.Where(b => b.IsTryHeader && !visited.Contains(b.Id)))
{
    var tryStructure = BuildTryStructure(seqBlock, seqBlocks);
    if (tryStructure != null)
    {
        structures.Add(tryStructure);
        MarkStructureVisited(tryStructure);
    }
}

// 2. 然后链接 Loop 结构（可能嵌套在 Try 的 body 中）
foreach (var seqBlock in seqBlocks.Where(b => b.IsLoopHeader && !visited.Contains(b.Id)))
{
    var loopStructure = BuildLoopStructure(seqBlock, seqBlocks);
    if (loopStructure != null)
    {
        structures.Add(loopStructure);
        MarkStructureVisited(loopStructure);
    }
}

// 3. 再链接 With 结构
foreach (var seqBlock in seqBlocks.Where(b => b.IsWithHeader && !visited.Contains(b.Id)))
{
    var withStructure = BuildWithStructure(seqBlock, seqBlocks);
    if (withStructure != null)
    {
        structures.Add(withStructure);
        MarkStructureVisited(withStructure);
    }
}

// 4. 最后链接 IfElse 结构（最灵活，不与其他结构冲突）
foreach (var seqBlock in seqBlocks.Where(b => b.IsConditionHeader && !visited.Contains(b.Id)))
{
    var ifElseStructure = BuildIfElseStructure(seqBlock, seqBlocks);
    if (ifElseStructure != null)
    {
        structures.Add(ifElseStructure);
        MarkStructureVisited(ifElseStructure);
    }
}
```

**链接优先级**: Try > Loop > With > IfElse。Try 先用 ExceptionTable 的严格 offset 边界约束，然后是 Loop（可能嵌套在 Try body 中），With 和 IfElse 最后。

### 8.6 BuildTryStructure — ExceptionTable 模式（3.11+）

核心流程：

```csharp
// 1. 从 seqBlock.ExceptionTableEntries 筛选与 header.StartOffset 匹配的条目
// 2. 按 Depth 分组 handler
// 3. 收集 try body 块（使用 overlap check: body end > tryStart && body start < tryEnd）
//    注意: 必须用 EndOffset > StartOffset 的重叠检查而非 >= 检查，
//    因为 header seqBlock 可能包含 try 之前的代码（MergeLinearChain 合并了前缀）
// 4. 对每个 handler 块，检查 PUSH_EXC_INFO/CHECK_EXC_MATCH/STORE_FAST
// 5. 如果有 IsFinally 条目 → 构建 finally-block
// 6. 否则如果 handler 后有 else 范围的 seqBlock → 构建 else-block
```

### 8.7 BuildTryStructure — SETUP_FINALLY 模式（3.10-）

核心流程：

```csharp
// 1. 从 header.Instructions 中找到 SETUP_FINALLY/SETUP_EXCEPT
// 2. 读取指令的 Argument（handler 偏移量）
// 3. 通过 offset 找到 handler 的 seqBlock
// 4. 将 header 本身加入 bodyBlocks（header 包含 try body 的指令）
// 5. BFS 遍历后继块，跳过 handler 偏移量
// 6. 构建 try 结构
```

### 8.8 LinkControlStructures — 结构链接

将解析出的控制结构链接回 SequentialBlock 列表：
- `structure.Header.ParentStructure = structure`
- 对所有 `structure.BodyBlocks` 设置 ParentStructure
- 对 Try 的 handler/else/finally 子块递归设置
- 对 IfElse 的 true/false branch 设置
- 对 try 结构范围内未被覆盖的 seqBlock（包含 PUSH_EXC_INFO / RERAISE / POP_EXCEPT 等指令的）也设置为 try 的所属

---

## 9. GenerateAstStatementsHybrid — 混合遍历（Phase 3c）

### 9.1 遍历策略

Hybrid 遍历分为两个阶段：

**第一阶段（主 DFS 遍历）**：
1. 从入口顺序块（cfg.Entry 映射的 SequentialBlock）出发
2. 对每个顺序块：
   - 如果 `structureHeaders.Contains(seqBlock.Id)` → 调用 `BuildStructureStatements()`
   - 否则如果 `seqBlock.ParentStructure != null` → 跳过（属于某个控制结构的 body）
   - 否则 → 直接输出 `seqBlock.Statements`（缓存的反编译结果）
3. 递归后继，用 processedSeqBlocks HashSet 防重复

**第二阶段（补齐扫描）**：
遍历所有顺序块，处理第一阶段未被处理的情况：
- 结构头未被 DFS 覆盖 → 调用 BuildStructureStatements
- 未归属结构的块 → 直接输出缓存语句

### 9.2 标记机制

`MarkStructureBlocksProcessed` 将整个结构的块（header + body + handler + else + finally）标记为已处理，防止后续重复输出。

### 9.3 Try 结构的 Merge Point 处理

try 结构在 Hybrid 遍历中不继续后继遍历（return stmts），因为 try 的后续由 ExceptionTable 的出口偏移确定，而非 CFG succ 边。For/While/IfElse 结构会通过 FindMergePoint 找到 merge point 并继续后继遍历。

---

## 10. PythonCodeGenerator — 代码生成

### 10.1 访问者模式实现

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

### 10.2 缩进管理

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

### 10.3 注释块输出

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

## 11. Decompiler 主入口

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

## 12. 版本矩阵读差异

### 12.1 .pyc 头部格式

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

### 12.2 pre-3.8 ref_index

Python 3.8 之前的 marshal 格式中，`TYPE_CODE` 之后有一个 `ref_index` 字段：
```csharp
if (version < 3.8)
    br.ReadInt32();  // 跳过 ref_index
```

### 12.3 3.11+ Marshal 格式变化

Python 3.11+ 在 marshal 格式上有重大变更：

#### TYPE_CODE 字段数变化

```
3.8-3.10: argcount + posonlyargcount + kwonlyargcount + nlocals + stacksize + flags (6 fields)
3.11+:    argcount + posonlyargcount + kwonlyargcount + stacksize + flags (5 fields, 去掉了 nlocals!)
```

nlocals 改为由 `localsplusnames` + `localspluskinds` 派生。

#### TYPE_CODE_SIMPLE (115) 新类型

v3.11+ 引入 `TYPE_CODE_SIMPLE`（值=115=0x73），与旧版 `TYPE_STRING` 同值。用于简化内嵌代码对象：

```
TYPE_CODE_SIMPLE: argcount + nlocals + stacksize + flags (4 fields)
```

**冲突处理**：内嵌 code 对象的 bytecode/linetable/exceptiontable 字段使用 TYPE_STRING(0x73) 存储。通过 `IsPython311Plus()` 在 `ReadMarshalValue` 中区分：
- TYPE_STRING(115) + v3.11+ → 优先匹配 `ReadMarshalCodeObject(isSimple: true)`
- 字节码/linetable/exceptiontable 等明确期望 bytes 的字段 → 使用 `ReadRawMarshalBytes` 直接读取，避免误判

#### v3.11+ 字段顺序

```
TYPE_CODE (99):
  argcount (int32)
  posonlyargcount (int32)
  kwonlyargcount (int32)
  stacksize (int32)
  flags (int32)
  code (marshal bytes: type=0x73 + int32 len + raw bytes)
  consts (marshal tuple)
  names (marshal tuple of strings)
  localsplusnames (marshal tuple → 替代 varnames + cellvars + freevars)
  localspluskinds (marshal bytes → 变量类型编码)
  filename (marshal string)
  name (marshal string)
  qualname (marshal string)  ← 新增
  firstlineno (int32)
  linetable (marshal bytes → 替代 lnotab)
  exceptiontable (marshal bytes)  ← 新增
```

#### 其他变化

| 变化 | 说明 | 处理 |
|------|------|------|
| CACHE 条目 | adaptive 指令后的 2 字节槽 | 跳过 `rawOp==0`（不依赖 cache 表） |
| RESUME=90 | 与旧版 STORE_NAME 同值 | `IsPython311Plus() && rawOp == 90` → Opcode.RESUME |
| JUMP_BACKWARD | 替代 JUMP_ABSOLUTE 的回跳 | 跳转方向不同 |
| POP_JUMP_FORWARD_IF_* | 替代 POP_JUMP_IF_* 的前跳 | 跳转方向不同 |
| 无 SETUP_FINALLY/POP_BLOCK/END_FINALLY | 异常处理全在 ExceptionTable | 反编译流水线待适配 |
| localsplusnames/kinds | 替代 varnames + cellvars + freevars | 合并到 Varnames 列表 |
| linetable | 替代 lnotab（新编码格式） | 暂不解析 |
| exceptiontable | 新增的异常映射表 | 已解析，反编译未使用 |

---

## 13. 测试体系

### 13.1 版本矩阵测试

```csharp
// 7 层级 × 11 版本 = 77 测试 (2.7 → 3.14 全覆盖)
// Lv0_Expressions: test_expr_basic       → 11 versions
// Lv1_Sequential:  test_seq_clean        → 11 versions  
// Lv2_ControlFlow: test_control_flow     → 11 versions
// Lv3_X:           test_nested_depth_5   → 11 versions
// Lv3_Y:           test_nested_mixed_5   → 11 versions
// Lv3_Z:           test_nested_matrix    → 11 versions
// Lv3-1:           test_nested_depth_9   → 11 versions (九层塔)
```

测试通过所有 `known_issue` 版本。AST 语义比较仍在收敛中。
3.11+ 版本通过 marshal 3.11+ 格式修复正确读取。
3.13/3.14 的 marshal 格式与 3.11/3.12 兼容。

```csharp
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

### 13.2 比较方案

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

### 13.3 测试文件编译

`compile_pyc_matrix.py` 使用 pyenv 管理多版本：
```bash
VERSIONS=("2.7.18" "3.5.10" "3.6.15" "3.7.17" "3.8.18" "3.9.18" "3.10.14")
for v in "${VERSIONS[@]}"; do
    pyenv local $v && python3 -m py_compile "$input.py" &&
    mv "__pycache__/input.cpython-*.pyc" "compiled/input.${v}.pyc"
done
```

---

## 14. 常见问题与故障排除

### 14.1 NullReferenceException — 12 字节 header

**症状**：Python 3.5/3.6 pyc 反编译时空引用异常。
**原因**：3.5/3.6 使用 12 字节头部，误读为 16 字节导致数据偏移 4 字节。
**修复**：根据 magic number 判断 header 大小。

### 14.2 FOR_ITER 后 body 为空

**症状**：for 循环体为空。
**原因**：`FindLastIndex` 获取了最后一个 LOAD 指令而非第一个；
`CollectBodyBlocks` 污染了 `visited`。
**修复**：改为 `FindIndex`（找第一个）；嵌套循环改用 `visited.Remove(bb)`。

### 14.3 无限递归/StackOverflow — 嵌套循环

**症状**：嵌套 while 循环导致 StackOverflow。
**原因**：每个 `BuildWhileLoop` 创建独立 `bodyVisited`，嵌套后 body 块被重复处理。
**修复**：移除 body 块从 visited，用同一 visited 直传（详见 6.3 节）。

### 14.4 `else :` 有额外空格

**症状**：生成的 `else :` 而非 `else:`。
**原因**：`PythonCodeGenerator.cs` 中字面量为 `"else :"`。
**修复**：改为 `"else:"`，同理 `try:`、`finally:`。

### 14.5 POP_TOP 在 for 循环体中不生效

**症状**：for 循环中的 break 被忽略。
**原因**：FOR_ITER 不压栈，POP_TOP 的 SafePop() 返回 null。
**修复**：添加 `_isForLoop` 标志，POP_TOP 在 for 体中返回 `Break()`。

### 14.6 v2.7 names 偏少 / strref_N 异常

**症状**：模块 names 数量不对，或输出 `strref_N`。
**原因**：误将 TYPE_STRINGREF(0x52) 当作 TYPE_INTERNAL_REF 处理，查了错误的 ref 列表。
**修复**：v2.7 中 0x52 是 TYPE_STRINGREF，从 `_internedStrings27` 查找，不是 `_refList27`。

---

## 15. Lv3 嵌套控制块测试设计

### 15.1 设计目标

Lv3 的核心目标是验证 **AstBuilder 在大量嵌套控制块时的稳定性**。通过对偶矩阵（depth 2）、三重/四重组合（depth 3-4）、同类型 5 层深嵌套（depth 5）的全面覆盖，确保：

1. visited 集合不泄露（不丢失已处理块）
2. 嵌套循环不 StackOverflow
3. else 子句在各种嵌套深度下正确识别
4. try 的 body 收集在嵌套场景下不吞掉内层块
5. 空体（pass）在深层嵌套中正确生成

### 15.2 三层测试架构

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

### 15.3 覆盖矩阵总览

| 维度 | 计算 | 数量 |
|------|------|------|
| 同类型深度 5 | 4 种类型 × 5 层 | 4 函数 |
| 混合深度 5 | 4 种排列 × 5 层 | 4 函数 |
| 对偶矩阵 | 4 种外 × 3 种内 (排除自身) | 12 函数 |
| 三重组合 | 4 选 3 × 排列 | 8 函数 |
| 四重组合 | 4 种类型各 1 × 2 排列 | 2 函数 |
| **总计** | | **30 函数** |

### 15.4 预期通过条件

- 每个函数的反编译输出经 `ast.dump()` 比较与原 .py 源一致
- 无 StackOverflow 异常
- 无 visited 泄露（不重复输出同一块）
- 所有 else 子句正确归属
- pass 在空体中正确生成

---

## 16. Phase 4〜8 阶段开发详情

### 16.1 Phase 4 — 函数/类/生成器（P0）

#### Lv4a: lambda 表达式修复

**状态**: ⏳ 进行中
**难点**: lambda 的 code object 在模块 consts 中内嵌。需识别 `co_name == '<lambda>'` 的 code 对象，将其反编译为 `Lambda(args, body)` 而非 `def func(args): body`。

```python
# 源码
f = lambda x: x + 1

# 字节码视角
# 1. LOAD_CONST <code object <lambda> at ...>  (consts 中为 TYPE_CODE)
# 2. MAKE_FUNCTION 0
# 3. STORE_NAME 'f'
```

**关键指令**: `MAKE_FUNCTION` / `LOAD_CONST(code_obj)` / `LOAD_LAMBDA`

**v2.7 差异**: Python 2.7 lambda 使用 `MAKE_FUNCTION` 指令，与 3.x 相同。

#### Lv4b: def 语句

```python
# 源码
def func(a, b=10, *args, **kwargs):
    return a + b
```

**检测**: 
- `MAKE_FUNCTION` + `STORE_NAME` → def 语句
- 函数名从 `STORE_NAME` 的参数获取
- 默认值从 consts 中对应 code 对象之前的 consts 项获取
- `co_argcount` 与 `co_varnames` 的前 N 项对应参数
- `co_flags & VARARGS` → `*args`；`co_flags & VARKEYWORDS` → `**kwargs`

**关键指令**: `MAKE_FUNCTION` / `MAKE_CLOSURE` / `LOAD_CONST` (code obj) / `STORE_NAME`

#### Lv4c: class 定义

```python
class MyClass(Base1, Base2):
    x = 1
    def method(self):
        pass
```

**检测**: 
- `BUILD_CLASS` + `STORE_NAME` → class 语句
- Load consts 中的 code object（class body）
- Load names 中的基类名
- class body 的 code object 使用 `exect()` 执行（专用指令序列）

**关键指令**: `LOAD_BUILD_CLASS` / `BUILD_CLASS` / `LOAD_CONST` (code obj) / `LOAD_NAME` (base classes)

#### Lv4d: 装饰器

```python
@decorator1
@decorator2(arg)
def func():
    pass
```

**检测**: 
- 函数定义前有 `LOAD_NAME` / `CALL_FUNCTION`... `STORE_NAME` 序列
- `STORE_NAME` 重写为 `Assign` with decorated target
- 需要在 AstBuilder 中识别 `LOAD_NAME decorator; CALL_FUNCTION; STORE_NAME func` 模式

#### Lv4e: 生成器

```python
def gen():
    yield 1
    yield from other_gen
```

**检测**: `co_flags & 0x20 (CO_GENERATOR)` → 生成器函数
- `YIELD_VALUE` → `Yield(expr)` 表达式
- `YIELD_FROM` (opcode=72 in 3.5-3.9 / 72 in 3.10) → `YieldFrom(expr)`
- StackMachine 需处理 YIELD_VALUE 不设置返回值

### 16.2 Phase 5 — 异常/流程增强（P1）

| 子项 | 内容 | 检测方式 |
|------|------|---------|
| **with** | `SETUP_WITH` + `WITH_EXCEPT_START` | 反解为 `With(items, body)` |
| **finally** | `SETUP_FINALLY` + `POP_BLOCK` + `END_FINALLY` | 反解为 try 的 finalbody |
| **raise from** | `RAISE_VARARGS(2)` → `raise X from Y` | arg=2 时有 cause |
| **assert** | `LOAD_ASSERT...` | 反解为 `Assert(test, msg)` |
| **AugAssign 增强** | 所有复合运算符 | `i += 1` / `s *= 2` / `x |= y` |

### 16.3 Phase 6 — v3.11+ 反编译（P2）

| 子项 | 内容 | 难点 |
|------|------|------|
| 新操作码 | PUSH_EXC_INFO, PULL_EXC_FROM_INFO, RERAISE, COPY, SWAP, LOAD_LOCALS, SAVE_LOCALS | opcode 值几乎全部重编号 |
| ExceptionTable 解析 | try/except/finally 范围编码 | 需读取 exceptiontable bytes → 解析 entries |
| 无 SETUP_FINALLY | 全用 ExceptionTable | 反编译需从 ExceptionTable 重建 try 块 |
| linetable | 替换 lnotab | 新行号编码格式（per-statement） |
| CACHE 条目 | 指令对齐 | 导致字节码阵列变长，读取时需跳过 |

### 16.4 Phase 7 — 代码查看器增强 + 反编译质量评价（P1）

| 子项 | 内容 | 优先级 | 状态 |
|------|------|--------|:----:|
| A1 | 锁定滚动同步（dis/py 双栏按比例联动） | P1 | 📋 |
| A2 | 行号映射（dis offset → 源码行号） | P1 | 📋 |
| A3 | 失败块灰色背景（TextMarkerService） | P1 | 📋 |
| A4 | 统计面板（块数/成功率/版本） | P1 | 📋 |
| B1 | 有源码质量评价（编译→反编译→AST diff） | P1 | 📋 |
| B2 | 无源码质量评价（反编译→重编译→dis diff） | P1 | 📋 |
| B3 | 多版本质量扫描（同一源码多版本对比） | P1 | 📋 |
| B4 | GUI 质量评价面板（拖放 + 质量报告） | P1 | 📋 |

详见 `docs/plan_phase7.md`。

### 16.5 Phase 8 — 持续完善（长期）

- AST 语义比较 CI 自动化
- 性能优化（大文件/多代码对象）
- Python 2.7 特有操作码全面支持（SLICE+PRINT+EXEC+RAISE in 2.7）
- Python 3.13+ 新特性
- 插件化引擎架构
