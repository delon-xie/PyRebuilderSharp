# Phase 8+ 改进计划 v2.1

> 基于 `docs/improve.md` + `docs/improve_pycdc.md` 分析 + 实际代码审查后的修正计划
> 对比结论：项目已实现 CFG + 支配树 + AST + 版本策略 + 后处理，
> 两篇文档的多数「缺失」指控不准确——改进重点在「已有基础设施上的精准化」

---

## 目录

1. [后支配树 + COME_FROM 结构验证二次校验](#1-后支配树--come_from-结构验证二次校验)
2. [AST/IR — BARE_EXPR 系统性清理 + 表达式折叠增强](#2-astir--bare_expr-系统性清理--表达式折叠增强)
3. [Round-trip compile 验证](#3-round-trip-compile-验证)
4. [COME_FROM 机制增强嵌套结构验证](#4-come_from-机制增强嵌套结构验证)
5. [嵌套 CodeObject 递归反编译增强](#5-嵌套-codeobject-递归反编译增强)
6. [边界精确度 — 研读 uncompyle6/decompyle3 + pycdc](#6-边界精确度--研读-uncompyle6decompyle3--pycdc)
7. [优先级与里程碑](#7-优先级与里程碑)

---

## 1. 后支配树 + COME_FROM 结构验证二次校验

### 1.1 现状

项目**已有**：
- `ControlFlowScanner.ComputeImmediateDominators()` — 前向支配树 ✅
- `ControlFlowScanner.ComputeDominators()` — 完整支配集 ✅
- `ControlFlowScanner.DetectNaturalLoops()` — 自然循环检测 ✅
- SequentialBlock 多轮标注 + 模式目录（28 子模式）✅
- `ControlFlowGraph` + `BasicBlock`（含前驱/后继边）✅

**缺失**：
- 后支配树（Post-Dominator Tree）— 反向图支配分析
- COME_FROM 伪指令 — 跳转目标→原始指令的反向映射
- 结构边界二次校验 — 模式匹配结果与支配分析的交叉验证
- **ExceptionTable → CFG 异常边的严格映射**（来自 improve_pycdc.md，已有 `AnnotateExceptionTableBlocks` 但需更严格）

### 1.2 设计

#### 1.2.1 新增组件

```
PyRebuilderSharp.Core/Scanners/
├── PostDominatorScanner.cs    # 新增 — 后支配树 + COME_FROM
└── StructuralValidator.cs     # 新增 — 结构验证器
```

#### 1.2.2 PostDominatorScanner

```csharp
/// <summary>
/// 后支配树分析 + COME_FROM 集合构建。
/// 
/// 原理：
/// - 将 CFG 反向（反转所有边），在前向支配树算法上跑一次 → 后支配树
/// - 对每个跳转目标指令，在其目标块中构建一个"COME_FROM"映射
/// - 后支配树用于验证：if-elif 链的 else 分支是否确实被 header 后支配
///   try/except 的 handler 是否被 try body 后支配
/// </summary>
public class PostDominatorScanner
{
    private Dictionary<BasicBlock, BasicBlock> _postIdoms = new();
    private Dictionary<BasicBlock, HashSet<BasicBlock>> _postDominance = new();
    private Dictionary<int, List<int>> _comeFrom = new(); // targetOffset → [sourceOffsets]

    /// <summary>
    /// 构建反向 CFG 并计算后支配树。
    /// 反向图 = 所有边取反，以原始 Exit 为入口。
    /// </summary>
    public Dictionary<BasicBlock, BasicBlock> ComputePostDominators(ControlFlowGraph cfg)
    {
        // Step 1: 构建反向 CFG
        var reverseCFG = BuildReverseCFG(cfg);

        // Step 2: 在反向图上运行立即支配树算法（复用 ComputeImmediateDominators 逻辑）
        _postIdoms = ComputeImmediateDominatorsOnGraph(reverseCFG);

        // Step 3: 计算完整后支配集
        _postDominance = ComputePostDominanceSets(cfg);

        return _postIdoms;
    }

    /// <summary>
    /// 构建 COME_FROM 映射。
    /// 对每个跳转指令，记录其目标偏移量←源偏移量。
    /// 
    /// 跳转分类规则（来自 uncompyle6 scanner.py）：
    ///   JUMP_FORWARD / JUMP_ABSOLUTE → 不产生（无条件转发）
    ///   POP_JUMP_IF_FALSE / POP_JUMP_IF_TRUE → 产生（条件汇聚点）
    ///   SETUP_FINALLY / SETUP_EXCEPT → 不产生（异常入口）
    ///   FOR_ITER → 产生（循环出口，区别 for 和 while）
    ///   JUMP_BACKWARD → 不产生（循环回边）
    /// </summary>
    public Dictionary<int, List<int>> BuildComeFromMap(ControlFlowGraph cfg)
    {
        _comeFrom.Clear();
        foreach (var block in cfg.Blocks)
        {
            foreach (var instr in block.Instructions)
            {
                if (!ShouldGenerateComeFrom(instr.Opcode)) continue;
                if (!instr.Argument.HasValue) continue;
                    
                int target = instr.Argument.Value;
                if (!_comeFrom.ContainsKey(target))
                    _comeFrom[target] = new List<int>();
                _comeFrom[target].Add(instr.Offset);
            }
        }
        return _comeFrom;
    }

    /// <summary>
    /// 跳转 → COME_FROM 分类决策。
    /// 这是从 uncompyle6 研读中提取的核心规则。
    /// </summary>
    private bool ShouldGenerateComeFrom(Opcode op) => op switch
    {
        Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
            or Opcode.POP_JUMP_IF_NONE or Opcode.POP_JUMP_IF_NOT_NONE
            or Opcode.FOR_ITER => true,
        // 以下不产生 COME_FROM
        Opcode.JUMP_FORWARD or Opcode.JUMP_ABSOLUTE
            or Opcode.JUMP_BACKWARD or Opcode.SETUP_FINALLY
            or Opcode.SETUP_EXCEPT or Opcode.SETUP_LOOP => false,
        _ => false
    };
}
```

#### 1.2.3 StructuralValidator — 结构验证器

```csharp
/// <summary>
/// 结构验证器 — 在模式目录匹配后，用后支配拓扑进行二次校验。
/// 
/// 校验规则：
/// 
/// R1 [if-elif 链]: 连续 if 的 header A 必须后支配其 else 后继 if B。
///    如果 A 不后支配 B，说明 B 是独立的 if，不是 elif。
///    → 防止 if/elif 误判
/// 
/// R2 [try-except]: except handler 的第一条指令必须被 try body 的最后指令后支配。
///    如果否，该 except 可能不是当前 try 的 handler。
///    → 防止嵌套 try 的 handler 归属错配（EMPTY_TRY 根因之一）
/// 
/// R3 [loop-body]: 回边目标（loop header）必须后支配回边的源（back edge source）。
///    如果否，该回边可能是 break 而非 while 回边。
///    → 防止 while 与 break 误判
/// 
/// R4 [else-body]: if/for/while 的 else 块必须被对应 header 后支配。
///    如果否，else 块实际上是 header 退出后的独立块。
///    → 防止 else 归属错误
/// 
/// R5 [ExceptionTable → CFG 异常边]: ET 条目的 handler 块必须被 ET body 区域后支配。
///    如果否，handler 属于外部 try 而非当前 try。
///    → 防止过度链接（Batch A 根因）
/// </summary>
public class StructuralValidator
{
    public ValidationResult Validate(StructuredCFG stcf, 
        Dictionary<BasicBlock, BasicBlock> postIdoms,
        Dictionary<int, List<int>> comeFrom)
    {
        // 对每个 ControlStructure 应用 R1-R5
        // 返回 FAIL 结构 + 修复建议
    }
}
```

### 1.3 ExceptionTable → CFG 异常边严格映射（pycdc 改进点）

**来自 improve_pycdc.md 的补充**：项目已有的 `AnnotateExceptionTableBlocks` 存在过度链接问题（Phase 2 给每个 Depth==0 的 ET 条目设置 IsTryHeader=true，导致 handler 内部嵌套 try 被当做独立 try）。修复方向：

```csharp
/// Phase 2 AnnotateExceptionTableBlocks 增强：
/// 1. ET 条目的 body 精确到第一个 handler 入口（而非 ET.EndOffset）
/// 2. handler 内的嵌套 ET 条目不产生 IsTryHeader=true（已由外层 try 覆盖）
/// 3. 异常边的深度匹配：backward 扫描 ET Depth 嵌套层次
/// 4. 与后支配树 R5 交叉验证
///
/// 参考 pycdc 的做法：exception table 条目直接生成 CFG 异常边，
/// 不像现在先标注再 ParseControlStructures 模式匹配。
/// 改为在 CFG 构建阶段直接插入异常边（ExceptionHandlers + FinallyBlock），
/// 然后在标注阶段沿用。
```

### 1.4 集成到 Phase 7 流水线

```
现有流水线:
  BuildSequentialBlocks() → 多轮标注 → ParseControlStructures() → [已经匹配]
  
Phase 8 新增:
  CFG Build
    → PostDominatorScanner.ComputePostDominators()   ← 新增
    → PostDominatorScanner.BuildComeFromMap()         ← 新增
    → BuildSequentialBlocks() → 多轮标注 (含 ET 严格映射)
    → ParseControlStructures() → StructuralValidator.Validate()  ← 新增二次校验
    → [修正后的结构]
```

### 1.5 风险与代价

| 项目 | 评估 |
|------|------|
| 实现成本 | 中 (~3天，主要是 PostDominatorScanner + validator) |
| 对全量基线影响 | 低 — 新流程不影响现有 1325/1325 基线 |
| 白盒改善预期 | **+5~10%**（主要 from if-elif 链 + 嵌套 try + ET 严格映射） |
| 退化风险 | 低 — validator 只报错不修复，修完才生效 |

---

## 2. AST/IR — BARE_EXPR 系统性清理 + 表达式折叠增强

### 2.1 现状

现有 BARE_EXPR = **83 例**（README 2026-07-09 基线）。这些是 StackMachine 生成的指令残留表达式，被作为 `ExprStmt` 泄漏到 AST 中。

**来自 improve_pycdc.md 的补充判断**：项目已有 AST 中间表示（`Stmt.cs`+`Expr.cs`+visitor 模式 `PythonCodeGenerator`），因此**问题不在「缺少 AST IR」**，而是**AST 构建完成后残留表达式过多**——这是后处理不充分的问题，不是架构缺失。

分类：

| 分类 | 约数量 | 根因 |
|------|--------|------|
| comprehension 变量泄漏 | ~30 | `LIST_APPEND` / `MAP_ADD` 执行后栈上的 generator 表达式被当独立语句 |
| class 属性初始化泄漏 | ~20 | `STORE_NAME attr` 前的 `LOAD_CONST` 没有被正确消化 |
| match pattern 中间值 | ~15 | match/case 的条件检测指令残留 |
| decorator 表达式泄漏 | ~5 | `MAKE_FUNCTION` + `CALL_FUNCTION` 产生的 intermediate 调用未折叠 |
| f-string 格式说明符残留 | ~3 | FORMAT_ERROR: reprlib 双花括号转义 |
| 其他 | ~10 | 短路条件残留、for-iter 变量 |

### 2.2 设计

#### 2.2.1 新增后处理 pass

`AstBuilder.cs` 中的 `Build()` 流程末尾，在已有 pass 之后追加：

```csharp
// Phase 8: BARE_EXPR 清理
stmts = CleanupBareExpr(stmts);
// Phase 8: 表达式折叠增强（decorator 序列、f-string 格式说明符）
stmts = FoldDecoratorCalls(stmts);
```

#### 2.2.2 BareExprCleaner

```csharp
/// <summary>
/// BARE_EXPR 专用清理器。
/// 
/// 清除规则（来自实际白盒测试 83 例审计）：
///  B1: 列表推导式中 `list.append(value)` → 删除（comprehension 已生成 ListComp AST）
///  B2: 集合推导式中 `set.add(value)` → 删除
///  B3: 字典推导式中 `dict.__setitem__(key, val)` → 删除
///  B4: 纯函数引用 `FunctionRef` → 删除（已成为 FunctionDef）
///  B5: 类体中 `namespace['__qualname__']` → 删除
///  B6: `LOAD_BUILD_CLASS` 产生的 `<function <lambda>>` → 删除
///  B7: match/case guard 中的中间 LOAD_NAME/LOAD_FAST → 与 case body 合并
///  B8: 仅含 Name 的 ExprStmt（孤立变量引用）→ 删除
///  B9: for-iter 循环的 `.__iter__()` 调用残留 → 删除
/// 
/// 安全规则：
///  - 只删除可以明确判定为编译器伪影的表达式
///  - 有副作用的函数调用（print, .write 等）永不删除
///  - 删除时必须同时检测上下文的 If/For/While 结构是否有对应的 AST 节点
///    如果删除后导致空 body，应补 `pass`
/// </summary>
private List<Stmt> CleanupBareExpr(List<Stmt> stmts)
{
    var result = new List<Stmt>(stmts.Count);
    foreach (var stmt in stmts)
    {
        if (stmt is ExprStmt { Value: Call { Func: Attribute { Attr: "append" or "add" } } } 
            && IsInComprehensionContext(stmt, stmts))
        {
            continue; // 删除 B1/B2
        }
        if (stmt is ExprStmt { Value: FunctionRef } funcRef)
        {
            if (funcRef.Value.Name.StartsWith("<"))
                continue; // 删除 B4/B6
        }
        if (HandleMatchPatternBareExpr(stmt, stmts, result))
            continue;
        // ... 其他规则
        result.Add(stmt);
    }
    return result;
}
```

#### 2.2.3 Decorator 表达式折叠（pycdc 改进点）

**来自 improve_pycdc.md**：pycdc 将 `MAKE_FUNCTION` + `CALL_FUNCTION` 折叠为 `@decorator` 语法。项目已通过 `FunctionRef` 初步实现，但 decorator 链（多层 `@A @B @C`）仍可能部分泄漏。

```csharp
/// <summary>
/// 装饰器折叠—将残余的 decorator 函数调用合并到 FunctionDef.Decorators。
/// 
/// 检测模式：
///   src = func(defn)     → 如果 func 是装饰器名，defn 是 FunctionDef => @func
///   src = decorator_A(decorator_B(func_def)) → @A @B C
///   
/// 对每个 FunctionDef 前的连续 ExprStmt(Call(...)) 进行贪婪匹配：
///   - Call 的 Args 必须是 FunctionDef（直接或嵌套）
///   - Call 的 Func 是装饰器名称表达式
/// </summary>
private List<Stmt> FoldDecoratorCalls(List<Stmt> stmts)
{
    // 扫描连续的 f(FunctionDef) 模式
    // 从后向前匹配（最内层 decorator 先执行）
}
```

#### 2.2.4 推导式中间表达式关联

**核心问题**：当前 ListComp/SetComp/DictComp/GeneratorExp AST 节点已存在，但 `ConvertComprehensionCalls` 只在 `FunctionRef` 层面处理。BARE_EXPR 的一部分是 `ConvertComprehensionCalls` 生成了 `ListComp` 节点后，原始的 `LIST_APPEND` loop 体仍然留下了一些残余。

**修复方向**：在 `ConvertComprehensionCalls` 返回后，添加一个清理 pass 来检查：
- 如果某个 `ExprStmt` 的 `.append()` 或 `.add()` 调用与前面已生成的推导式共享同名的目标变量 → 可删除
- 基于变量名匹配的启发式，不需要精确的 def-use 链

### 2.3 验证策略

1. 在白盒测试中新增分类「BARE_EXPR_CHECK」— 标记清理后 BARE_EXPR 数量
2. 用 `--verbose` 模式输出每个清理决策的日志（`[BARE_CLEAN] cause=xxx`）
3. 所有清理决策必须有**可逆证明**（删除的 ExprStmt 不会改变程序语义）

### 2.4 风险与代价

| 项目 | 评估 |
|------|------|
| 实现成本 | 中 (~2.5天，需逐类审计 83 例再编码 + decorator 折叠) |
| 白盒改善预期 | **BARE_EXPR 83 → ~25（-58）**；FORMAT_ERROR 3→0 |
| 退化风险 | **高** — 误删语义性表达式会导致 SYNTAX_ERROR 或语义错误 |
| 缓解措施 | 只删可明确判定为伪影的 3 类；其余推迟到更精准的分析 |

---

## 3. Round-trip compile 验证

### 3.1 现状

已有：
- `PycdcSuiteRunner` — token 级语义比较（细致，但不是语法校验）
- 白盒测试 405 例 — 包含编译→反编译→diff 验证

**缺失**：
- 反编译后 `compile(source, '<decomp>', 'exec')` 语法有效性检查
- CPython 版本兼容性验证（生成代码在目标 Python 版本上是否能执行）

### 3.2 设计

#### 3.2.1 语法验证器

```csharp
// Testing/CompileVerifier.cs
public static class CompileVerifier
{
    /// <summary>
    /// 验证反编译输出的 Python 源代码是否能被 CPython 正确解析。
    /// 使用子进程调用匹配版本的 Python。
    /// 
    /// 三种模式：
    ///   1. ast.parse — 仅检查语法树是否有效（最轻量）
    ///   2. compile — 检查是否能编译为字节码（中级）
    ///   3. execute — 实际执行并检查运行时错误（最重量）
    /// </summary>
    public static CompileResult VerifySyntax(string source, PythonVersion version)
    {
        // 方式 A: 通过子进程调用 python3 -c "compile(...)"
        //   echo source | python3 -c "
        //   import sys, ast
        //   code = sys.stdin.read()
        //   try:
        //       ast.parse(code)
        //       print('PASS')
        //   except SyntaxError as e:
        //       print(f'FAIL:{e.lineno}:{e.msg}')
        //   "
    }

    /// <summary>
    /// 版本匹配的 compile 检查。
    /// 使用 pyenv 获取对应版本的 Python 解释器。
    /// 3.5 的 Python 无法编译 3.10 格式的 f-string。
    /// </summary>
    public static CompileResult VerifyWithVersion(string source, PythonVersion targetVersion)
    {
        var pyBin = ResolvePyenvBinary(targetVersion);
        // 子进程调用
    }
}
```

#### 3.2.2 集成到 PycdcSuiteRunner

在 `PycdcSuiteRunner.RunTestCase` 的 token 比较之后追加：

```csharp
// Phase 8 新增: compile 验证
if (options.EnableCompileVerification)
{
    var compiled = CompileVerifier.VerifySyntax(generatedSource, pyVersion);
    if (!compiled.IsValid)
    {
        testResult.Decorations.Add(
            $"SYNTAX_WARN: {compiled.ErrorMessage}");
    }
}
```

#### 3.2.3 CLI 选项

```bash
# 默认关闭（compile 验证需要 Python 解释器，增加 CI 依赖）
pyrebuilder test --verify-compile
# 或
pyrebuilder test --compile-version 3.12
```

### 3.3 实现策略

| 阶段 | 内容 | 依赖 |
|------|------|------|
| 1 | `ast.parse()` 子进程调用（仅验证语法树） | 当前 Python 版本即可 |
| 2 | 版本匹配的 compile（需要 pyenv 安装对应版本） | 安装工具链 |
| 3 | CI 集成（每个 PR 自动验证） | GitHub Actions + pyenv |

### 3.4 风险与代价

| 项目 | 评估 |
|------|------|
| 实现成本 | **低** (~0.5天，ast.parse 模式极其简单) |
| 价值 | ⭐⭐ — 发现隐蔽缩进/括号/冒号问题 |
| 退化风险 | **低** — 验证器只报告不修改 |
| 注意 | 需要确认 CI 环境安装了 Python 解释器 |

---

## 4. COME_FROM 机制增强嵌套结构验证

### 4.1 COME_FROM 概念详解

uncompyle6/decompyle3 的核心创新在于**在反编译过程中合成 `COME_FROM` 伪指令**：

```
原始字节码:              反编译视角:
  0x10 LOAD_FAST x        0x10 LOAD_FAST x
  0x12 LOAD_CONST 0        0x12 LOAD_CONST 0
  0x14 COMPARE_OP ==       0x14 COMPARE_OP ==
  0x16 POP_JUMP_IF_FALSE  ══╗→ 0x22 ←目标
  0x18 LOAD_CONST 'hi'       │   0x22 COME_FROM(0x16)  ← 伪指令
  0x20 RETURN_VALUE          │   0x24 ...
                              ╚══ (跳转是从 0x16 过来的)
```

COME_FROM 让反编译器在遍历 AST 时能够回答一个关键问题：**"正在解析的字节码位置，有哪些控制流路径汇聚到了这里？"**

### 4.2 uncompyle6 的 COME_FROM 实现原理

```python
# uncompyle6/scanner.py (简化示意)
class Scanner:
    def build_come_from(self, bytecode):
        """
        扫描所有跳转指令，为每个目标偏移量记录源偏移量。
        
        关键设计决策：
        1. 无条件跳转（JUMP_FORWARD, JUMP_ABSOLUTE）→ 目标不是 COME_FROM
           （无条件跳转的目标在控制流中不是"汇聚点"，而是"转发点"）
        2. 条件跳转（POP_JUMP_IF_FALSE, POP_JUMP_IF_TRUE）→ 目标是 COME_FROM
           （条件跳转的目标是条件分支的汇聚点）
        3. SETUP_FINALLY → 目标不是 COME_FROM（是 try body 的异常入口）
        4. FOR_ITER → 是（是 for 循环出口，用于区别 for 和 while 循环）
        """
        pass

    def is_come_from(self, offset):
        """检查某个偏移量是否是一个 COME_FROM 目标。"""
        return offset in self._come_froms
```

### 4.3 在 PyRebuilderSharp 中的适配设计

项目已有 SequentialBlock + 模式目录，COME_FROM 作为**标注层**的补充：

```csharp
/// <summary>
/// ComeFromAnnotator — Phase 2d (在 Phase 2c HandlerDepth 之后)。
/// 
/// 为每个 SequentialBlock 标注 COME_FROM 来源信息。
/// 
/// 标注数据结构：
///   SequentialBlock.ComeFromSources: List<ComeFromSource>
///   ComeFromSource = { SourceBlockId: int, SourceOffset: int, JumpType: ComeFromType }
///   
/// ComeFromType 枚举：
///   CJump_True   — POP_JUMP_IF_TRUE 跳转目标
///   CJump_False  — POP_JUMP_IF_FALSE 跳转目标
///   CJump_Short  — JUMP_IF_TRUE_OR_POP / JUMP_IF_FALSE_OR_POP (短跳)
///   CExcept      — ExceptionTable handler 目标 (3.11+)
///   CSetFinally  — SETUP_FINALLY handler 目标 (3.10-)
///   CForEnd      — FOR_ITER 出口目标
/// </summary>
public class ComeFromAnnotator
{
    public void AnnotateComeFrom(List<SequentialBlock> seqBlocks, ControlFlowGraph cfg)
    {
        // 1. 收集所有跳转指令 → 目标偏移量映射
        var jumpTargets = new Dictionary<int, List<ComeFromSource>>();
        
        foreach (var block in cfg.Blocks)
        {
            foreach (var instr in block.Instructions)
            {
                if (!TryGetComeFromType(instr.Opcode, out var cfType)) 
                    continue;
                if (!instr.Argument.HasValue) 
                    continue;
                    
                int target = instr.Argument.Value;
                if (!jumpTargets.ContainsKey(target))
                    jumpTargets[target] = new List<ComeFromSource>();
                jumpTargets[target].Add(new ComeFromSource(block.Id, instr.Offset, cfType));
            }
        }
        
        // 2. 将 COME_FROM 信息挂到对应的 SequentialBlock 上
        foreach (var seq in seqBlocks)
        {
            if (jumpTargets.TryGetValue(seq.StartOffset, out var sources))
            {
                seq.ComeFromSources.AddRange(sources);
            }
        }
    }
}
```

### 4.4 COME_FROM 用于结构验证的场景

#### 场景 1: if-elif 链验证

```
源 Python: 
  if a: ...
  elif b: ...
  else: ...
  
字节码（简化）:
  0x00 LOAD_FAST a
  0x02 POP_JUMP_IF_FALSE → 0x0A  ──┐ if false → elif
  0x04 LOAD_FAST b                    │
  0x06 POP_JUMP_IF_FALSE → 0x10   ──┤ if false → else
  0x08 JUMP_FORWARD → 0x12       ──┐ │ if-true → end
  0x0A ...elif body...              │ │
  0x0C JUMP_FORWARD → 0x12       ──┤ │ elif-true → end
  0x10 ...else body...              │ │
  0x12 COME_FROM(0x08, 0x0C) ←─────┘─┘ ← 两个汇聚点
```

COME_FROM(0x08, 0x0C) 表示块 0x12 有两个来源：0x08 和 0x0C。如果模式匹配把这 3 个分支识别为嵌套 if 而非 elif 链，COME_FROM 会暴露矛盾 → 3 个分支汇聚到同一出口，应该是 elif。

#### 场景 2: try-except 嵌套层级验证

```
源 Python:
  try:
      try:
          ...
      except A:
          ...
  except B:
      ...

COME_FROM 分析:
  - handler A 的入口：COME_FROM(CExcept, depth=1)
  - handler B 的入口：COME_FROM(CExcept, depth=0)
  - 如果深度分析将 A 的 handler 也标记为 depth=0 → COME_FROM 发现 B 的两个来源
    (外界和 A 内部) 都指向同一个 handler → 验证失败
```

#### 场景 3: while 循环 vs for 循环

```
while 模式:
  LOAD_FAST x
  POP_JUMP_IF_FALSE → exit
  [body]
  JUMP_ABSOLUTE → header
  exit: COME_FROM(header + fallthrough)
  
for 模式:
  GET_ITER
  FOR_ITER → exit
  [body]
  JUMP_ABSOLUTE → FOR_ITER
  exit: COME_FROM(FOR_ITER)
```

COME_FROM(FOR_ITER) ≠ COME_FROM(条件跳转) 可以区分 for 和 while。

### 4.5 集成到 Annotation 流水线

```
Phase 1:  MergeLinearChain
Phase 2:  AnnotateExceptionTableBlocks (增强：ET→CFG 严格映射)
Phase 2a: AnnotateMatchBlocks
Phase 2b: AnnotateForWhileSubtypes
Phase 2c: AnnotateHandlerDepths
Phase 2d: AnnotateComeFrom               ← 新增
Phase 3:  AnnotateSequentialBlock
Phase 3b: AnnotateMergePointsAndExits
Phase 4:  AnnotateBackEdges

ParseControlStructures:
  - StructuralValidator.ConsultComeFrom() ← 新增：在模式匹配时咨询 COME_FROM
  二次校验:
  - StructuralValidator.Validate() + postIdoms ← 新增：R1-R5 验证
```

### 4.6 风险与代价

| 项目 | 评估 |
|------|------|
| 实现成本 | 中 (~3天: COME_FROM annotator + validator 规则) |
| 白盒改善预期 | **+3~5%**（主要解决嵌套 try 归属 + if-elif 链） |
| 与现有架构集成 | 低 — Annotation 流水线已有扩展点（Phase 2a/2b/2c） |
| 测试策略 | 新增 COME_FROM 单元测试 + 白盒回归 |

---

## 5. 嵌套 CodeObject 递归反编译增强

### 5.1 现状

**来自 improve_pycdc.md 的补充**：pycdc 对 `co_consts` 中嵌套的 `PyCodeObject` 递归调用 `BuildFromCode()`，完整恢复嵌套 `def` / `lambda` / 推导式。

项目已有：
- `PostProcessFunctionDefs` — 处理 FunctionDef/ClassDef body 的反编译 ✅
- `ConvertChildCodesToFunctionDefs` — 基于偏移的 fallback 匹配 ✅
- `ConvertComprehensionCalls` — 推导式代码对象转 ListComp/DictComp 等 ✅

**但**：`ConvertChildCodesToFunctionDefs` 是**扁平匹配**（按偏移量位置匹配 child codes 与 stmts），不是**递归构建**。当 child code 嵌套深度超过 2 层时（例如：函数内嵌 lambda 内嵌推导式），扁平匹配可能错位。

### 5.2 设计

```csharp
/// <summary>
/// 增强后的递归嵌套代码对象反编译。
/// 
/// 原: ConvertChildCodesToFunctionDefs — 扁平偏移匹配
/// 新: DecompileNestedCodeObjects — 递归构建
/// 
/// 流程：
///   1. Build() 对顶层模块生成 stmts
///   2. 扫描 stmts 中的 FunctionDef/ClassDef
///   3. 对每个 child code object（在 co_consts 中）：
///      a. 检查对应的 FunctionDef 是否已正确处理（有非空 body）
///      b. 如果否，使用 child code 的 own code object 重新调用 Build()
///      c. 替换或合并结果
///   4. 递归处理 FunctionDef body 中的嵌套 FunctionDef
/// 
/// 触发条件：
///   - FunctionDef.Body 仅含 CommentBlock 或 pass → ChildCode 未正确反编译
///   - ClassDef.Body 不能包含 LOAD_CONST+MAKE_FUNCTION 模式（代码对象未展开）
///   
/// 安全约束：
///   - 递归深度 ≤ 10（防止无限递归）
///   - 每个 code object 只处理一次（按 name 去重）
/// </summary>
private List<Stmt> DecompileNestedCodeObjects(List<Stmt> stmts, CodeObject parentCode)
{
    // 收集 parentCode.ChildCodes 中尚未正确展开的 code object
    // 对每个 child，从 co_consts 获取实际 Bytecode.CodeObject
    // 调用 Decompiler.DecompileCodeObject(childCode) 递归
    // 合并结果到父 stmts
}
```

### 5.3 集成到 Build() 流程

```
Build() 现有末尾:
  stmts = PostProcessFunctionDefs(stmts);
  stmts = ConvertChildCodesToFunctionDefs(stmts);
  stmts = ConvertComprehensionCalls(stmts);
  
Phase 8 增强:
  stmts = PostProcessFunctionDefs(stmts);
  stmts = DecompileNestedCodeObjects(stmts, _codeObject);   ← 新增
  stmts = ConvertChildCodesToFunctionDefs(stmts);            // fallback
  stmts = ConvertComprehensionCalls(stmts);
```

### 5.4 风险与代价

| 项目 | 评估 |
|------|------|
| 实现成本 | 中 (~2天: 递归构建 + 去重 + 深度保护) |
| 白盒改善预期 | **+2~3%**（主要影响闭包/嵌套 lambda/推导式） |
| 退化风险 | **中** — 递归调用 Build() 可能改变现有 stmts 语义 |
| 缓解措施 | 递归仅在 FunctionDef.Body 为空时触发 |

---

## 6. 边界精确度 — 研读 uncompyle6/decompyle3 + pycdc

### 6.1 目标

| 研读目标 | 来源 | 具体产出 |
|---------|------|---------|
| COME_FROM 构建算法 | uncompyle6 `scanner.py` | 跳转类型的精确分类（哪些跳转产生 COME_FROM） |
| 后支配树 + CFG 结构还原 | uncompyle6 `scan.py` | dominator tree 在 try/while/for 边界判定中的用法 |
| 异常表结构判定 | **pycdc** `ASTree.cpp` | Python 3.11+ exception table 如何映射到 try-except-finally |
| 推导式反编译 | uncompyle6 `scanner.py` LIST_APPEND | `LIST_APPEND` 模式如何映射到 `ListComp` |
| 装饰器还原 | **pycdc** `ASTree.cpp` BuildFromCode | `MAKE_FUNCTION` + `CALL_FUNCTION` 识别为 `@decorator` |
| 嵌套 CodeObject 递归 | **pycdc** `ASTree.cpp` | 如何递归调用 BuildFromCode 处理闭包/嵌套函数 |
| 死代码消除 | uncompyle6 `semantics/` | 什么情况下可以安全地删除 unreachable code |

### 6.2 研读计划

#### 6.2.1 克隆目标代码仓库

```bash
# uncompyle6 — 最成熟的反编译器，Python 2.4~3.8
git clone https://github.com/rocky/python-uncompyle6.git ref/uncompyle6/

# decompyle3 — uncompyle6 的分支，聚焦 Python 3.7-3.8+
git clone https://github.com/rocky/python-decompyle3.git ref/decompyle3/

# pycdc — C++ 反编译器，聚焦 3.11+ exception table + CodeObject 递归
# 项目已有 ref/pycdc/（由 CMake 构建）
# 重点读：src/ASTree.cpp, src/bytecode.cpp
```

#### 6.2.2 关键文件对应表

| 源文件 | 项目 | 功能 | 对应 PyRebuilderSharp 模块 | 优先级 |
|--------|------|------|---------------------------|--------|
| `scanner.py` | uncompyle6 | 字节码扫描 + COME_FROM + 指令分类 | `Scanners/` | **P0** |
| `scan.py` | uncompyle6 | 语义扫描 + 条件跳转分析 | `Scanners/ControlFlowScanner.cs` | **P0** |
| `ASTree.cpp` | pycdc | AST 构建 + 表达式折叠 + CodeObject 递归 | `Builders/AstBuilder.cs` | **P0** |
| `bytecode.cpp` | pycdc | 字节码版本解析 | `Versioning/VersionStrategy*.cs` | **P1** |
| `parsers/parser.py` | uncompyle6 | 语法规则引擎 + reduce | `Builders/SequentialBlockBuilder.cs` | **P1** |
| `skeleton.py` | uncompyle6 | AST 结构骨架 | `Builders/AstBuilder.cs` | **P1** |
| `semantics/` | uncompyle6 | 语义规则（if/while/for/try） | `Builders/` 结构构建 | **P1** |
| `decompyle.py` | uncompyle6 | 主流程入口 | `Decompiler.cs` | **P2** |
| `code.py` | uncompyle6 | CodeType 对象模型 | `Models/Bytecode/CodeObject.cs` | **P2** |

### 6.3 研读产出物要求

每次研读完成后，产出：

```markdown
# 研读记录: [主题]

## 来源
- 文件: `uncompyle6/scanner.py:150-220`
- 对应 PyRebuilderSharp: `Scanners/PostDominatorScanner.cs`

## 核心发现
### 1. 关键算法
（源码片段 + 注释）

### 2. 设计决策
（为什么这样设计，权衡了什么）

### 3. 在 PyRebuilderSharp 中的应用
（具体改动方案：新增/修改哪些文件，如何修改）
```

### 6.4 研读顺序（建议）

| 顺序 | 文件/模块 | 来源 | 期望解决的白盒问题 | 预计耗时 |
|------|----------|------|-------------------|---------|
| 1 | `scanner.py` COME_FROM | uncompyle6 | EMPTY_TRY 边界 + if-elif 链 | 2 小时 |
| 2 | `ASTree.cpp` BuildFromCode | **pycdc** | 嵌套 CodeObject 递归 + decorator 折叠 | 2 小时 |
| 3 | `semantics/` try/finally | uncompyle6 | TRY_NO_HANDLER | 2 小时 |
| 4 | `scanner.py` LIST_APPEND | uncompyle6 | BARE_EXPR (comprehension) | 1 小时 |
| 5 | `ASTree.cpp` exception table | **pycdc** | ET→CFG 严格映射 | 1 小时 |
| 6 | `decompyle.py` MAKE_FUNCTION | uncompyle6 | decorator 序列 | 1 小时 |
| 7 | `semantics/` match/case | uncompyle6 (dev) | match 模式还原 | 1 小时 |

### 6.5 风险与代价

| 项目 | 评估 |
|------|------|
| 研读成本 | 中 (~10 小时总阅读时间，分 7 次，含 pycdc 2 次) |
| 直接产出 | 7 份研读记录 + 对应代码改动 |
| 落地效果 | 间接改善（不直接改代码，但指导后续 fix） |
| 最佳实践 | 研读后立即动手实现，避免纸上谈兵 |

---

## 7. 优先级与里程碑

### 7.1 改进路线图

```
Phase 8 (本改进计划，预计 2 周)
├── 8.0 研读（7 次，共 ~10h）
│   ├── 8.0.1 uncompyle6 COME_FROM (2h)
│   ├── 8.0.2 pycdc ASTree.cpp (2h)
│   ├── 8.0.3 uncompyle6 try/finally semantics (2h)
│   ├── 8.0.4 uncompyle6 LIST_APPEND (1h)
│   ├── 8.0.5 pycdc exception table (1h)
│   └── 8.0.6-7 decorator / match (2h)
│
├── 8.1 Round-trip compile 验证 (~0.5天)
│   └── CompileVerifier.cs + PycdcSuiteRunner 集成
│
├── 8.2 BARE_EXPR 系统性清理 + 表达式折叠 (~2.5天)
│   ├── 分类审计 83 例 (基于 8.0.4 LIST_APPEND 研读)
│   ├── CleanupBareExpr pass
│   ├── FoldDecoratorCalls pass
│   └── 白盒回归验证
│
├── 8.3 后支配树 + COME_FROM 结构验证 (~3天)
│   ├── PostDominatorScanner.cs (基于 8.0.1 研读)
│   ├── ComeFromAnnotator.cs (Phase 2d)
│   └── StructuralValidator.cs
│
├── 8.4 COME_FROM 增强嵌套结构验证 (~3天)
│   └── Validation R1-R5 规则实现 + 白盒回归
│
└── 8.5 嵌套 CodeObject 递归 + ET 严格映射 (~2天)
    ├── DecompileNestedCodeObjects (基于 8.0.2 pycdc 研读)
    └── ET→CFG 异常边增强 (基于 8.0.5 研读)

Phase 9+ (延续)
├── 9.0 EMPTY_TRY 边界批量化修复 (Batch A)
├── 9.1 TRY_NO_HANDLER 修复 (Batch B)
└── 9.2 REDUNDANT_PASS/RAISE/RETURN 清洗
```

### 7.2 预期收益

| 阶段 | 改善点 | 预期基线 | 白盒通过率 |
|------|--------|---------|-----------|
| 当前 | — | 1325/1325 ✅ | 73% (298/405) |
| 8.1 | compile 验证 + 发现隐蔽语法问题 | 1325/1325 ✅ | 73% → 73% (发现若干 SYNTAX_WARN) |
| 8.2 | BARE_EXPR 55→25, FORMAT_ERROR 3→0 | 1325/1325 ✅ | 73% → **78%** |
| 8.3 | 嵌套 try/if-elif 边界 | 1325/1325 ✅ | 78% → **82%** |
| 8.4 | COME_FROM 增强嵌套验证 | 1325/1325 ✅ | 82% → **85%** |
| 8.5 | 闭包/嵌套 lambda/decorator 序列 | 1325/1325 ✅ | 85% → **87%** |

### 7.3 风险登记册

| # | 风险 | 概率 | 影响 | 缓解措施 |
|---|------|------|------|---------|
| 1 | BARE_EXPR 清理误删语义表达式 | 中 | 高 | 只清理可明确判定的 3 类；保留脆弱项 |
| 2 | COME_FROM 标注增加编译时间 | 低 | 低 | Phase 2d 是线性扫描，O(N) |
| 3 | 后支配树与模式目录结果矛盾 | 中 | 中 | 验证器先报错不修复，手动评估 |
| 4 | uncompyle6 代码过时（3.8 停止更新） | 高 | 低 | 只借鉴设计理念，不复制代码 |
| 5 | compile 验证需要 Python 解释器 | 低 | 中 | 可选的 CI 步骤，默认关闭 |
| 6 | **pycdc ASTree.cpp 递归深度过大** | 中 | 低 | 设置最大递归深度 = 10 |
| 7 | **ET→CFG 严格映射破坏全量基线** | 低 | 高 | 逐步切换：先新路径，验证通过再切默认 |

---

> **文档版本**: v2.1
> **编写日期**: 2026-07-10
> **状态**: 草稿 — 待评审
> 
> **与 v2.0 的差异**:
> - 合并 `improve_pycdc.md` 分析 → 新增「章节 5: 嵌套 CodeObject 递归反编译增强」
> - 扩充「章节 2」增加 decorator 表达式折叠 + f-string 格式说明符
> - 扩充「章节 1/4」增加 ET→CFG 异常边严格映射
> - 扩充「章节 6」增加 pycdc `ASTree.cpp` 研读条目（2 次）
> - 扩充研读产出物格式 + 顺序表
> - 更新路线图：8.5 + Phase 9+ 延续
> - 新增风险 #6-#7
> 
> **下一步**:
> 1. 立即启动研读 uncompyle6 COME_FROM 算法
> 2. 同时启动 pycdc ASTree.cpp 递归 CodeObject 阅读
> 3. 编写 CompileVerifier.cs（~0.5天）
> 4. 分类审计 83 例 BARE_EXPR 的实际根因
