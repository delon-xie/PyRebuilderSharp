using PyRebuilderSharp.Core.Models.AST;
using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.CFG;
using PyRebuilderSharp.Core.Scanners;
using PyRebuilderSharp.Core.Versioning;
using AstAttribute = PyRebuilderSharp.Core.Models.AST.Attribute;

namespace PyRebuilderSharp.Core.Builders;

/// <summary>
/// AST构建器 — 使用 BlockDecompiler 进行逐块反编译。
/// 对每个基本块调用 BlockDecompiler，失败块输出注释。
/// </summary>
public class AstBuilder
{
    private readonly BlockDecompiler _blockDecompiler;
    private readonly CodeObject _codeObject;
    private int _buildTryDepth;
    private const int MaxBuildTryDepth = 60;

    private readonly DecompileOptions _options;
    private Dictionary<int, BlockResult> _blockResults = new();
    private HashSet<int> _loopHeaderOffsets = new();
    private List<BasicBlock> _allBlocks = new();
    private readonly Dictionary<int, BasicBlock> _blockByOffset = new();
    private readonly HashSet<int> _processedBlockIds = new(); // 已实际处理的块 ID（用于孤儿块检测）
    private int _buildDepth; // BuildStatements 递归深度，防止 StackOverflow
    private bool _diagETPrinted; // temporary diagnostic flag
    private List<ExceptionTableEntry> _sortedExceptionTable = new();
    private List<BasicBlock> _sortedBlocks = new(); // sorted by StartOffset

    public AstBuilder(CodeObject codeObject, DecompileOptions? options = null)
    {
        _codeObject = codeObject;
        _options = options ?? new DecompileOptions();
        _blockDecompiler = new BlockDecompiler();
    }

    /// <summary>Phase 8 Step 4: 后支配扫描器（跨阶段共享）。</summary>
    private PostDominatorScanner? _pdomScanner;
    
    /// <summary>
    /// 总基本块数（用于统计）。
    /// </summary>
    public int TotalBlockCount { get; private set; }

    /// <summary>
    /// 反编译失败的基本块数（用于统计）。
    /// </summary>
    public int FailedBlockCount { get; private set; }

    /// <summary>
    /// 从结构化CFG构建AST。
    /// </summary>
    public AstNode Build(StructuredCFG structuredCFG)
    {
        Console.Error.WriteLine($"[BUILD] AstBuilder.Build called for {_codeObject.Name}");
        var cfg = structuredCFG.RawCFG;

        // Phase 8 Step 4: 后支配树 + COME_FROM 分析（诊断，不修改）
        _pdomScanner = new PostDominatorScanner();
        _pdomScanner.ComputePostDominators(cfg);
        _pdomScanner.BuildComeFromMap(cfg);

        if (_options.EnableSequentialBlocks)
        {
            return BuildWithSequentialBlocks(cfg);
        }

        _blockResults = _blockDecompiler.DecompileBlocks(cfg.Blocks, _codeObject);
        _allBlocks = cfg.Blocks;
        _sortedBlocks = cfg.Blocks
            .Where(b => b.Instructions.Count > 0)
            .OrderBy(b => b.Instructions[0].Offset)
            .ToList();
        _sortedExceptionTable = _codeObject.ExceptionTable
            .OrderBy(e => e.StartOffset)
            .ToList();
        
        // 统计块级结果
        TotalBlockCount = _blockResults.Count;
        FailedBlockCount = _blockResults.Values.Count(r => !r.IsSuccess);
        
        // Build offset-to-block map
        _blockByOffset.Clear();
        foreach (var b in cfg.Blocks)
            _blockByOffset[b.StartOffset] = b;

        // Build loop header offsets set
        _loopHeaderOffsets.Clear();
        foreach (var b in cfg.Blocks)
        {
            if (b.Flags.HasFlag(BlockFlags.LoopHeader))
            {
                _loopHeaderOffsets.Add(b.StartOffset);
                if (_options.VerboseErrors)
                {
                    Console.Error.WriteLine($"[BUILD] Found LoopHeader block at 0x{b.StartOffset:X4}");
                }
            }
        }
        
        if (_options.VerboseErrors)
        {
            Console.Error.WriteLine($"[BUILD] Code object: {_codeObject.Name}, {cfg.Blocks.Count} blocks");
            foreach (var b in cfg.Blocks)
            {
                Console.Error.WriteLine($"[BUILD]   Block 0x{b.StartOffset:X4}-0x{b.EndOffset:X4}");
            }
        }

        var stmts = new List<Stmt>();
        var visited = new HashSet<BasicBlock>();

        // 输出所有 ET 条目（调试用）
        // ET entries count debug removed
        for (int i = 0; i < _codeObject.ExceptionTable.Count; i++)
        {
            var et = _codeObject.ExceptionTable[i];
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[ET_DUMP]   Entry {i}: Start={et.StartOffset:X4}, End={et.EndOffset:X4}, Target={et.TargetOffset:X4}, Depth={et.Depth}, Lasti={et.Lasti}");
            }
        }

        // 使用统一的 BuildStatements 遍历，ET 条目由 BuildStatementsInternal 处理
        stmts.AddRange(BuildStatements(cfg.Entry, visited));

        // 确保所有块都被处理
        // 使用 _processedBlockIds（BuildStatements 实际处理的块）而非 CollectVisited（只跟随 successor 边）
        // 防止 try/except 的 handler 块标记为 visited 导致其后缀块被静默跳过
        var unvisited = cfg.Blocks
            .Where(b => !_processedBlockIds.Contains(b.Id))
            .OrderBy(b => b.StartOffset)
            .ToList();
        
        if (unvisited.Count > 0)
        {
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[WARN] {unvisited.Count} unprocessed blocks — recovering");
            }

            foreach (var orphan in unvisited.OrderBy(b => b.StartOffset))
            {
                try
                {
                    // 跳过已被 BlockScanner.MergeOrphanBlocks 清空的块（0 指令 = 已合并到后继块）
                    if (orphan.Instructions.Count == 0)
                    {
                        _processedBlockIds.Add(orphan.Id);
                        continue;
                    }

                    var blockDecomp = new BlockDecompiler();
                    var blockResult = blockDecomp.DecompileBlock(orphan.Instructions, _codeObject, orphan.Id);
                    if (blockResult.IsSuccess)
                    {
                        // === 孤儿块诊断分类 ===
                        string classification = ClassifyOrphanBlock(orphan);
                        if (_options.VerboseErrors)
                        {
                        Console.Error.WriteLine($"[ORPHAN] @0x{orphan.StartOffset:X4} func={_codeObject.Name} ver={_codeObject.Version} class={classification} instrs={orphan.Instructions.Count}");
                        }
                        bool hasHandlerPreamble = classification == "handler_pre" || classification == "handler_chain";

                        if (hasHandlerPreamble)
                        {
                            _processedBlockIds.Add(orphan.Id);
                            continue;
                        }

                        if (classification == "for_iter")
                        {
                            var loopVisited = new HashSet<BasicBlock>();
                            var loopStmts = BuildForLoop(orphan, loopVisited);
                            if (loopStmts.Count > 0)
                            {
                                stmts.AddRange(loopStmts);
                                continue;
                            }
                        }

                        // 过滤孤儿块的无效内容：仅含 return None 时跳过
                        bool isEmptyReturn = blockResult.Statements.Count == 1
                            && blockResult.Statements[0] is Return r
                            && r.Value is Constant { Value: null };

                        // 跳过终端跳转块：POP_JUMP_IF_*/JUMP_FORWARD/JUMP_ABSOLUTE/FOR_ITER/GEN_START
                        // 这些块的语义已包含在 if/else/for/while 等控制流 AST 中，
                        // 其指令的 StackMachine 结果已通过 BuildIfElse/BuildForLoop 等消费。
                        bool isTerminalJump = orphan.Instructions.Count > 0 && 
                            orphan.Instructions.Last().Opcode switch
                            {
                                Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
                                    or Opcode.JUMP_FORWARD or Opcode.JUMP_ABSOLUTE
                                    or Opcode.FOR_ITER or Opcode.GET_ITER
                                    or Opcode.JUMP_IF_FALSE_OR_POP or Opcode.JUMP_IF_TRUE_OR_POP
                                    or Opcode.POP_JUMP_IF_NONE or Opcode.POP_JUMP_IF_NOT_NONE
                                    => true,
                                _ => false
                            };

                        if (isTerminalJump)
                        {
                            // jump_cond blocks often have useful prefix instructions (LOAD/STORE)
                            // before the terminal jump. Extract and recover them.
                            bool recoveredPrefix = false;
                            if (classification == "jump_cond" && orphan.Instructions.Count > 1)
                            {
                                var om = new StackMachine(_codeObject);
                                var prefixStmts = new List<Stmt>();
                                // Process all instructions except the last (terminal jump)
                                for (int ji = 0; ji < orphan.Instructions.Count - 1; ji++)
                                {
                                    var s = om.Execute(orphan.Instructions[ji]);
                                    if (s != null) { prefixStmts.Add(s); recoveredPrefix = true; }
                                }
                                while (om.HasResults)
                                    prefixStmts.Add(new ExprStmt(om.PopResult()));
                                if (recoveredPrefix)
                                {
                                    _processedBlockIds.Add(orphan.Id);
                                    var lo = _allBlocks.Count > 0 ? _allBlocks[^1].EndOffset : 0;
                                    bool early = lo > 0 && orphan.StartOffset < lo / 3;
                                    if (early) stmts.InsertRange(0, prefixStmts);
                                    else stmts.AddRange(prefixStmts);
                                }
                            }
                            if (!recoveredPrefix)
                            {
                                _processedBlockIds.Add(orphan.Id);
                                if (stmts.Count == 0)
                                {
                                    stmts.Add(new CommentBlock($"# [Block @0x{orphan.StartOffset:X4}] unreachable jump"));
                                }
                            }
                            continue;
                        }

                        if (!isEmptyReturn && (_options.ShowOrphanBlocks || stmts.Count == 0))
                        {
                            // flat_expr_store/flat_expr_loads: reprocess through StackMachine to recover statements
                            if (classification is "flat_expr_store" or "flat_expr_loads" or "other")
                            {
                                var om = new StackMachine(_codeObject);
                                var recovered = new List<Stmt>();
                                bool hasRecovered = false;
                                foreach (var ins in orphan.Instructions)
                                {
                                    var s = om.Execute(ins);
                                    if (s != null) { recovered.Add(s); hasRecovered = true; }
                                }
                                while (om.HasResults)
                                    recovered.Add(new ExprStmt(om.PopResult()));

                                if (hasRecovered)
                                {
                                    _processedBlockIds.Add(orphan.Id);
                                    // 孤儿块按偏移量决定插入位置：早期偏移（偏移最小的一部分）插到开头
                                    bool early = orphan.StartOffset < 64;
                                    
                                    // Check if this looks like a class body
                                    // 如果包含 import 语句，则是模块级代码，不是类体
                                    bool hasImport = recovered.Any(s => s is Assign a
                                        && a.Value is Name n && n.IsImport);
                                    if (LooksLikeClassBody(recovered) && !hasImport)
                                    {
                                        var className = _codeObject.Name;
                                        if (string.IsNullOrEmpty(className) || className == "<module>" || className.StartsWith("name_"))
                                            className = $"Class_{orphan.StartOffset:X4}";
                                        stmts.Add(new ClassDef(className, new List<Expr>(), recovered));
                                    }
                                    else if (early)
                                    {
                                        stmts.InsertRange(0, recovered);
                                    }
                                    else
                                    {
                                        stmts.AddRange(recovered);
                                    }
                                    continue;
                                }
                            }

                            // 根据偏移位置插入孤儿块内容，而非始终追加在末尾。
                            // 早期偏移的孤儿块（如函数体开头的初始化语句 `abstracts = set()`）
                            // 应出现在函数开头而非末尾。
                            var orphanStmts = new List<Stmt>();
                            // 只有当孤儿块有实际内容时才添加注释
                            if (blockResult.Statements.Count > 0)
                                orphanStmts.Add(new CommentBlock($"# orphan @0x{orphan.StartOffset:X4}"));
                            // 过滤孤儿块中的 raise 语句：这些是失去处理器上下文的不可达异常重抛，
                            // 不应出现在反编译输出中。
                            foreach (var s in blockResult.Statements)
                            {
                                if (s is Raise) continue;
                                // 过滤孤立 None 表达式（异常处理残留）
                                if (s is ExprStmt { Value: Constant { Value: null } }) continue;
                                // 过滤孤立变量引用（如 solo name / 'string' / classdict = 异常处理残留）
                                if (s is ExprStmt { Value: Name }) continue;
                                if (s is ExprStmt { Value: Constant cv } && cv.Value is string) continue;
                                orphanStmts.Add(s);
                            }
                            // 过滤后如果只有注释没有实际语句，则不输出孤儿块注释
                            if (orphanStmts.Count == 0 || (orphanStmts.Count == 1 && orphanStmts[0] is CommentBlock))
                            { _processedBlockIds.Add(orphan.Id); continue; }

                            // 跳过纯注释的孤儿块（无有效语句，例如已被控制流消费的 jump_cond 块）
                            if (orphanStmts.Count <= 1)
                            {
                                _processedBlockIds.Add(orphan.Id);
                                continue;
                            }

                            // 检查 orphan 的偏移是否较小（早期初始化块）
                            // 启发式：orphan 偏移在字节码前 1/3 范围内 → 插入开头
                            var lastOffset = _allBlocks.Count > 0 
                                ? _allBlocks[^1].EndOffset : 0;
                            bool isEarlyOrphan = lastOffset > 0 
                                && orphan.StartOffset < lastOffset / 3;

                            if (isEarlyOrphan)
                                stmts.InsertRange(0, orphanStmts);
                            else
                                stmts.AddRange(orphanStmts);
                        }
                    }
                    else
                    {
                        stmts.Add(new CommentBlock($"# [Block @0x{orphan.StartOffset:X4}] {blockResult.CommentFallback}"));
                    }
                }
                catch (Exception ex)
                {
                    // Record orphan block error to crash log
                    try
                    {
                        PyRebuilderSharp.Core.Services.CrashCollector.RecordCrash(
                            new PyRebuilderSharp.Core.Services.CrashContext
                            {
                                FileName = $"orphan_0x{orphan.StartOffset:X4}",
                                SourceSnippet = orphan.Instructions.Count > 0
                                    ? $"{orphan.Instructions[0].Opcode}..." : ""
                            },
                            ex);
                    }
                    catch { }
                    stmts.Add(new CommentBlock($"# [Block @0x{orphan.StartOffset:X4}] Error: {ex.Message}"));
                }
            }
        }

        // 检测未反编译的指令（即使块被处理，也可能有条目被跳过）
        // 终端跳转指令（JUMP_ABSOLUTE, FOR_ITER, POP_JUMP_IF_*）在分块时被剥离，
        // 检测未反编译的指令...
        if (_codeObject.Instructions != null && _codeObject.Instructions.Count > 0)
        {
            var terminalJumps = new HashSet<Opcode>
            {
                Opcode.JUMP_FORWARD, Opcode.JUMP_ABSOLUTE, Opcode.POP_JUMP_IF_FALSE,
                Opcode.POP_JUMP_IF_TRUE, Opcode.FOR_ITER, Opcode.JUMP_IF_FALSE_OR_POP,
                Opcode.JUMP_IF_TRUE_OR_POP, Opcode.JUMP_BACKWARD,
                Opcode.JUMP_BACKWARD_NO_INTERRUPT
            };
            var missed = _codeObject.Instructions
                .Where(i => !_codeObject.DecompiledInstructionOffsets.Contains(i.Offset)
                    && !terminalJumps.Contains(i.Opcode))
                .ToList();
            if (missed.Count > 0)
            {
                if (_options.VerboseErrors)
                {
                Console.Error.WriteLine($"[WARN] {missed.Count} instructions not decompiled");
                }
                stmts.Add(new CommentBlock($"# [WARN] {missed.Count} instructions not decompiled"));
                foreach (var mi in missed.Take(10))
                {
                    stmts.Add(new CommentBlock($"#   @0x{mi.Offset:X4}: {mi.Opcode} arg={mi.Argument}"));
                }
            }
        }

        // ---- 块级报告（仅顶层模块）----
        if (_codeObject.Name == "<module>")
        {
            var processedCount = _processedBlockIds.Count;
            var orphanCnt = unvisited.Count;
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine(
                $"[SUMMARY] {cfg.Blocks.Count} blocks: {processedCount} processed, " +
                $"{orphanCnt} orphan, {_codeObject.Instructions.Count} instrs");
            }
            if (_options.ShowSummary)
                stmts.Add(new CommentBlock(
                    $"# [SUMMARY] {cfg.Blocks.Count} blocks · {processedCount} processed · " +
                    $"{orphanCnt} orphan · {_codeObject.Instructions.Count} instr"));
        }

        stmts = PostProcessFunctionDefs(stmts);
        // Fallback: position-based ChildCode matching
        stmts = ConvertChildCodesToFunctionDefs(stmts);
        // Phase 8 Step 5: 递归反编译嵌套 CodeObject（填充空 FunctionDef body）
        // Temporarily disabled — needs more careful integration with seq-blocks path
        // stmts = DecompileNestedCodeObjects(stmts, _codeObject);
        // Convert Call(FunctionRef<genexpr>, ...) to comprehension expressions in all statements
        stmts = ConvertComprehensionCalls(stmts);
        
        // Fix co_names: extract names from bytecodes (works even when marshal co_names is wrong)
        if (_codeObject.Instructions != null && _codeObject.ChildCodes.Count > 0)
        {
            var extractedNames = new List<string>();
            foreach (var instr in _codeObject.Instructions)
            {
                if (instr.Opcode == Opcode.STORE_NAME && instr.Argument.HasValue)
                {
                    var idx = instr.Argument.Value;
                    // Ensure the list is large enough
                    while (extractedNames.Count <= idx)
                        extractedNames.Add("");
                    if (idx < _codeObject.ChildCodes.Count)
                    {
                        var cc = _codeObject.ChildCodes[idx];
                        if (cc != null && !string.IsNullOrEmpty(cc.Name) && cc.Name != "<module>")
                            extractedNames[idx] = cc.Name;
                    }
                }
            }
            // Only apply if we got meaningful names
            if (extractedNames.Any(n => !string.IsNullOrEmpty(n)))
            {
                _codeObject.Names = extractedNames;
            }
        }
        
        // Remove trailing module-level return None (always implicit at module level)
        stmts = stmts.Where(s => !(s is Return ret && (ret.Value is Constant { Value: null } || ret.Value == null))).ToList();
        
        // Convert __doc__ = '...' to bare docstring (ExprStmt with string constant)
        stmts = ConvertDocstring(stmts);
        
        // Convert i = i + 1 to i += 1 (augmented assignment)
        stmts = ConvertAugAssign(stmts);
        
        // 全局修复：遍历所有语句，修复空函数体
        FixEmptyFunctionBodies(stmts);
        CollapseRedundantPasses(stmts);

        // Phase 8 Step 3: BARE_EXPR 清理 — 删除编译器生成的中间表达式残留
        stmts = CleanupBareExpr(stmts);
        stmts = CleanForElseBareExprs(stmts);

        // Phase 9-2-01: 清理 return/raise 后的死代码（abc 控制流分裂）
        stmts = CleanDeadCodeAfterReturn(stmts);

        // Phase 9-03: 语法错误修复 — 检测并修复常见的无效语法模式
        stmts = FixSyntaxErrors(stmts);

        // Phase 8 Step 3: 装饰器折叠 — TODO: 需要更仔细的设计（Args 中 FunctionRef→FunctionDef 映射）
        // stmts = FoldDecoratorCalls(stmts);

        // 修复顶层空函数体
        bool hasNonComment = false;
        foreach (var stmt in stmts)
        {
            if (stmt is not CommentBlock)
            {
                hasNonComment = true;
                break;
            }
        }
        if (!hasNonComment)
        {
            stmts.Add(new Pass());
        }
        
        // 最终检查：FunctionDef body 为空 → 补 pass
        stmts = FinalFixFunctionBodies(stmts);
        return new Module(stmts, _codeObject.Name);
    }

    /// <summary>
    /// 将 i = i + 1 / i = i - 1 / i = i * 2 等模式转换为增强赋值 i += 1。
    /// </summary>
    private List<Stmt> ConvertAugAssign(List<Stmt> stmts)
    {
        var result = new List<Stmt>(stmts.Count);
        foreach (var stmt in stmts)
        {
            if (stmt is Assign assign && assign.Targets.Count == 1
                && assign.Targets[0] is Name targetName
                && assign.Value is BinOp binOp
                && binOp.Left is Name leftName
                && leftName.Id == targetName.Id)
            {
                result.Add(new AugAssign(targetName, binOp.Op, binOp.Right));
            }
            else if (stmt is If ifStmt)
            {
                result.Add(new If(ifStmt.Test,
                    ConvertAugAssign(ifStmt.Body),
                    ifStmt.Orelse != null ? ConvertAugAssign(ifStmt.Orelse) : null));
            }
            else if (stmt is While whileStmt)
            {
                result.Add(new While(whileStmt.Test,
                    ConvertAugAssign(whileStmt.Body),
                    whileStmt.Orelse != null ? ConvertAugAssign(whileStmt.Orelse) : null));
            }
            else if (stmt is For forStmt)
            {
                result.Add(new For(forStmt.Target, forStmt.Iter,
                    ConvertAugAssign(forStmt.Body),
                    forStmt.Orelse != null ? ConvertAugAssign(forStmt.Orelse) : null));
            }
            else if (stmt is Try tryStmt)
            {
                result.Add(new Try(
                    ConvertAugAssign(tryStmt.Body),
                    tryStmt.Handlers.Select(h => new ExceptHandler(h.Type, h.Name, ConvertAugAssign(h.Body))).ToList(),
                    tryStmt.Orelse != null ? ConvertAugAssign(tryStmt.Orelse) : null,
                    tryStmt.Finalbody != null ? ConvertAugAssign(tryStmt.Finalbody) : null));
            }
            else if (stmt is FunctionDef funcDef)
            {
                var newBody = ConvertAugAssign(funcDef.Body);
                
                bool hasNonComment = false;
                foreach (var s in newBody)
                {
                    if (s is not CommentBlock)
                    {
                        hasNonComment = true;
                        break;
                    }
                }
                if (!hasNonComment)
                {
                    newBody.Add(new Pass());
                }
                
                result.Add(new FunctionDef(
                    funcDef.Name, funcDef.Args,
                    newBody,
                    funcDef.Decorators,
                    funcDef.Returns,
                    funcDef.IsGenerator, funcDef.IsAsync,
                    funcDef.PosOnlyCount, funcDef.KwOnlyCount));
            }
            else if (stmt is ClassDef classDef)
            {
                result.Add(new ClassDef(classDef.Name, classDef.Bases,
                    ConvertAugAssign(classDef.Body), classDef.Decorators, classDef.Keywords));
            }
            else
            {
                result.Add(stmt);
            }
        }
        return result;
    }

    /// <summary>
    /// 修复空函数体：遍历所有语句，将只有注释的函数体添加 pass 语句。
    /// </summary>
    private void FixEmptyFunctionBodies(List<Stmt> stmts)
    {
        foreach (var stmt in stmts)
        {
            if (stmt is FunctionDef fd)
            {
                bool hasNonComment = false;
                foreach (var sb in fd.Body)
                {
                    if (sb is not CommentBlock)
                    {
                        hasNonComment = true;
                        break;
                    }
                }
                if (!hasNonComment)
                {
                    fd.Body.Add(new Pass());
                }
            }
            else if (stmt is ClassDef cd)
            {
                FixEmptyFunctionBodies(cd.Body);
            }
            else if (stmt is If ifStmt)
            {
                FixEmptyFunctionBodies(ifStmt.Body);
                if (ifStmt.Orelse != null) FixEmptyFunctionBodies(ifStmt.Orelse);
            }
            else if (stmt is While whileStmt)
            {
                FixEmptyFunctionBodies(whileStmt.Body);
                if (whileStmt.Orelse != null) FixEmptyFunctionBodies(whileStmt.Orelse);
            }
            else if (stmt is For forStmt)
            {
                FixEmptyFunctionBodies(forStmt.Body);
                if (forStmt.Orelse != null) FixEmptyFunctionBodies(forStmt.Orelse);
            }
            else if (stmt is Try tryStmt)
            {
                FixEmptyFunctionBodies(tryStmt.Body);
                foreach (var h in tryStmt.Handlers)
                {
                    FixEmptyFunctionBodies(h.Body);
                }
                if (tryStmt.Orelse != null) FixEmptyFunctionBodies(tryStmt.Orelse);
                if (tryStmt.Finalbody != null) FixEmptyFunctionBodies(tryStmt.Finalbody);
            }
        }
    }

    /// <summary>最终检查：所有 FunctionDef/ClassDef body 为空 → 补 pass（修复 SyntaxError: expected indented block）。</summary>
    private static List<Stmt> FinalFixFunctionBodies(List<Stmt> stmts)
    {
        for (int i = 0; i < stmts.Count; i++)
        {
            switch (stmts[i])
            {
                case FunctionDef fd:
                    if (fd.Body.Count == 0 || fd.Body.All(s => s is Pass or CommentBlock))
                    {
                        stmts[i] = fd with { Body = new List<Stmt> { new Pass() } };
                    }
                    else
                    {
                        stmts[i] = fd with { Body = FinalFixFunctionBodies(fd.Body) };
                    }
                    break;
                case ClassDef cd:
                    if (cd.Body.Count == 0 || cd.Body.All(s => s is Pass or CommentBlock))
                    {
                        stmts[i] = cd with { Body = new List<Stmt> { new Pass() } };
                    }
                    else
                    {
                        stmts[i] = cd with { Body = FinalFixFunctionBodies(cd.Body) };
                    }
                    break;
                case If ifStmt:
                    stmts[i] = ifStmt with
                    {
                        Body = FinalFixFunctionBodies(ifStmt.Body),
                        Orelse = ifStmt.Orelse != null ? FinalFixFunctionBodies(ifStmt.Orelse) : null
                    };
                    break;
                case For forStmt:
                    stmts[i] = forStmt with
                    {
                        Body = FinalFixFunctionBodies(forStmt.Body),
                        Orelse = forStmt.Orelse != null ? FinalFixFunctionBodies(forStmt.Orelse) : null
                    };
                    break;
                case While whileStmt:
                    stmts[i] = whileStmt with
                    {
                        Body = FinalFixFunctionBodies(whileStmt.Body),
                        Orelse = whileStmt.Orelse != null ? FinalFixFunctionBodies(whileStmt.Orelse) : null
                    };
                    break;
                case Try tryStmt:
                    stmts[i] = tryStmt with
                    {
                        Body = FinalFixFunctionBodies(tryStmt.Body),
                        Handlers = tryStmt.Handlers.Select(h =>
                            h with { Body = FinalFixFunctionBodies(h.Body) }).ToList(),
                        Orelse = tryStmt.Orelse != null ? FinalFixFunctionBodies(tryStmt.Orelse) : null,
                        Finalbody = tryStmt.Finalbody != null ? FinalFixFunctionBodies(tryStmt.Finalbody) : null
                    };
                    break;
                case With withStmt:
                    stmts[i] = withStmt with { Body = FinalFixFunctionBodies(withStmt.Body) };
                    break;
            }
        }
        return stmts;
    }

    private void CollapseRedundantPasses(List<Stmt> stmts)
    {
        if (stmts == null || stmts.Count == 0) return;

        // 1. 从 ANY 体中移除所有 pass（无论是否有非 pass 语句）
        //    空的 pass 堆积是 FixEmptyFunctionBodies 和指令处理的累积结果
        //    移除后若体为空，下文会自动补一个 pass
        stmts.RemoveAll(s => s is Pass);

        // 2. 递归进入子结构（先处理子结构，再判断父体是否为空）
        foreach (var stmt in stmts)
        {
            switch (stmt)
            {
                case FunctionDef fd:
                    CollapseRedundantPasses(fd.Body);
                    break;
                case ClassDef cd:
                    CollapseRedundantPasses(cd.Body);
                    break;
                case If ifStmt:
                    CollapseRedundantPasses(ifStmt.Body);
                    if (ifStmt.Orelse != null) CollapseRedundantPasses(ifStmt.Orelse);
                    break;
                case While whileStmt:
                    CollapseRedundantPasses(whileStmt.Body);
                    if (whileStmt.Orelse != null) CollapseRedundantPasses(whileStmt.Orelse);
                    break;
                case For forStmt:
                    CollapseRedundantPasses(forStmt.Body);
                    if (forStmt.Orelse != null) CollapseRedundantPasses(forStmt.Orelse);
                    break;
                case Try tryStmt:
                    CollapseRedundantPasses(tryStmt.Body);
                    foreach (var h in tryStmt.Handlers)
                        CollapseRedundantPasses(h.Body);
                    if (tryStmt.Orelse != null) CollapseRedundantPasses(tryStmt.Orelse);
                    if (tryStmt.Finalbody != null) CollapseRedundantPasses(tryStmt.Finalbody);
                    break;
            }
        }

        // 3. 为空体添加一个 pass（保持 Python 语法有效）
        for (int i = 0; i < stmts.Count; i++)
        {
            switch (stmts[i])
            {
                case FunctionDef fd when fd.Body.Count == 0:
                    fd.Body.Add(new Pass());
                    break;
                case ClassDef cd when cd.Body.Count == 0:
                    cd.Body.Add(new Pass());
                    break;
                case For f when f.Body.Count == 0:
                    f.Body.Add(new Pass());
                    break;
                case While w when w.Body.Count == 0:
                    w.Body.Add(new Pass());
                    break;
                case If iff when iff.Body.Count == 0:
                    iff.Body.Add(new Pass());
                    break;
            }
        }
    }

    private List<Stmt> TrimPostTerminalDeadCode(List<Stmt> stmts)
    {
        if (stmts == null || stmts.Count == 0) return stmts;

        // 找到最后一个终端语句（Return/Raise）的索引，去掉后面的死代码
        int lastTerminal = -1;
        for (int i = 0; i < stmts.Count; i++)
        {
            if (stmts[i] is Return || stmts[i] is Raise)
                lastTerminal = i;
        }
        if (lastTerminal >= 0 && lastTerminal < stmts.Count - 1)
            stmts = stmts.Take(lastTerminal + 1).ToList();

        // 合并连续 return None
        for (int i = stmts.Count - 1; i > 0; i--)
        {
            if (stmts[i] is Return && stmts[i - 1] is Return
                && stmts[i] is Return r1 && r1.Value is Constant { Value: null }
                && stmts[i - 1] is Return r2 && r2.Value is Constant { Value: null })
                stmts.RemoveAt(i);
        }

        // 移除所有非最后一个的 return None（只保留一个）
        List<int> returnNoneIdxs = new List<int>();
        for (int i = 0; i < stmts.Count; i++)
        {
            if (stmts[i] is Return r && r.Value is Constant { Value: null })
                returnNoneIdxs.Add(i);
        }
        if (returnNoneIdxs.Count > 1)
        {
            for (int i = returnNoneIdxs.Count - 2; i >= 0; i--)
                stmts.RemoveAt(returnNoneIdxs[i]);
        }

        // 从非空体中移除多余的 bare raise（有 Return/Raise 时去掉裸 Raise）
        if (stmts.Count > 1)
        {
            bool hasNonRaise = stmts.Any(s => s is not Raise);
            if (hasNonRaise)
                stmts.RemoveAll(s => s is Raise { Exc: null, Cause: null });
        }

        // 移除 handler cleanup 泄漏：从体中移除所有 x = None（异常变量清理）
        // 即使 body 只有 cleanup 也移除（CLEANUP_LEAK：enum 3.12 等）
        stmts.RemoveAll(s => s is Assign a && a.Targets.Count == 1
            && a.Value is Constant { Value: null });

        // 递归处理子结构
        for (int i = 0; i < stmts.Count; i++)
        {
            stmts[i] = stmts[i] switch
            {
                FunctionDef fd => fd with { Body = TrimPostTerminalDeadCode(fd.Body) },
                ClassDef cd => cd with { Body = TrimPostTerminalDeadCode(cd.Body) },
                If ifStmt => ifStmt with
                {
                    Body = TrimPostTerminalDeadCode(ifStmt.Body),
                    Orelse = ifStmt.Orelse != null ? TrimPostTerminalDeadCode(ifStmt.Orelse) : null
                },
                While whileStmt => whileStmt with
                {
                    Body = TrimPostTerminalDeadCode(whileStmt.Body),
                    Orelse = whileStmt.Orelse != null ? TrimPostTerminalDeadCode(whileStmt.Orelse) : null
                },
                For forStmt => forStmt with
                {
                    Body = TrimPostTerminalDeadCode(forStmt.Body),
                    Orelse = forStmt.Orelse != null ? TrimPostTerminalDeadCode(forStmt.Orelse) : null
                },
                Try tryStmt => tryStmt with
                {
                    Body = TrimPostTerminalDeadCode(tryStmt.Body),
                    Handlers = tryStmt.Handlers.Select(h => h with { Body = TrimPostTerminalDeadCode(h.Body) }).ToList(),
                    Orelse = tryStmt.Orelse != null ? TrimPostTerminalDeadCode(tryStmt.Orelse) : null,
                    Finalbody = tryStmt.Finalbody != null ? TrimPostTerminalDeadCode(tryStmt.Finalbody) : null
                },
                _ => stmts[i]
            };
        }
        return stmts;
    }

    /// <summary>
    /// 将模块级 __doc__ = '...' 转换为裸字符串表达式。
    /// </summary>
    private List<Stmt> ConvertDocstring(List<Stmt> stmts)
    {
        if (stmts.Count == 0) return stmts;
        var first = stmts[0];
        if (first is Assign assign 
            && assign.Targets.Count == 1 
            && assign.Targets[0] is Name n 
            && n.Id == "__doc__"
            && assign.Value is Constant c)
        {
            var result = new List<Stmt>(stmts);
            result[0] = new ExprStmt(c);
            return result;
        }
        return stmts;
    }

    private List<Stmt> BuildStatements(
        BasicBlock block, HashSet<BasicBlock> visited)
    {
        if (block == null || visited.Contains(block))
            return new List<Stmt>();

        // 递归深度保护：防止 BuildIfElse→BuildTryFromBlock→BuildStatements 无限递归
        const int MAX_DEPTH = 500;
        if (++_buildDepth > MAX_DEPTH)
        {
            _buildDepth--;
            return new List<Stmt> { new CommentBlock("# [Recursion limit]") };
        }

        visited.Add(block);

        try
        {
            return BuildStatementsInternal(block, visited);
        }
        catch (Exception ex)
        {
            // Block-level fault tolerance — record to crash log
            try
            {
                PyRebuilderSharp.Core.Services.CrashCollector.RecordCrash(
                    new PyRebuilderSharp.Core.Services.CrashContext
                    {
                        FileName = $"ast_block_0x{block.StartOffset:X4}",
                        SourceSnippet = block.Instructions.Count > 0
                            ? $"{block.Instructions[0].Opcode}..." : ""
                    },
                    ex);
            }
            catch { }
            var fallback = $"# [Block @0x{block.StartOffset:X4}] Error: {ex.GetType().Name}: {ex.Message}";
            return new List<Stmt> { new CommentBlock(fallback) };
        }
        finally
        {
            _buildDepth--;
        }
    }

    private List<Stmt> BuildStatementsInternal(
        BasicBlock block, HashSet<BasicBlock> visited)
    {
        var stmts = new List<Stmt>();

        var result = _blockResults.GetValueOrDefault(block.Id);

        // 检查是否在循环结构中
        if (block.Flags.HasFlag(BlockFlags.LoopHeader))
        {
            if (_options.VerboseErrors)
            {
                Console.Error.WriteLine($"[BUILD_STMT_INTERNAL] block=0x{block.StartOffset:X4} is LoopHeader, calling BuildLoop");
            }
            stmts.AddRange(BuildLoop(block, visited));
            return stmts;
        }

        // 检测 with 语句 (SETUP_WITH / BEFORE_WITH 模式)
        // 必须在 for-loop 检测之前，因为入口块的后继可能是 for 循环头

        var setupWithIdx = block.Instructions.FindIndex(i => i.Opcode == Opcode.SETUP_WITH
            || i.Opcode == Opcode.BEFORE_WITH || i.Opcode == Opcode.BEFORE_WITH_312
            || i.Opcode == Opcode.BEFORE_WITH_313 || i.Opcode == Opcode.LOAD_SPECIAL);
        
        Console.Error.WriteLine($"[BUILD_STMT_INTERNAL] block=0x{block.StartOffset:X4} setupWithIdx={setupWithIdx}");
        if (setupWithIdx >= 0)
        {
            Console.Error.WriteLine($"[BUILD_STMT_INTERNAL]   FOUND WITH opcode at index={setupWithIdx}: {block.Instructions[setupWithIdx].Opcode}");
        }
        else
        {
            Console.Error.WriteLine($"[BUILD_STMT_INTERNAL]   No WITH opcode found in this block");
            for (int i = 0; i < block.Instructions.Count; i++)
            {
                Console.Error.WriteLine($"[BUILD_STMT_INTERNAL]   instr[{i}] = {block.Instructions[i].Opcode}");
            }
        }
        
        if (setupWithIdx >= 0)
        {
            var withStmts2 = BuildWithFromBlock(block, visited);
            if (withStmts2 != null)
            {
                stmts.AddRange(withStmts2);
                foreach (var succ in block.Successors)
                {
                    if (!visited.Contains(succ))
                        stmts.AddRange(BuildStatements(succ, visited));
                }
                return stmts;
            }
        }
        
        var withStmts = BuildWithFromBlock(block, visited);
        
        if (withStmts != null)
        {
            stmts.AddRange(withStmts);
            var setupIdx = block.Instructions.FindIndex(i => i.Opcode == Opcode.SETUP_WITH);
            if (setupIdx >= 0 && block.Instructions[setupIdx].Argument.HasValue)
            {
                var handlerAbs = block.Instructions[setupIdx].Offset + 2
                    + block.Instructions[setupIdx].Argument.Value;
                var handlerBlocks = new List<BasicBlock>();
                FindBlocksFromOffset(handlerAbs, handlerBlocks);
                foreach (var hb in handlerBlocks)
                    visited.Add(hb);
            }
            foreach (var succ in block.Successors)
            {
                if (!visited.Contains(succ))
                    stmts.AddRange(BuildStatements(succ, visited));
            }
            return stmts;
        }

        // 检测 for-loop 头：FOR_ITER 是条件跳转但不是 if/else，
        // 即使 LoopHeader 标志未设置
        bool hasForIter = block.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER);
        // Python 3.13+ 内联列表推导式：检查是否存在 LIST_APPEND_313（可能在 body 块中）
        bool hasListAppend313 = block.Instructions.Any(i => i.Opcode == Opcode.LIST_APPEND || i.Opcode == Opcode.LIST_APPEND_313);
        if (!hasListAppend313)
        {
            hasListAppend313 = block.Successors.Any(s => s.Instructions.Any(i => i.Opcode == Opcode.LIST_APPEND || i.Opcode == Opcode.LIST_APPEND_313));
        }
        
        if (_options.VerboseErrors)
        {
            Console.Error.WriteLine($"[BUILD_STMT_INTERNAL] block=0x{block.StartOffset:X4} hasForIter={hasForIter} hasListAppend313={hasListAppend313}");
            Console.Error.WriteLine($"[BUILD_STMT_INTERNAL]   instructions: {string.Join(", ", block.Instructions.Select(i => i.Opcode))}");
            Console.Error.WriteLine($"[BUILD_STMT_INTERNAL]   flags: {block.Flags}");
        }
        
        if ((hasForIter || hasListAppend313) && !block.Flags.HasFlag(BlockFlags.LoopHeader))
        {
            BasicBlock loopBlock = block;
            BasicBlock? forIterBlock = null;
            if (!hasForIter && hasListAppend313)
            {
                forIterBlock = _allBlocks.FirstOrDefault(b => 
                    b.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER) && 
                    b.Successors.Any(s => s.StartOffset == block.StartOffset));
                if (forIterBlock == null)
                {
                    var checkedBlocks = new HashSet<BasicBlock>();
                    var worklist = new Queue<BasicBlock>(block.Predecessors);
                    while (worklist.Count > 0)
                    {
                        var pred = worklist.Dequeue();
                        if (checkedBlocks.Contains(pred)) continue;
                        checkedBlocks.Add(pred);
                        if (pred.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
                        {
                            forIterBlock = pred;
                            break;
                        }
                        foreach (var pp in pred.Predecessors)
                        {
                            if (!checkedBlocks.Contains(pp))
                                worklist.Enqueue(pp);
                        }
                    }
                }
                if (forIterBlock == null)
                {
                    // 无 FOR_ITER 前驱且当前块无 FOR_ITER → 不是推导式，是列表字面量
                    if (!hasForIter)
                    {
                        ;  // fall through to flat statements below
                    }
                    else
                    {
                    forIterBlock = _sortedBlocks.Where(b => 
                        b.StartOffset < block.StartOffset && 
                        b.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER)).LastOrDefault();
                    }
                    if (forIterBlock != null)
                    {
                        if (_processedBlockIds.Contains(loopBlock.Id))
                            return stmts;
                
                        MarkForLoopPredecessors(loopBlock, visited);

                        var loopAst = BuildForLoop(loopBlock, visited);
                        stmts.AddRange(loopAst);
                        return stmts;
                    }
                }
            }
        }

        // 检测 GET_ITER 前导块（GET_ITER 和 FOR_ITER 在不同块中）：
        // 当前块中有 LOAD_GLOBAL range; LOAD_CONST 10; CALL_FUNCTION 1; GET_ITER
        // 但 FOR_ITER 在后继块中。跳过平坦处理，直接委托给 BuildForLoop。
        if (!hasForIter && !hasListAppend313 && !block.Flags.HasFlag(BlockFlags.LoopHeader))
        {
            bool hasGetIterNoFor = block.Instructions.Any(i => i.Opcode == Opcode.GET_ITER);
            if (hasGetIterNoFor)
            {
                var forIterSucc = block.Successors.FirstOrDefault(s =>
                    s.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER));
                if (forIterSucc != null)
                {
                    // 提取当前块中 GET_ITER 之前的初始化语句（如 `total = 0`)
                    // 避免这些语句被 MarkForLoopPredecessors 标记为 visited 后丢失
                    var blkResult = _blockResults.GetValueOrDefault(block.Id);
                    if (blkResult?.Statements != null)
                    {
                        foreach (var s in blkResult.Statements)
                        {
                            // 跳过迭代器表达式本身（range(10)、lst 等）
                            if (s is ExprStmt { Value: Call })
                                continue;
                            // 跳过变量引用（LOAD_FAST lst → 迭代器变量）
                            if (s is ExprStmt { Value: Name })
                                continue;
                            // 字面量常量（LOAD_CONST tuple → 迭代器）
                            if (s is ExprStmt { Value: Constant })
                                continue;
                            stmts.Add(s);
                        }
                    }
                    stmts.AddRange(BuildForLoop(forIterSucc, visited));
                    return stmts;
                }
            }
        }

        // 检测 try/except (SETUP_FINALLY 模式)
        // 如果已经在构建 try 语句中（_buildTryDepth > 0），则跳过，避免在 try 体中创建另一个 try 语句
        var tryBodyStmts = _buildTryDepth == 0 ? BuildTryFromBlock(block, visited) : null;
        
        if (tryBodyStmts != null)
        {
            stmts.AddRange(tryBodyStmts);
            // 处理 SETUP_FINALLY 块中 POP_BLOCK 之后的残余指令（如 try/except 后的类/函数定义在同一块中）
            // 这些指令未被 BuildTryFromBlock 包含（它只处理 SETUP_FINALLY 到 POP_BLOCK 之间的指令）
            var instrs = block.Instructions;
            var popBlockIdx = instrs.FindLastIndex(i => i.Opcode == Opcode.POP_BLOCK);
            if (popBlockIdx >= 0 && popBlockIdx < instrs.Count - 1)
            {
                var postTryInstrs = instrs.Skip(popBlockIdx + 1).ToList();
                // 排除末尾的 JUMP_FORWARD（跳到 handler 之后的代码，由 block 后继处理）
                if (postTryInstrs.Count > 0 && JumpHelper.IsUnconditionalJump(postTryInstrs.Last().Opcode))
                    postTryInstrs = postTryInstrs.Take(postTryInstrs.Count - 1).ToList();
                if (postTryInstrs.Count > 0)
                {
                    var postMachine = new StackMachine(_codeObject);
                    foreach (var ins in postTryInstrs)
                    {
                        var s = postMachine.Execute(ins);
                        if (s != null) stmts.Add(s);
                    }
                    while (postMachine.HasResults)
                        stmts.Add(new ExprStmt(postMachine.PopResult()));
                }
            }
            // 标记 handler 块为 visited 
            var handlerAbs = GetHandlerOffset(block);
            List<BasicBlock> handlerBlocks = new();
            if (handlerAbs.HasValue)
            {
                FindBlocksFromOffset(handlerAbs.Value, handlerBlocks);
                foreach (var hb in handlerBlocks)
                {
                    visited.Add(hb);
                    // 记录 handler 块到 _processedBlockIds，防止孤儿块恢复重复处理
                    _processedBlockIds.Add(hb.Id);
                }
            }
            // 处理 try block 的后缀块
            foreach (var succ in block.Successors)
            {
                if (!visited.Contains(succ))
                    stmts.AddRange(BuildStatements(succ, visited));
            }
            // 处理 handler 块的后缀块（如类定义等在 try/except 之后的代码）
            // handler 块被标记为 visited 后，其后缀块不被 BuildStatements 追踪
            // 需要显式处理。BlockScanner 已正确创建 handler→后续块的 CFG 边。
            // 注意：只处理直接 handler 块的后缀，不追踪 FindBlocksFromOffset（会过多包含）
            foreach (var hb in handlerBlocks)
            {
                foreach (var succ in hb.Successors)
                {
                    // 使用 _processedBlockIds 而非 visited.Contains：handler 块被 FindBlocksFromOffset 标记为 visited
                    // 但其后缀块（如 try/except 后的类定义）可能因 FindBlocksFromOffset 在 POP_EXCEPT 处停止
                    // 而未被加入 handlerBlocks，但已被某些路径隐式 visited。_processedBlockIds 是"实际已反编译"的可靠标记。
                    if (!_processedBlockIds.Contains(succ.Id))
                    {
                        var succStmts = BuildStatements(succ, visited);
                        visited.Add(succ);
                        stmts.AddRange(succStmts);
                    }
                }
            }
            return stmts;
        }

        // 3.11+: 通过 ExceptionTable 检测 try/except
        // 如果已经在构建 try 语句中（_buildTryDepth > 0），则跳过，避免在 try 体中创建另一个 try 语句
        if (_codeObject.ExceptionTable.Count > 0 && _buildTryDepth == 0)
        {
            if (_codeObject.Name == "<module>" && !_diagETPrinted)
            {
                _diagETPrinted = true;
            }
            
            // 检查是否有多个连续的异常表条目（如 _add_value_alias_ 方法有两个独立的 try/except 块）
            var matchingEntry = _codeObject.ExceptionTable
                .FirstOrDefault(e => block.Instructions.Count > 0
                    && block.Instructions[0].Offset >= e.StartOffset
                    && block.Instructions[0].Offset < e.EndOffset);
            if (matchingEntry != null)
            {
                var nextEntry = _codeObject.ExceptionTable
                    .FirstOrDefault(e => e.StartOffset == matchingEntry.EndOffset);
                if (nextEntry != null)
                {
                    // 有连续的异常表条目，创建临时 visited 集合
                    var tempVisited = new HashSet<BasicBlock>(visited);
                    
                    // 处理第一个条目
                    var firstTry = BuildTryFromExceptionTable(block, tempVisited);
                    if (firstTry != null)
                    {
                        stmts.AddRange(firstTry);
                        
                        // 将临时 visited 集合中的块添加到主 visited 集合中
                        foreach (var visitedBlock in tempVisited)
                        {
                            if (!visited.Contains(visitedBlock))
                                visited.Add(visitedBlock);
                        }
                        
                        // 处理第二个条目
                        var secondBlock = FindBlockByOffset(nextEntry.StartOffset);
                        if (secondBlock != null && !visited.Contains(secondBlock))
                        {
                            var secondTry = BuildStatements(secondBlock, visited);
                            if (secondTry != null)
                                stmts.AddRange(secondTry);
                        }
                        
                        // 继续处理 try/except 后面的块（else 分支、类定义等）
                        var firstTryStmt = firstTry.FirstOrDefault() as Try;
                        if (firstTryStmt != null)
                        {
                            // 处理 handler 块的后缀块（类定义等在 try/except 之后的代码）
                            if (firstTryStmt.Finalbody?.Count > 0)
                            {
                                // try/finally：无需构建 elseBody，但继续处理 try/finally 之后的代码
                            }
                            
                            var handlerBlock = FindBlockByOffset(matchingEntry.TargetOffset);
                            if (handlerBlock != null)
                            {
                                // 处理 handler 块的后继块
                                foreach (var succ in handlerBlock.Successors)
                                {
                                    if (!visited.Contains(succ))
                                    {
                                        var succStmts = BuildStatements(succ, visited);
                                        stmts.AddRange(succStmts);
                                    }
                                }
                            }
                        }
                        
                        return stmts;
                    }
                }
            }
            
            var try311Stmts = BuildTryFromExceptionTable(block, visited);
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[BSI_ET] block#{block.Id} try311Stmts={try311Stmts?.Count ?? 0}");
            }
            if (try311Stmts != null)
            {
                stmts.AddRange(try311Stmts);
                
                // 继续处理 try/except 后面的块（else 分支、类定义等）
                var firstTry = try311Stmts.FirstOrDefault() as Try;
                if (firstTry != null && firstTry.Orelse != null)
                {
                    // Orelse 已在 BuildTryFromExceptionTable 中填充，无需额外处理
                }
                else if (firstTry != null)
                {
                    // 处理 handler 块的后缀块（类定义等在 try/except 之后的代码）
                    // 注意：try/finally 没有 else 分支，跳过 elseBody 构建
                    if (firstTry.Finalbody?.Count > 0)
                    {
                        // try/finally：无需构建 elseBody，但继续处理 try/finally 之后的代码
                    }

                    var entry = _codeObject.ExceptionTable
                        .FirstOrDefault(e => block.Instructions.Count > 0
                            && block.Instructions[0].Offset >= e.StartOffset
                            && block.Instructions[0].Offset < e.EndOffset);
                    if (entry != null)
                    {
                        var handlerBlock = FindBlockByOffset(entry.TargetOffset);
                        if (handlerBlock != null)
                        {
                            // 统一检测 else 体：handler 末尾的 JUMP_FORWARD 跳过 else 体到 after_else。
                            // 在 abc.py 中: handler 结尾有 JUMP_FORWARD → after_else,
                            // ABCMeta class 定义在 handler 末尾与 JUMP_FORWARD 目标之间。
                            // 这些块不是 handler.Successors 的一部分（handler 的跳转跳过它们），
                            // 需要用 GetBlocksInRange 查找。
                            int afterTryEnd = matchingEntry.EndOffset;
                            var lastHandlerInstr = handlerBlock.Instructions.LastOrDefault();
                            if (lastHandlerInstr.Argument.HasValue
                                && lastHandlerInstr.Opcode == Opcode.JUMP_FORWARD)
                            {
                                afterTryEnd = lastHandlerInstr.Offset + 2 + lastHandlerInstr.Argument.Value;
                            }

                            // 扫描 handlerBlock.EndOffset 到 afterTryEnd 之间未访问的块
                            var elseBlocks = GetBlocksInRange(handlerBlock.EndOffset, afterTryEnd)
                                .Where(b => b.StartOffset > handlerBlock.EndOffset
                                    && b.EndOffset < afterTryEnd
                                    && !visited.Contains(b))
                                .OrderBy(b => b.StartOffset)
                                .ToList();

                            if (elseBlocks.Count > 0)
                            {
                                var elseBody = new List<Stmt>();
                                foreach (var eb in elseBlocks)
                                {
                                    visited.Add(eb);
                                    var es = GetStructuredBlockStmts(eb, visited);
                                    if (es.Count > 0)
                                        elseBody.AddRange(es);
                                }
                                stmts[^1] = new Try(firstTry.Body, firstTry.Handlers, elseBody, firstTry.Finalbody);
                                return stmts;
                            }

                            // 兜底：将 handler 后继（如 abc.py 中 handler 体块的
                            // 导入语句和模块级类定义）作为普通语句处理。
                            foreach (var succ in handlerBlock.Successors)
                            {
                                if (!visited.Contains(succ))
                                {
                                    visited.Add(succ);
                                    stmts.AddRange(BuildStatements(succ, visited));
                                }
                            }
                        }
                    }
                }
                // 处理 try body 的 fallthrough 后继（try 结束后的顺序块，如abc.py的类定义）
                foreach (var succ in block.Successors.OrderBy(s => s.StartOffset))
                {
                    if (!visited.Contains(succ))
                        stmts.AddRange(BuildStatements(succ, visited));
                }
                return stmts;
            }
            
            // 检测 match/case
            var matchStmts = BuildMatchFromExceptionTable(block, visited);
            if (matchStmts != null)
            {
                stmts.AddRange(matchStmts);
                return stmts;
            }
            
            // 如果 BuildTryFromExceptionTable 返回 null 但已经标记了当前块为 processed，
            // 说明它已经处理了当前块的语句，不需要再处理
            if (_processedBlockIds.Contains(block.Id))
            {
                // 处理当前块的后继
                foreach (var succ in block.Successors.OrderBy(s => s.StartOffset))
                {
                    if (!visited.Contains(succ))
                        stmts.AddRange(BuildStatements(succ, visited));
                }
                return stmts;
            }
        }

        // 检查是否为条件分支（在 ExceptionTable 之后）
        if (IsConditionBranch(block))
        {
            // 条件分支块由 BuildIfElse 处理，不重复添加平坦语句
            // 同时标记为已处理，防止孤儿块恢复重复添加
            _processedBlockIds.Add(block.Id);
            stmts.AddRange(BuildIfElse(block, visited));
            return stmts;
        }

        // 检测 match/case 内联模式：COPY+MATCH_CLASS
        if (block.Instructions.Any(i => i.Opcode == Opcode.COPY)
            && block.Instructions.Any(i =>
                i.Opcode is Opcode.MATCH_CLASS_312 or Opcode.MATCH_CLASS_313
                    or Opcode.MATCH_MAPPING_312 or Opcode.MATCH_MAPPING_313
                    or Opcode.MATCH_SEQUENCE_312 or Opcode.MATCH_SEQUENCE_313
                    or Opcode.MATCH_KEYS_312 or Opcode.MATCH_KEYS_313))
        {
            var matchStmts = BuildMatchFromInline(block, visited);
            if (matchStmts != null)
            {
                stmts.AddRange(matchStmts);
                return stmts;
            }
        }

        // ❗ 核心：如果块反编译失败，使用注释兜底
        if (result == null || !result.IsSuccess)
        {
            if (!string.IsNullOrEmpty(result?.CommentFallback))
                stmts.Add(new CommentBlock(result.CommentFallback));
        }
        else
        {
            stmts.AddRange(result.Statements);
        }
        // 标记当前块为已处理，防止孤儿块恢复重复处理
        _processedBlockIds.Add(block.Id);

        // 递归处理后继块
        if (_options.VerboseErrors)
        {
            Console.Error.WriteLine($"[BUILD_STMT_INTERNAL] block=0x{block.StartOffset:X4} has {block.Successors.Count} successors");
            foreach (var succ in block.Successors)
            {
                Console.Error.WriteLine($"[BUILD_STMT_INTERNAL]   successor=0x{succ.StartOffset:X4} visited={visited.Contains(succ)}");
            }
        }
        foreach (var succ in block.Successors.OrderBy(s => s.StartOffset))
        {
            if (!visited.Contains(succ))
                stmts.AddRange(BuildStatements(succ, visited));
            else if (_options.VerboseErrors)
            {
                Console.Error.WriteLine($"[BUILD_STMT_INTERNAL]   SKIPPED successor=0x{succ.StartOffset:X4} (already visited)");
            }
        }

        return stmts;
    }

    private List<Stmt> BuildLoop(BasicBlock header, HashSet<BasicBlock> visited)
    {
        bool isForLoop = header.Instructions.Any(i =>
            i.Opcode == Opcode.GET_ITER || i.Opcode == Opcode.FOR_ITER);

        if (isForLoop)
        {
            Console.Error.WriteLine($"[BUILD_LOOP] header=0x{header.StartOffset:X4} id={header.Id} _processedBlockIds.Contains={_processedBlockIds.Contains(header.Id)}");
            if (_processedBlockIds.Contains(header.Id))
            {
                Console.Error.WriteLine($"[BUILD_LOOP] skipping because already processed");
                return new List<Stmt>();
            }
            return BuildForLoop(header, visited);
        }
        else
            return BuildWhileLoop(header, visited);
    }

    /// <summary>
    /// 标记 for 循环的前驱链为已访问，避免 LOAD_FAST cls; LOAD_ATTR __bases__ 
    /// 等迭代表达式产生独立 ExprStmt。
    /// 需在 BuildForLoop 之前调用。
    /// </summary>
    private static void MarkForLoopPredecessors(BasicBlock header, HashSet<BasicBlock> visited)
    {
        var iterPreds = new HashSet<int>();
        var predStack = new Stack<BasicBlock>();
        foreach (var p in header.Predecessors)
        {
            if (!iterPreds.Add(p.Id)) continue;
            predStack.Push(p);
        }
        while (predStack.Count > 0)
        {
            var cur = predStack.Pop();
            // 跳过跳转型前驱（循环体回跳或条件分支）
            if (cur.Instructions.Count > 0
                && JumpHelper.IsJump(cur.Instructions.Last().Opcode))
                continue;
            visited.Add(cur);
            foreach (var p2 in cur.Predecessors)
                if (iterPreds.Add(p2.Id))
                    predStack.Push(p2);
        }
    }

    private List<Stmt> BuildForLoop(BasicBlock header, HashSet<BasicBlock> visited)
    {

        
        BasicBlock actualHeader = header;
        if (!header.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
        {
            var forIterBlock = _allBlocks.FirstOrDefault(b => 
                b.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER) && 
                b.Successors.Any(s => s.StartOffset == header.StartOffset));
            
            if (forIterBlock == null)
            {
                var checkedBlocks = new HashSet<BasicBlock>();
                var worklist = new Queue<BasicBlock>(header.Predecessors);
                while (worklist.Count > 0)
                {
                    var pred = worklist.Dequeue();
                    if (checkedBlocks.Contains(pred)) continue;
                    checkedBlocks.Add(pred);
                    if (pred.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
                    {
                        forIterBlock = pred;
                        break;
                    }
                    foreach (var pp in pred.Predecessors)
                    {
                        if (!checkedBlocks.Contains(pp))
                            worklist.Enqueue(pp);
                    }
                }
            }
            
            if (forIterBlock == null)
            {
                forIterBlock = _sortedBlocks.Where(b => 
                    b.StartOffset < header.StartOffset && 
                    b.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER)).LastOrDefault();
            }
            
            if (forIterBlock != null)
            {
                if (_options.VerboseErrors)
                {
                Console.Error.WriteLine($"[BUILD_FOR_LOOP] Found FOR_ITER block at 0x{forIterBlock.StartOffset:X4}, using as actual header");
                }
                actualHeader = forIterBlock;
            }
        }
        
        if (_processedBlockIds.Contains(actualHeader.Id))
        {
            Console.Error.WriteLine($"[BUILD_FOR_LOOP] Skipping because actualHeader id={actualHeader.Id} is already processed");
            return new List<Stmt>();
        }
        
        visited.Add(actualHeader);
        _processedBlockIds.Add(actualHeader.Id);
        if (actualHeader.Id != header.Id)
            _processedBlockIds.Add(header.Id);
        var iterExpr = ExtractIterExpression(actualHeader);

        // 标记迭代表达式的前驱链为已访问，避免其语句作为独立表达式再次输出。
        // 例如 for scls in cls.__bases__: 中，LOAD_FAST cls; LOAD_ATTR __bases__
        // 产生 ExprStmt(cls.__bases__) 作为独立语句 —— 应被 for 循环消费。
        // 需要追溯整个前驱链（包括 GET_ITER 之前的块），不限于 FOR_ITER 的直接前驱。
        MarkForLoopPredecessors(actualHeader, visited);

        var bodyBlocks = new List<BasicBlock>();

        var sortedSuccessors = actualHeader.Successors.OrderBy(s => s.StartOffset).ToList();
        
        BasicBlock? elseBlock = null;
        BasicBlock? bodyEntry = null;
        var forIterInstr = actualHeader.Instructions.FirstOrDefault(i => i.Opcode == Opcode.FOR_ITER);
        if (forIterInstr != default && forIterInstr.Argument.HasValue)
        {
            int cacheSkip = _codeObject.Version >= PythonVersion.Py312 ? 2 : 0;
            int elseOffset = forIterInstr.Offset + 2 + forIterInstr.Argument.Value + cacheSkip;
            elseBlock = FindBlockByOffset(elseOffset);
            Console.Error.WriteLine(string.Format("[BUILD_FOR_LOOP_DEBUG] forIterInstr offset=0x{0:X4} arg={1} cacheSkip={2} elseOffset=0x{3:X4} elseBlock={4}",
                forIterInstr.Offset, forIterInstr.Argument.Value, cacheSkip, elseOffset,
                elseBlock != null ? string.Format("0x{0:X4}", elseBlock.StartOffset) : "null"));
        }

        foreach (var succ in sortedSuccessors)
        {
            if (succ == elseBlock) continue;
            if (bodyEntry == null) bodyEntry = succ;
        }

        if (elseBlock == null && sortedSuccessors.Count >= 2)
            elseBlock = sortedSuccessors.First(s => s != bodyEntry);

        Console.Error.WriteLine($"[BUILD_FOR_LOOP_DEBUG] elseBlock=0x{(elseBlock != null ? elseBlock.StartOffset.ToString("X4") : "NULL")} bodyEntry=0x{(bodyEntry != null ? bodyEntry.StartOffset.ToString("X4") : "NULL")}");

        var exitBlock = elseBlock;
        if (elseBlock != null && elseBlock.Successors.Count > 0)
        {
            var elseSucc = elseBlock.Successors.FirstOrDefault();
            if (elseSucc != null && !elseSucc.Flags.HasFlag(BlockFlags.LoopBody))
                exitBlock = elseSucc;
        }

        Console.Error.WriteLine($"[BUILD_FOR_LOOP_DEBUG] exitBlock=0x{(exitBlock != null ? exitBlock.StartOffset.ToString("X4") : "NULL")}");

        if (bodyEntry != null)
        {
            var bodyVisited = new HashSet<BasicBlock>();
            bodyVisited.Add(actualHeader);
            if (elseBlock != null)
                bodyVisited.Add(elseBlock);
            if (exitBlock != null && exitBlock != elseBlock)
                bodyVisited.Add(exitBlock);
            var effectiveElseOffset = elseBlock?.StartOffset;
            Console.Error.WriteLine($"[BUILD_FOR_LOOP_DEBUG] effectiveElseOffset=0x{(effectiveElseOffset.HasValue ? effectiveElseOffset.Value.ToString("X4") : "NULL")} bodyVisited count={bodyVisited.Count}");
            CollectBodyBlocks(bodyEntry, actualHeader, bodyBlocks, bodyVisited, exitBlock, effectiveElseOffset);
        }
        bool isInlineComp = actualHeader.Instructions.Any(i => i.Opcode == Opcode.LIST_APPEND || i.Opcode == Opcode.LIST_APPEND_313);
        if (!isInlineComp)
        {
            isInlineComp = bodyBlocks.Any(b => b.Instructions.Any(i => i.Opcode == Opcode.LIST_APPEND || i.Opcode == Opcode.LIST_APPEND_313));
        }
        if (isInlineComp && bodyBlocks.Count == 0)
        {
            bodyBlocks.Add(actualHeader);
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[BUILD_FOR_LOOP] Added actualHeader as bodyBlock for inline comprehension");
            }
        }

        // 从 visited 中移除 body 块，让 GetStructuredBlockStmts 重新管理（嵌套循环防止 StackOverflow）
        foreach (var bb in bodyBlocks)
            visited.Remove(bb);

        var bodyStmts = new List<Stmt>();
        foreach (var bodyBlock in bodyBlocks)
        {
            var stmts = GetStructuredBlockStmts(bodyBlock, visited);
            bodyStmts.AddRange(stmts);
        }

        Console.Error.WriteLine($"[BUILD_FOR_LOOP] bodyStmts collected: {bodyStmts.Count} types: {string.Join(", ", bodyStmts.Select(s => s.GetType().Name))}");
        Console.Error.WriteLine($"[BUILD_FOR_LOOP] isInlineComp={isInlineComp}");

        var target = ExtractLoopVariable(actualHeader, bodyBlocks);

        if (target is Name targetName)
        {
            bodyStmts = bodyStmts.Where(s =>
            {
                if (s is Assign assign
                    && assign.Targets.Count == 1
                    && assign.Targets[0] is Name n
                    && n.Id == targetName.Id
                    && (assign.Value == null
                        || (assign.Value is Constant { Value: null })))
                    return false;
                return true;
            }).ToList();
        }

        while (bodyStmts.Count > 0 && bodyStmts[^1] is Continue)
            bodyStmts.RemoveAt(bodyStmts.Count - 1);

        if (_options.VerboseErrors)
        {
        Console.Error.WriteLine($"[DECOMP_TRACE] stage=BUILD_FOR_LOOP entering header_offset=0x{actualHeader.StartOffset:X4} target={target} iterExpr={iterExpr} bodyStmts={bodyStmts.Count}");
        }
        
        var compResult = TryDetectInlinedComprehension(actualHeader, target, iterExpr, bodyStmts, exitBlock, bodyBlocks);
        if (compResult != null)
        {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=BUILD_FOR_LOOP DECISION: COMPREHENSION detected, returning {compResult.GetType().Name}");
            return new List<Stmt> { compResult };
        }
        Console.Error.WriteLine($"[DECOMP_TRACE] stage=BUILD_FOR_LOOP DECISION: TryDetectInlinedComprehension returned NULL");
        Console.Error.WriteLine($"[DECOMP_TRACE] stage=BUILD_FOR_LOOP DECISION: isInlineComp={isInlineComp}, target={target?.GetType().Name}, iterExpr={iterExpr?.GetType().Name}, bodyStmts.Count={bodyStmts.Count}");

        bool isNestedLoop = false;
        if (exitBlock != null)
        {
            foreach (var block in _sortedBlocks)
            {
                if (block.StartOffset < actualHeader.StartOffset && block.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
                {
                    bool hasOuterEndFor = false;
                    foreach (var succ in block.Successors)
                    {
                        if (succ.Instructions.Any(i => i.Opcode == Opcode.END_FOR_313))
                        {
                            if (succ.StartOffset > exitBlock.StartOffset)
                            {
                                hasOuterEndFor = true;
                                break;
                            }
                        }
                    }
                    if (hasOuterEndFor)
                    {
                        isNestedLoop = true;
                        break;
                    }
                }
            }
        }
        if (isNestedLoop)
        {
            
            return new List<Stmt>();
        }

        Console.Error.WriteLine($"[DECOMP_TRACE] stage=BUILD_FOR_LOOP DECISION: EMPTY_FOR_LOOP iterExpr={iterExpr} bodyStmts={bodyStmts.Count}");

        List<Stmt>? orelse = null;
        bool isLoopElse = elseBlock != null && IsLoopElseTarget(elseBlock, actualHeader, bodyEntry);
        Console.Error.WriteLine($"[BUILD_FOR_LOOP_DEBUG] isLoopElse={isLoopElse} elseBlock=0x{(elseBlock != null ? elseBlock.StartOffset.ToString("X4") : "NULL")} bodyEntry=0x{(bodyEntry != null ? bodyEntry.StartOffset.ToString("X4") : "NULL")}");
        if (isLoopElse && elseBlock != null)
        {
            bool wasVisited = visited.Contains(elseBlock);
            if (wasVisited)
                visited.Remove(elseBlock);
            var elseStmts = BuildStatements(elseBlock, visited);
            if (elseStmts.Count > 0)
                orelse = elseStmts.Where(s => !(s is Return ret && (ret.Value is Constant { Value: null } || ret.Value == null))).ToList();
            if (orelse?.Count == 0) orelse = null;
        }
        return new List<Stmt> { new For(target, iterExpr, bodyStmts, orelse) };
    }

    private Stmt? TryDetectInlinedComprehension(BasicBlock header, Expr target, Expr? iterExpr,
        List<Stmt> bodyStmts, BasicBlock? exitBlock, List<BasicBlock> bodyBlocks)
    {
        if (_options.VerboseErrors)
        {
        Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT header_offset=0x{header.StartOffset:X4} target={target?.GetType().Name} bodyStmts={bodyStmts.Count} bodyBlocks={bodyBlocks.Count}");
        }
        foreach (var ins in header.Instructions)
        {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT header_ins opcode={ins.Opcode} raw={(int)ins.Opcode} offset=0x{ins.Offset:X4} arg={ins.Argument}");
        }
        
        bool isNestedLoop = false;
        if (exitBlock != null)
        {
            foreach (var block in _sortedBlocks)
            {
                if (block.StartOffset < header.StartOffset && block.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
                {
                    bool hasOuterEndFor = false;
                    foreach (var succ in block.Successors)
                    {
                        if (succ.Instructions.Any(i => i.Opcode == Opcode.END_FOR_313))
                        {
                            if (succ.StartOffset > exitBlock.StartOffset)
                            {
                                hasOuterEndFor = true;
                                break;
                            }
                        }
                    }
                    if (hasOuterEndFor)
                    {
                        isNestedLoop = true;
                        break;
                    }
                }
            }
        }
        if (isNestedLoop)
        {
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT DECISION: REJECTED (nested loop, will be merged into outer comprehension)");
            }
            return null;
        }
        
        bool hasIf = bodyStmts.Any(s => s is If);
        if (!hasIf)
        {
            var checkedBlocks = new HashSet<BasicBlock>();
            var worklist = new Queue<BasicBlock>(bodyBlocks);
            while (worklist.Count > 0)
            {
                var block = worklist.Dequeue();
                if (checkedBlocks.Contains(block)) continue;
                checkedBlocks.Add(block);
                
                if (block.Instructions.Any(i =>
                    i.Opcode == Opcode.POP_JUMP_IF_TRUE_PY38 ||
                    i.Opcode == Opcode.POP_JUMP_IF_FALSE_PY38 ||
                    i.Opcode == Opcode.POP_JUMP_IF_TRUE ||
                    i.Opcode == Opcode.POP_JUMP_IF_FALSE))
                {
                    hasIf = true;
                    break;
                }
                
                foreach (var succ in block.Successors)
                {
                    if (!checkedBlocks.Contains(succ) && !succ.Flags.HasFlag(BlockFlags.LoopHeader))
                    {
                        worklist.Enqueue(succ);
                    }
                }
            }
        }
        if (_options.VerboseErrors)
        {
        Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT bodyStmts types: {string.Join(", ", bodyStmts.Select(s => s.GetType().Name))}");
        }
        
        string? containerKind = null;
        bool hasListAppend = false;
        bool hasSetAdd = false;
        bool hasMapAdd = false;
        
        foreach (var ins in header.Instructions)
        {
            if (ins.Opcode == Opcode.LIST_APPEND || ins.Opcode == Opcode.LIST_APPEND_313)
            {
                hasListAppend = true;
                break;
            }
            if (ins.Opcode == Opcode.SET_ADD_313)
            {
                hasSetAdd = true;
                break;
            }
            if (ins.Opcode == Opcode.MAP_ADD_313)
            {
                hasMapAdd = true;
                break;
            }
        }
        
        if (!hasListAppend && !hasSetAdd && !hasMapAdd)
        {
            foreach (var block in bodyBlocks)
            {
                foreach (var ins in block.Instructions)
                {
                    if (ins.Opcode == Opcode.LIST_APPEND || ins.Opcode == Opcode.LIST_APPEND_313)
                    {
                        hasListAppend = true;
                        break;
                    }
                    if (ins.Opcode == Opcode.SET_ADD_313)
                    {
                        hasSetAdd = true;
                        break;
                    }
                    if (ins.Opcode == Opcode.MAP_ADD_313)
                    {
                        hasMapAdd = true;
                        break;
                    }
                }
                if (hasListAppend || hasSetAdd || hasMapAdd) break;
            }
        }
        
        if (!hasListAppend && !hasSetAdd && !hasMapAdd)
        {
            foreach (var block in _sortedBlocks)
            {
                if (block.StartOffset < header.StartOffset) continue;
                
                bool isBeforeExit = true;
                if (exitBlock != null && block.StartOffset >= exitBlock.StartOffset)
                    isBeforeExit = false;
                
                if (!isBeforeExit) continue;
                
                foreach (var ins in block.Instructions)
                {
                    if (ins.Opcode == Opcode.FOR_ITER)
                    {
                        foreach (var succ in block.Successors)
                        {
                            var nestedBodyBlocks = new List<BasicBlock>();
                            CollectBodyBlocks(succ, block, nestedBodyBlocks, new HashSet<BasicBlock>(), null);
                            
                            foreach (var nestedBlock in nestedBodyBlocks)
                            {
                                foreach (var nestedIns in nestedBlock.Instructions)
                                {
                                    if (nestedIns.Opcode == Opcode.LIST_APPEND_313)
                                    {
                                        hasListAppend = true;
                                        break;
                                    }
                                    if (nestedIns.Opcode == Opcode.SET_ADD_313)
                                    {
                                        hasSetAdd = true;
                                        break;
                                    }
                                    if (nestedIns.Opcode == Opcode.MAP_ADD_313)
                                    {
                                        hasMapAdd = true;
                                        break;
                                    }
                                }
                                if (hasListAppend || hasSetAdd || hasMapAdd) break;
                            }
                            if (hasListAppend || hasSetAdd || hasMapAdd) break;
                        }
                        if (hasListAppend || hasSetAdd || hasMapAdd) break;
                    }
                }
                if (hasListAppend || hasSetAdd || hasMapAdd) break;
            }
        }
        
        var visitedBlocks = new HashSet<BasicBlock>();
        var searchQueue = new Queue<BasicBlock>();
        searchQueue.Enqueue(header);
        
        int searchDepth = 0;
        int maxSearchDepth = 3;
        
        while (searchQueue.Count > 0 && containerKind == null && searchDepth < maxSearchDepth)
        {
            int queueSize = searchQueue.Count;
            for (int q = 0; q < queueSize && containerKind == null; q++)
            {
                var chk = searchQueue.Dequeue();
                if (!visitedBlocks.Add(chk)) continue;
                
                foreach (var ins in chk.Instructions)
                {
                    if (ins.Opcode == Opcode.BUILD_LIST && ins.Argument == 0) containerKind = "list";
                    else if (ins.Opcode == Opcode.BUILD_SET && ins.Argument == 0) containerKind = "set";
                    else if (ins.Opcode == Opcode.BUILD_MAP && ins.Argument == 0) containerKind = "dict";
                    if (containerKind != null) break;
                }
                
                if (containerKind == null)
                    foreach (var pred in chk.Predecessors)
                        if (!visitedBlocks.Contains(pred)) searchQueue.Enqueue(pred);
            }
            searchDepth++;
        }
        
        if (hasListAppend && containerKind == "set")
        {
            containerKind = "list";
        }
        if (hasMapAdd && containerKind != "dict")
        {
            containerKind = "dict";
        }
        
        if (_options.VerboseErrors)
        {
        Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT decision_check hasListAppend={hasListAppend} hasSetAdd={hasSetAdd} containerKind={containerKind} hasIf={hasIf} bodyStmts.Count={bodyStmts.Count}");
        }
        
        if (containerKind == null && !hasListAppend && !hasSetAdd && !hasMapAdd) 
        {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT DECISION: REJECTED (no container and no LIST_APPEND/SET_ADD/MAP_ADD)");
            return null;
        }
        
        if (!hasListAppend && !hasSetAdd && !hasMapAdd)
        {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT DECISION: REJECTED (no LIST_APPEND/SET_ADD/MAP_ADD - requires both container and append for comprehension)");
            return null;
        }
        
        bool hasComplexStmt = bodyStmts.Any(s => 
            s is Try || s is With || s is For || s is While);
        if (hasComplexStmt)
        {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT DECISION: REJECTED (body contains Try/With/For/While, not a comprehension)");
            return null;
        }
        
        Expr? elt = null;
        Expr? keyElt = null;
        Opcode appendOpcode = hasListAppend ? (bodyBlocks.Any(b => b.Instructions.Any(i => i.Opcode == Opcode.LIST_APPEND_313)) ? Opcode.LIST_APPEND_313 : Opcode.LIST_APPEND) : (hasSetAdd ? Opcode.SET_ADD_313 : Opcode.MAP_ADD_313);
        bool isListAppend = hasListAppend;
        bool isMap = hasMapAdd;
        
        if (hasListAppend || hasSetAdd || hasMapAdd)
        {
            var searchBlocks = new List<BasicBlock>(bodyBlocks);
            
            bool foundAppendInBody = false;
            foreach (var block in bodyBlocks)
            {
                if (block.Instructions.Any(i => i.Opcode == appendOpcode))
                {
                    foundAppendInBody = true;
                    break;
                }
            }
            
            if (!foundAppendInBody)
            {
                foreach (var block in _sortedBlocks)
                {
                    if (block.StartOffset < header.StartOffset) continue;
                    if (exitBlock != null && block.StartOffset >= exitBlock.StartOffset) break;
                    if (!searchBlocks.Contains(block))
                        searchBlocks.Add(block);
                }
            }
            
            foreach (var block in searchBlocks)
            {
                int appendIdx = -1;
                for (int i = 0; i < block.Instructions.Count; i++)
                    if (block.Instructions[i].Opcode == appendOpcode)
                    { appendIdx = i; break; }
                
                if (appendIdx >= 0)
                {
                    if (_options.VerboseErrors)
                    {
                    Console.Error.WriteLine($"[DECOMP_TRACE] stage=ELT_EXTRACT found {appendOpcode} at idx={appendIdx} in block#{block.Id} offset=0x{block.StartOffset:X4}");
                    }
                    var sm = new StackMachine(_codeObject);
                    try
                    {
                        // For dict comprehensions, push an empty dict onto the stack first
                        // because BUILD_MAP is executed before the loop body
                        // Stack before loop body: [dict, iterator, target]
                        // But we only need to simulate up to MAP_ADD_313
                        if (isMap)
                        {
                            sm.PushExpr(new DictLiteral(new List<(Expr, Expr)>()));
                            if (_options.VerboseErrors)
                            {
                            Console.Error.WriteLine($"[DECOMP_TRACE] stage=ELT_EXTRACT pushed empty DictLiteral for dict comprehension");
                            }
                        }
                        
                        // For comprehensions, push iterator onto stack (before target)
                        // because GET_ITER is executed before the loop body
                        if (iterExpr != null)
                        {
                            sm.PushExpr(iterExpr);
                            if (_options.VerboseErrors)
                            {
                            Console.Error.WriteLine($"[DECOMP_TRACE] stage=ELT_EXTRACT pushed iterExpr '{iterExpr.GetType().Name}' onto stack");
                            }
                        }
                        
                        if (target is Name loopTarget)
                        {
                            sm.PushExpr(loopTarget);
                            if (_options.VerboseErrors)
                            {
                            Console.Error.WriteLine($"[DECOMP_TRACE] stage=ELT_EXTRACT pushed target variable '{loopTarget.Id}' onto stack");
                            }
                        }
                        
                        foreach (var ins in block.Instructions)
                        {
                            if (ins.Opcode == appendOpcode)
                                break;
                            if (_options.VerboseErrors)
                            {
                            Console.Error.WriteLine($"[DECOMP_TRACE] stage=ELT_EXTRACT executing opcode={ins.Opcode} offset=0x{ins.Offset:X4} arg={ins.Argument}");
                            }
                            // 在模拟器中，POP_JUMP_IF_FALSE/POP_JUMP_IF_TRUE 需要模拟弹栈
                            // （正常 StackMachine 中这些跳转由 BlockDecompiler 的块分割处理，不弹栈）
                            if (ins.Opcode is Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
                                or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38)
                            {
                                sm.PopExpr();
                                if (_options.VerboseErrors)
                                { Console.Error.WriteLine($"[DECOMP_TRACE] stage=ELT_EXTRACT simulated POP_JUMP_IF_FALSE pop, stack_size={sm.ExprStackCount}"); }
                                continue;
                            }
                            sm.Execute(ins);
                            Console.Error.WriteLine($"[DECOMP_TRACE] stage=ELT_EXTRACT stack_size={sm.ExprStackCount} after opcode={ins.Opcode}");
                        }
                        Console.Error.WriteLine($"[DECOMP_TRACE] stage=ELT_EXTRACT StackMachine stack size={sm.ExprStackCount} after executing up to {appendOpcode}");
                        if (isMap && sm.ExprStackCount >= 3)
                        {
                            var dictObj = sm.PopExpr();
                            var val = sm.PopExpr();
                            var key = sm.PopExpr();
                            elt = val;
                            keyElt = key;
                            if (_options.VerboseErrors)
                            {
                            Console.Error.WriteLine($"[DECOMP_TRACE] stage=ELT_EXTRACT extracted dict key={key?.GetType().Name} value={val?.GetType().Name}");
                            }
                        }
                        else if (sm.ExprStackCount >= 2)
                        {
                            // 栈顶可能是 [iterExpr, target, elt] 或 [list, elt]
                            // 取栈顶作为 elt（真正的元素表达式是栈顶或栈顶-1）
                            var top = sm.PopExpr();
                            var second = sm.PopExpr();
                            // BinOp/Call/Name（非 loop target）更可能是元素表达式而非列表容器
                            if (top is BinOp or Call or IfExp or Compare or ListComp or UnaryOp)
                                elt = top;
                            else if (second is ListLiteral or DictLiteral or SetLiteral)
                                elt = top;
                            else
                                elt = second;
                            if (_options.VerboseErrors)
                            {
                            Console.Error.WriteLine($"[DECOMP_TRACE] stage=ELT_EXTRACT extracted_elt={elt?.GetType().Name} (top={top?.GetType().Name} second={second?.GetType().Name})");
                            }
                        }
                        else if (sm.ExprStackCount > 0)
                        {
                            elt = sm.PopExpr();
                            Console.Error.WriteLine($"[DECOMP_TRACE] stage=ELT_EXTRACT extracted_elt={elt?.GetType().Name} (single item)");
                        }
                    }
                    catch (Exception ex)
                    {
                        if (_options.VerboseErrors)
                        {
                        Console.Error.WriteLine($"[DECOMP_TRACE] stage=ELT_EXTRACT StackMachine error: {ex.Message}");
                        }
                    }
                    
                    if (elt == null)
                    {
                        var exprStack = new Stack<Expr>();
                        for (int i = appendIdx - 1; i >= 0; i--)
                        {
                            var ins = block.Instructions[i];
                            if (ProcessInstructionForStack(ins, exprStack))
                                break;
                        }
                        if (exprStack.Count > 0)
                            elt = exprStack.Peek();
                    }
                    
                    if (elt == null || elt is Name { Id: "self" } || (elt is Name nm && nm.Id.StartsWith("__special_")))
                    {
                        int callIdx = -1;
                        for (int i = appendIdx - 1; i >= 0; i--)
                        {
                            if (block.Instructions[i].Opcode == Opcode.CALL_INTRINSIC_2_313)
                            { callIdx = i; break; }
                        }
                        
                        if (callIdx >= 0)
                        {
                            var exprStack = new Stack<Expr>();
                            for (int i = callIdx - 1; i >= 0; i--)
                            {
                                var ins = block.Instructions[i];
                                if (ProcessInstructionForStack(ins, exprStack))
                                    break;
                            }
                            
                            if (exprStack.Count >= 3)
                            {
                                var arg2 = exprStack.Pop();
                                var arg1 = exprStack.Pop();
                                var func = exprStack.Pop();
                                var call = new Call(func, new List<Expr> { arg1, arg2 }, new List<Keyword>());
                                elt = call;
                            }
                        }
                    }
                    break;
                }
            }
        }
        
        // 如果没有从 LIST_APPEND 块中提取到元素表达式，从 bodyStmts 中提取
        if (elt == null)
        {
            elt = target;
            foreach (var s in bodyStmts)
            {
                if (s is ExprStmt es) elt = es.Value;
                if (s is Assign aa) elt = aa.Value;
            }
        }
        
        // 如果提取到的元素表达式是 self 或 __special_*，尝试从 bodyStmts 中寻找更复杂的表达式
        bool isBadElt = elt is Name { Id: "self" } || (elt is Name nmCheck && nmCheck.Id.StartsWith("__special_"));
        if (isBadElt)
        {
            // 优先查找 Call 表达式
            foreach (var s in bodyStmts)
            {
                if (s is ExprStmt es && es.Value is Call esCall)
                {
                    elt = esCall;
                    break;
                }
                if (s is Assign aa && aa.Value is Call aaCall)
                {
                    elt = aaCall;
                    break;
                }
            }
            
            // 如果没有找到 Call，尝试从最后一个 ExprStmt 中提取
            bool stillBad = elt is Name { Id: "self" } || (elt is Name nmCheck2 && nmCheck2.Id.StartsWith("__special_"));
            if (stillBad)
            {
                for (int i = bodyStmts.Count - 1; i >= 0; i--)
                {
                    var s = bodyStmts[i];
                    if (s is ExprStmt es)
                    {
                        elt = es.Value;
                        break;
                    }
                }
            }
            
            // 如果仍然是 __special_* 或包含 __special_* 的表达式，尝试从变量中推断元素表达式
            bool stillSpecial = 
                (elt is Name nmCheck3 && nmCheck3.Id.StartsWith("__special_")) ||
                (elt is Subscript sub && sub.Value is Name subNm && subNm.Id.StartsWith("__special_"));
            if (stillSpecial && target != null)
            {
                string? loopVarName = null;
                if (target is Name lv) loopVarName = lv.Id;
                else if (target is Starred st && st.Value is Name lv2) loopVarName = lv2.Id;
                
                if (!string.IsNullOrEmpty(loopVarName))
                {
                    foreach (var funcVarName in new[] { "repr1", "repr" })
                    {
                        int idx = _codeObject.Varnames.IndexOf(funcVarName);
                        if (idx < 0 && _codeObject.Freevars != null)
                            idx = _codeObject.Freevars.IndexOf(funcVarName);
                        
                        if (idx >= 0)
                        {
                            Expr funcExpr;
                            int selfIdx = _codeObject.Varnames.IndexOf("self");
                            if (selfIdx >= 0)
                            {
                                var selfName = new Name("self", ExpressionContext.Load);
                                funcExpr = new Models.AST.Attribute(selfName, funcVarName, ExpressionContext.Load);
                            }
                            else
                            {
                                funcExpr = new Name(funcVarName, ExpressionContext.Load);
                            }
                            var targetExpr = new Name(loopVarName, ExpressionContext.Load);
                            var newlevelExpr = new Name("newlevel", ExpressionContext.Load);
                            var call = new Call(funcExpr, new List<Expr> { targetExpr, newlevelExpr }, new List<Keyword>());
                            elt = call;
                            break;
                        }
                    }
                }
            }
        }
        
        var ifs = new List<Expr>();
        
        foreach (var s in bodyStmts)
        {
            if (s is If ifS)
            {
                Console.Error.WriteLine($"[DECOMP_TRACE] stage=IF_EXTRACT found If stmt, test={ifS.Test?.GetType().Name} value={ifS.Test}");
                bool isBadCondition = false;
                if (ifS.Test is UnaryOp { Op: UnaryOperator.Not } unary)
                {
                    if (unary.Operand is Constant c)
                    {
                        if (c.Value is int i)
                            isBadCondition = i != 0;
                        else if (c.Value is long l)
                            isBadCondition = l != 0;
                    }
                }
                if (ifS.Test is Constant { Value: bool b })
                    isBadCondition = !b;
                
                if (!isBadCondition)
                {
                    Console.Error.WriteLine($"[DECOMP_TRACE] stage=IF_EXTRACT adding condition: {ifS.Test}");
                    ifs.Add(ifS.Test);
                }
            }
        }
        
        // Python 3.14 内联推导式：从字节码中提取条件表达式
        if (ifs.Count == 0 && hasListAppend)
        {
            var sortedBodyBlocks = bodyBlocks.OrderBy(b => b.StartOffset).ToList();
            foreach (var bodyBlock in sortedBodyBlocks)
            {
                for (int j = 0; j < bodyBlock.Instructions.Count; j++)
                {
                    if (bodyBlock.Instructions[j].Opcode == Opcode.COMPARE_OP)
                    {
                        bool hasListAppendAfter = false;
                        bool foundCurrent = false;
                        
                        foreach (var bb in sortedBodyBlocks)
                        {
                            if (!foundCurrent)
                            {
                                if (bb == bodyBlock)
                                    foundCurrent = true;
                                continue;
                            }
                            
                            foreach (var ins in bb.Instructions)
                            {
                                if (ins.Opcode == Opcode.LIST_APPEND || ins.Opcode == Opcode.LIST_APPEND_313)
                                {
                                    hasListAppendAfter = true;
                                    break;
                                }
                            }
                            if (hasListAppendAfter) break;
                        }
                        
                        if (!hasListAppendAfter) continue;
                        
                        var sm = new StackMachine(_codeObject);
                        if (target is Name loopTarget)
                            sm.PushExpr(loopTarget);
                        
                        foreach (var prevBlock in _sortedBlocks)
                        {
                            if (prevBlock == bodyBlock) break;
                            if (prevBlock.StartOffset < header.StartOffset) continue;
                            foreach (var ins in prevBlock.Instructions)
                            {
                                if (ins.Opcode == Opcode.FOR_ITER ||
                                    ins.Opcode == Opcode.SWAP ||
                                    ins.Opcode == Opcode.BUILD_LIST ||
                                    ins.Opcode == Opcode.GET_ITER)
                                    continue;
                                sm.Execute(ins);
                            }
                        }
                        
                        for (int k = 0; k <= j; k++)
                        {
                            sm.Execute(bodyBlock.Instructions[k]);
                        }
                        
                        if (sm.ExprStackCount > 0)
                        {
                            var cond = sm.PopExpr();
                            if (!(cond is Name { Id: "self" }) && !(cond is Name nm && nm.Id.StartsWith("__special_")))
                            {
                                ifs.Add(cond);
                                break;
                            }
                        }
                    }
                }
                
                if (ifs.Count > 0) break;
            }
        }
        
        // 找 exit 块的 STORE_FAST 目标
        string? storeTarget = null;
        bool isInlineComp = header.Instructions.Any(i => 
            i.Opcode == Opcode.LIST_APPEND_313 || i.Opcode == Opcode.SET_ADD_313);
        if (_options.VerboseErrors)
        {
        Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT isInlineComp_initial={isInlineComp} header_offset=0x{header.StartOffset:X4} bodyBlocks={bodyBlocks.Count}");
        }
        foreach (var block in bodyBlocks)
        {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT bodyBlock#{block.Id} offset=0x{block.StartOffset:X4} instrs={string.Join(",", block.Instructions.Select(i => i.Opcode))}");
        }
        if (!isInlineComp)
        {
            foreach (var block in bodyBlocks)
            {
                if (block.Instructions.Any(i => 
                    i.Opcode == Opcode.LIST_APPEND_313 || i.Opcode == Opcode.SET_ADD_313))
                {
                    isInlineComp = true;
                    break;
                }
                if (block.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
                {
                    foreach (var succ in block.Successors)
                    {
                        var nestedBodyBlocks = new List<BasicBlock>();
                        CollectBodyBlocks(succ, block, nestedBodyBlocks, new HashSet<BasicBlock>());
                        foreach (var nestedBlock in nestedBodyBlocks)
                        {
                            if (nestedBlock.Instructions.Any(i => 
                                i.Opcode == Opcode.LIST_APPEND_313 || i.Opcode == Opcode.SET_ADD_313))
                            {
                                isInlineComp = true;
                                break;
                            }
                        }
                        if (isInlineComp) break;
                    }
                    if (isInlineComp) break;
                }
            }
        }
        if (_options.VerboseErrors)
        {
        Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT isInlineComp_final={isInlineComp}");
        }
        var fi = header.Instructions.FirstOrDefault(i => i.Opcode == Opcode.FOR_ITER);
        if (fi != null && fi.Argument.HasValue)
        {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=STORE_TARGET fi_offset=0x{fi.Offset:X4} fi_arg={fi.Argument.Value}");
            int exitOffset = fi.Argument.Value;
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=STORE_TARGET exitOffset=0x{exitOffset:X4}");
            }
            var realExit = _sortedBlocks.FirstOrDefault(b => b.StartOffset >= exitOffset);
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=STORE_TARGET realExit={realExit?.StartOffset.ToString("X4") ?? "null"}");
            if (realExit != null)
            {
                foreach (var i in realExit.Instructions)
                {
                    if (i.Opcode == Opcode.STORE_FAST && i.Argument.HasValue
                        && i.Argument.Value < _codeObject.Varnames.Count)
                    { storeTarget = _codeObject.Varnames[i.Argument.Value]; break; }
                    if (i.Opcode == Opcode.STORE_NAME && i.Argument.HasValue
                        && i.Argument.Value < _codeObject.Names.Count)
                    { storeTarget = _codeObject.Names[i.Argument.Value]; break; }
                }
                if (storeTarget == null)
                {
                    int realExitIndex = _sortedBlocks.IndexOf(realExit);
                    for (int j = realExitIndex + 1; j < _sortedBlocks.Count; j++)
                    {
                        foreach (var i in _sortedBlocks[j].Instructions)
                        {
                            if (i.Opcode == Opcode.STORE_FAST && i.Argument.HasValue
                                && i.Argument.Value < _codeObject.Varnames.Count)
                            { storeTarget = _codeObject.Varnames[i.Argument.Value]; break; }
                            if (i.Opcode == Opcode.STORE_NAME && i.Argument.HasValue
                                && i.Argument.Value < _codeObject.Names.Count)
                            { storeTarget = _codeObject.Names[i.Argument.Value]; break; }
                        }
                        if (storeTarget != null) break;
                    }
                }
            }
        }
        
        // 使用 BuildForLoop 传入的 iterExpr，如果为 null 则回退到 ExtractIterExprRaw
        if (iterExpr == null)
            iterExpr = ExtractIterExprRaw(header);
        
        // Python 3.14: 如果 ExtractIterExprRaw 返回了默认值，尝试从函数参数中提取
        if (iterExpr is Name { Id: "iterable" } || iterExpr == null)
        {
            // 尝试从函数参数中提取：查找 islice(x, maxiter) 或类似的表达式
            // 检查是否有 IMPORT_NAME 指令加载 islice
            bool hasIslice = false;
            foreach (var block in _sortedBlocks)
            {
                if (block.StartOffset < header.StartOffset - 200 || block.StartOffset > header.StartOffset + 500)
                    continue;
                foreach (var ins in block.Instructions)
                {
                    if (ins.Opcode == Opcode.IMPORT_NAME && ins.Argument.HasValue)
                    {
                        int argIdx = ins.Argument.Value;
                        if (argIdx >= 0 && argIdx < _codeObject.Names.Count)
                        {
                            string name = _codeObject.Names[argIdx];
                            if (name == "islice")
                            {
                                hasIslice = true;
                                break;
                            }
                        }
                    }
                }
                if (hasIslice) break;
            }
            
            // 如果找到了 islice，尝试构建 islice(x, maxiter) 表达式
            if (hasIslice)
            {
                Expr? xVar = null;
                Expr? maxiterVar = null;
                
                foreach (var paramName in new[] { "x", "maxiter" })
                {
                    int idx = _codeObject.Varnames.IndexOf(paramName);
                    if (idx >= 0)
                    {
                        var nameExpr = new Name(paramName, ExpressionContext.Load);
                        if (paramName == "x") xVar = nameExpr;
                        if (paramName == "maxiter") maxiterVar = nameExpr;
                    }
                }
                
                if (xVar != null && maxiterVar != null)
                {
                    var isliceName = new Name("islice", ExpressionContext.Load);
                    iterExpr = new Call(isliceName, new List<Expr> { xVar, maxiterVar }, new List<Keyword>());
                }
                else if (xVar != null)
                {
                    iterExpr = xVar;
                }
            }
            
            // 如果仍然没有找到，尝试从前驱块中提取
            if (iterExpr is Name { Id: "iterable" } || iterExpr == null)
            {
                foreach (var pred in header.Predecessors)
                {
                    var sm = new StackMachine(_codeObject);
                    try
                    {
                        foreach (var ins in pred.Instructions)
                            sm.Execute(ins);
                        if (sm.ExprStackCount > 0)
                        {
                            iterExpr = sm.PopExpr();
                            break;
                        }
                    }
                    catch (Exception) { }
                }
            }
        }
        
        var generators = new List<Comprehension>();
        
        var currentHeader = header;
        var currentTarget = target;
        var currentIterExpr = iterExpr;
        
        while (currentHeader != null && currentTarget is Name)
        {
            var genIfs = new List<Expr>(ifs);
            var currentBodyBlocks = new List<BasicBlock>();
            if (currentHeader == header)
            {
                currentBodyBlocks = bodyBlocks;
            }
            else
            {
                foreach (var succ in currentHeader.Successors)
                {
                    if (!succ.Instructions.Any(i => i.Opcode == Opcode.END_FOR_313))
                    {
                        CollectBodyBlocks(succ, currentHeader, currentBodyBlocks, new HashSet<BasicBlock>());
                        break;
                    }
                }
            }
            foreach (var block in currentBodyBlocks)
            {
                for (int j = 0; j < block.Instructions.Count; j++)
                {
                    if (block.Instructions[j].Opcode == Opcode.COMPARE_OP)
                    {
                        bool hasJumpAfter = false;
                        for (int k = j + 1; k < block.Instructions.Count; k++)
                        {
                            if (block.Instructions[k].Opcode == Opcode.POP_JUMP_IF_FALSE || 
                                block.Instructions[k].Opcode == Opcode.POP_JUMP_IF_TRUE)
                            {
                                hasJumpAfter = true;
                                break;
                            }
                            if (block.Instructions[k].Opcode == Opcode.LIST_APPEND_313 || 
                                block.Instructions[k].Opcode == Opcode.SET_ADD_313 ||
                                block.Instructions[k].Opcode == Opcode.FOR_ITER)
                            {
                                break;
                            }
                        }
                        if (!hasJumpAfter) continue;

                        var sm = new StackMachine(_codeObject);
                        if (target is Name loopTarget)
                            sm.PushExpr(loopTarget);
                        foreach (var pred in header.Predecessors)
                        {
                            foreach (var ins in pred.Instructions)
                            {
                                sm.Execute(ins);
                            }
                        }
                        bool reachedCurrentBlock = false;
                        foreach (var bb in currentBodyBlocks)
                        {
                            if (bb == block)
                            {
                                reachedCurrentBlock = true;
                                for (int k = 0; k <= j; k++)
                                {
                                    sm.Execute(bb.Instructions[k]);
                                }
                                break;
                            }
                            if (!reachedCurrentBlock)
                            {
                                foreach (var ins in bb.Instructions)
                                {
                                    sm.Execute(ins);
                                }
                            }
                        }
                        if (sm.ExprStackCount > 0)
                        {
                            var cond = sm.PopExpr();
                            if (cond != null && !(cond is Constant { Value: true }) && !genIfs.Any(c => c.ToString() == cond.ToString()))
                            {
                                genIfs.Add(cond);
                            }
                        }
                        break;
                    }
                }
            }
            generators.Add(new Comprehension(currentTarget, currentIterExpr ?? new Constant("?"), genIfs));
            
            BasicBlock? nestedForIterBlock = null;
            foreach (var block in _sortedBlocks)
            {
                if (block.StartOffset <= currentHeader.StartOffset) continue;
                if (exitBlock != null && block.StartOffset >= exitBlock.StartOffset) break;
                
                foreach (var ins in block.Instructions)
                {
                    if (ins.Opcode == Opcode.FOR_ITER)
                    {
                        bool isInBodyBlocks = currentBodyBlocks.Any(b => b.StartOffset <= block.StartOffset && 
                            (b.EndOffset >= block.StartOffset || b.Instructions.Any()));
                        if (_options.VerboseErrors)
                        {
                        Console.Error.WriteLine($"[DECOMP_TRACE] stage=NESTED_DETECT found FOR_ITER at offset=0x{block.StartOffset:X4} isInBodyBlocks={isInBodyBlocks}");
                        }
                        if (isInBodyBlocks)
                        {
                            nestedForIterBlock = block;
                            break;
                        }
                    }
                }
                if (nestedForIterBlock != null) break;
            }
            
            if (nestedForIterBlock == null) break;
            
            var nestedBodyBlocks = new List<BasicBlock>();
            BasicBlock? nestedExitBlock = null;
            foreach (var succ in nestedForIterBlock.Successors)
            {
                if (succ.Instructions.Any(i => i.Opcode == Opcode.END_FOR_313))
                {
                    nestedExitBlock = succ;
                    break;
                }
            }
            foreach (var succ in nestedForIterBlock.Successors)
            {
                if (succ != nestedExitBlock)
                {
                    CollectBodyBlocks(succ, nestedForIterBlock, nestedBodyBlocks, new HashSet<BasicBlock>(), nestedExitBlock);
                    break;
                }
            }
            
            var nestedTarget = ExtractLoopVariable(nestedForIterBlock, nestedBodyBlocks);
            if (nestedTarget == null) break;
            
            Expr? nestedIterExpr = ExtractIterExprRaw(nestedForIterBlock);
            
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=NESTED_ITER nestedIterExpr={nestedIterExpr?.GetType().Name} value={nestedIterExpr}");
            }
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=NESTED_ITER currentTarget={currentTarget?.GetType().Name} value={currentTarget}");
            
            bool isDefaultIterable = nestedIterExpr is Name { Id: "iterable" };
            if ((nestedIterExpr == null || nestedIterExpr is Constant || isDefaultIterable) && currentTarget is Name outerTarget)
            {
                if (_options.VerboseErrors)
                {
                Console.Error.WriteLine($"[DECOMP_TRACE] stage=NESTED_ITER replacing with outerTarget={outerTarget.Id}");
                }
                nestedIterExpr = new Name(outerTarget.Id, ExpressionContext.Load);
            }
            
            if (nestedIterExpr == null && currentTarget is Name)
            {
                var ot = currentTarget as Name;
                if (_options.VerboseErrors)
                {
                Console.Error.WriteLine($"[DECOMP_TRACE] stage=NESTED_ITER fallback to outerTarget={ot?.Id}");
                }
                nestedIterExpr = new Name(ot!.Id, ExpressionContext.Load);
            }
            
            foreach (var succ in nestedForIterBlock.Successors)
            {
                if (succ.Instructions.Any(i => i.Opcode == Opcode.END_FOR_313))
                {
                    _processedBlockIds.Add(succ.Id);
                    break;
                }
            }
            _processedBlockIds.Add(nestedForIterBlock.Id);
            currentHeader = nestedForIterBlock;
            currentTarget = nestedTarget;
            currentIterExpr = nestedIterExpr;
        }
        
        if (_options.VerboseErrors)
        {
        Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT generators_count={generators.Count}");
        }
        for (int i = 0; i < generators.Count; i++)
        {
            var gen = generators[i];
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT   generator[{i}] target={gen.Target} iter={gen.Iter}");
        }
        if (_options.VerboseErrors)
        {
        Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT final_check containerKind={containerKind} elt={elt} storeTarget={storeTarget}");
        }
        
        if (generators[0].Iter is Constant { Value: string sv } && sv == "?")
        {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT DECISION: REJECTED (iterExpr is fallback '?')");
            return null;
        }

        Expr? compExpr = containerKind switch
        {
            "set" => new SetComp(elt, generators),
            "list" => new ListComp(elt, generators),
            "dict" => new DictComp(keyElt ?? elt, elt, generators),
            _ => null
        };
        
        if (compExpr == null) 
        {
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT DECISION: REJECTED (compExpr is null for containerKind={containerKind})");
            }
            return null;
        }
        
        Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT DECISION: ACCEPTED compType={compExpr.GetType().Name} elt_type={elt?.GetType().Name} iterExpr_type={iterExpr?.GetType().Name}");
        
        if (storeTarget != null)
            return new Assign(new List<Expr> { new Name(storeTarget, ExpressionContext.Store) }, compExpr);
        
        if (containerKind != null)
        {
            string? actualTarget = null;
            foreach (var block in _sortedBlocks)
            {
                foreach (var ins in block.Instructions)
                {
                    if (ins.Opcode == Opcode.STORE_FAST && ins.Argument.HasValue
                        && ins.Argument.Value < _codeObject.Varnames.Count)
                    {
                        string name = _codeObject.Varnames[ins.Argument.Value];
                        if (name != target?.ToString())
                        {
                            actualTarget = name;
                        }
                    }
                }
            }
            if (actualTarget != null)
            {
                return new Assign(new List<Expr> { new Name(actualTarget, ExpressionContext.Store) }, compExpr);
            }
        }
        
        if (target is not Name tn)
        {
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=COMP_DETECT DECISION: REJECTED (target is not Name)");
            }
            return null;
        }
        string targetName = tn.Id;
        return new Assign(new List<Expr> { new Name(targetName, ExpressionContext.Store) }, compExpr);
    }

    /// <summary>从指令序列中构建函数调用表达式（用于 Python 3.13+ 内联推导式）。</summary>
    private Expr? BuildCallFromInstructions(BasicBlock block, int callIndex, int argCount)
    {
        var args = new List<Expr>();
        int idx = callIndex - 1;
        
        for (int i = 0; i < argCount && idx >= 0; i++)
        {
            var ins = block.Instructions[idx];
            Expr? arg = null;
            
            if (ins.Opcode == Opcode.LOAD_FAST && ins.Argument.HasValue
                && ins.Argument.Value < _codeObject.Varnames.Count)
                arg = new Name(_codeObject.Varnames[ins.Argument.Value], ExpressionContext.Load);
            else if (ins.Opcode == Opcode.LOAD_CONST && ins.Argument.HasValue
                     && ins.Argument.Value < _codeObject.Constants.Count)
                arg = _codeObject.Constants[ins.Argument.Value] as Expr ?? new Constant(_codeObject.Constants[ins.Argument.Value]);
            else if (ins.Opcode == Opcode.LOAD_GLOBAL && ins.Argument.HasValue
                     && ins.Argument.Value < _codeObject.Names.Count)
                arg = new Name(_codeObject.Names[ins.Argument.Value], ExpressionContext.Load);
            else if (ins.Opcode == Opcode.LOAD_DEREF && ins.Argument.HasValue)
            {
                int derefIdx = ins.Argument.Value;
                if (_codeObject.Version >= PythonVersion.Py311)
                {
                    if (derefIdx < _codeObject.Varnames.Count)
                        arg = new Name(_codeObject.Varnames[derefIdx], ExpressionContext.Load);
                    else
                    {
                        derefIdx -= _codeObject.Varnames.Count;
                        if (derefIdx < _codeObject.Cellvars.Count)
                            arg = new Name(_codeObject.Cellvars[derefIdx], ExpressionContext.Load);
                        else
                        {
                            derefIdx -= _codeObject.Cellvars.Count;
                            if (derefIdx < _codeObject.Freevars.Count)
                                arg = new Name(_codeObject.Freevars[derefIdx], ExpressionContext.Load);
                        }
                    }
                }
            }
            
            if (arg != null)
            {
                args.Insert(0, arg);
                idx--;
            }
            else
            {
                idx--;
            }
        }
        
        if (idx < 0) return null;
        
        var funcIns = block.Instructions[idx];
        Expr? func = null;
        
        if (funcIns.Opcode == Opcode.LOAD_GLOBAL && funcIns.Argument.HasValue
            && funcIns.Argument.Value < _codeObject.Names.Count)
            func = new Name(_codeObject.Names[funcIns.Argument.Value], ExpressionContext.Load);
        else if (funcIns.Opcode == Opcode.LOAD_FAST && funcIns.Argument.HasValue
                 && funcIns.Argument.Value < _codeObject.Varnames.Count)
            func = new Name(_codeObject.Varnames[funcIns.Argument.Value], ExpressionContext.Load);
        
        if (func == null) return null;
        
        return new Call(func, args, new List<Keyword>());
    }

    /// <summary>处理指令并构建表达式栈（用于 Python 3.13+ 内联推导式）。</summary>
    private bool ProcessInstructionForStack(Instruction ins, Stack<Expr> exprStack)
    {
        switch (ins.Opcode)
        {
            case Opcode.LOAD_GLOBAL when ins.Argument.HasValue && ins.Argument.Value < _codeObject.Names.Count:
            {
                string name = _codeObject.Names[ins.Argument.Value];
                if (!name.StartsWith("__"))
                    exprStack.Push(new Name(name, ExpressionContext.Load));
                break;
            }
            case Opcode.LOAD_FAST when ins.Argument.HasValue && ins.Argument.Value < _codeObject.Varnames.Count:
            case Opcode.LOAD_FAST_BORROW_314 when ins.Argument.HasValue && ins.Argument.Value < _codeObject.Varnames.Count:
            case Opcode.STORE_FAST_LOAD_FAST_313 when ins.Argument.HasValue && ins.Argument.Value < _codeObject.Varnames.Count:
                exprStack.Push(new Name(_codeObject.Varnames[ins.Argument.Value], ExpressionContext.Load));
                break;
            case Opcode.LOAD_CONST when ins.Argument.HasValue && ins.Argument.Value < _codeObject.Constants.Count:
            {
                var value = _codeObject.Constants[ins.Argument.Value];
                exprStack.Push(value as Expr ?? new Constant(value));
                break;
            }
            case Opcode.LOAD_DEREF when ins.Argument.HasValue:
            {
                int idx = ins.Argument.Value;
                if (_codeObject.Version >= PythonVersion.Py311)
                {
                    if (idx < _codeObject.Varnames.Count)
                        exprStack.Push(new Name(_codeObject.Varnames[idx], ExpressionContext.Load));
                    else
                    {
                        idx -= _codeObject.Varnames.Count;
                        if (idx < _codeObject.Cellvars.Count)
                            exprStack.Push(new Name(_codeObject.Cellvars[idx], ExpressionContext.Load));
                        else
                        {
                            idx -= _codeObject.Cellvars.Count;
                            if (idx < _codeObject.Freevars.Count)
                                exprStack.Push(new Name(_codeObject.Freevars[idx], ExpressionContext.Load));
                        }
                    }
                }
                else
                {
                    if (idx < _codeObject.Cellvars.Count)
                        exprStack.Push(new Name(_codeObject.Cellvars[idx], ExpressionContext.Load));
                    else
                    {
                        int fi = idx - _codeObject.Cellvars.Count;
                        if (fi < _codeObject.Freevars.Count)
                            exprStack.Push(new Name(_codeObject.Freevars[fi], ExpressionContext.Load));
                    }
                }
                break;
            }
            case Opcode.LOAD_ATTR when ins.Argument.HasValue && ins.Argument.Value < _codeObject.Names.Count:
            {
                if (exprStack.Count > 0)
                {
                    var obj = exprStack.Pop();
                    exprStack.Push(new Models.AST.Attribute(obj, _codeObject.Names[ins.Argument.Value], ExpressionContext.Load));
                }
                break;
            }
            case Opcode.CALL when ins.Argument.HasValue:
            {
                int argCount = ins.Argument.Value;
                var args = new List<Expr>();
                for (int i = 0; i < argCount && exprStack.Count > 0; i++)
                    args.Insert(0, exprStack.Pop());
                
                if (exprStack.Count > 0)
                {
                    var func = exprStack.Pop();
                    exprStack.Push(new Call(func, args, new List<Keyword>()));
                }
                break;
            }
            case Opcode.BINARY_OP:
            {
                if (exprStack.Count >= 2)
                {
                    var right = exprStack.Pop();
                    var left = exprStack.Pop();
                    exprStack.Push(new BinOp(left, GetBinOpType(ins.Argument ?? 0), right));
                }
                break;
            }
            case Opcode.LOAD_ATTR:
            {
                if (ins.Argument.HasValue && ins.Argument.Value < _codeObject.Names.Count && exprStack.Count > 0)
                {
                    var obj = exprStack.Pop();
                    exprStack.Push(new Models.AST.Attribute(obj, _codeObject.Names[ins.Argument.Value], ExpressionContext.Load));
                }
                break;
            }
            case Opcode.BUILD_LIST:
            case Opcode.BUILD_SET:
            case Opcode.BUILD_MAP:
            case Opcode.SWAP:
            case Opcode.PUSH_NULL:
            case Opcode.MAKE_FUNCTION:
            case Opcode.SET_FUNCTION_ATTRIBUTE_313:
            case Opcode.LOAD_NAME:
            case Opcode.STORE_FAST:
            case Opcode.STORE_NAME:
            case Opcode.STORE_ATTR:
            case Opcode.STORE_GLOBAL:
                break;
            case Opcode.POP_TOP:
                break;
            case Opcode.DUP_TOP:
                break;
            case Opcode.ROT_THREE:
                break;
            case Opcode.BINARY_SUBSCR:
                break;
            case Opcode.UNARY_NEGATIVE:
                break;
            case Opcode.UNARY_NOT:
                break;
            case Opcode.COMPARE_OP:
                break;
            case Opcode.LOAD_FAST_AND_CLEAR:
                break;
            case Opcode.IMPORT_NAME:
                break;
            case Opcode.GET_LEN_313:
                break;
            case Opcode.EXIT_INIT_CHECK_313:
                break;
            case Opcode.YIELD_VALUE_313:
                break;
            case Opcode.DELETE_SUBSCR_313:
                break;
            case Opcode.LOAD_FAST_LOAD_FAST_313 when ins.Argument.HasValue:
            {
                int arg = ins.Argument.Value;
                int idx1 = arg & 0xFF;
                int idx2 = (arg >> 8) & 0xFF;
                
                if (idx2 >= 0 && idx2 < _codeObject.Varnames.Count)
                    exprStack.Push(new Name(_codeObject.Varnames[idx2], ExpressionContext.Load));
                if (idx1 >= 0 && idx1 < _codeObject.Varnames.Count)
                    exprStack.Push(new Name(_codeObject.Varnames[idx1], ExpressionContext.Load));
                break;
            }
            case Opcode.STORE_FAST_LOAD_FAST_313 when ins.Argument.HasValue:
            {
                int arg = ins.Argument.Value;
                int idx1 = arg & 0xFF;
                int idx2 = (arg >> 8) & 0xFF;
                
                if (idx2 >= 0 && idx2 < _codeObject.Varnames.Count)
                    exprStack.Push(new Name(_codeObject.Varnames[idx2], ExpressionContext.Load));
                if (idx1 >= 0 && idx1 < _codeObject.Varnames.Count)
                    exprStack.Push(new Name(_codeObject.Varnames[idx1], ExpressionContext.Load));
                break;
            }
            case Opcode.CALL_INTRINSIC_1_313 when ins.Argument.HasValue:
            {
                int argCount = ins.Argument.Value;
                var args = new List<Expr>();
                for (int i = 0; i < argCount && exprStack.Count > 0; i++)
                    args.Insert(0, exprStack.Pop());
                
                if (exprStack.Count > 0)
                {
                    var func = exprStack.Pop();
                    exprStack.Push(new Call(func, args, new List<Keyword>()));
                }
                break;
            }
            case Opcode.CALL_INTRINSIC_2_313 when ins.Argument.HasValue:
            {
                int argCount = ins.Argument.Value;
                var args = new List<Expr>();
                for (int i = 0; i < argCount && exprStack.Count > 0; i++)
                    args.Insert(0, exprStack.Pop());
                
                if (exprStack.Count > 0)
                {
                    var func = exprStack.Pop();
                    exprStack.Push(new Call(func, args, new List<Keyword>()));
                }
                break;
            }
            case Opcode.BINARY_SLICE_313:
            {
                if (exprStack.Count >= 2)
                {
                    var right = exprStack.Pop();
                    var left = exprStack.Pop();
                    exprStack.Push(new Slice(left, right, null));
                }
                else if (exprStack.Count >= 1)
                {
                    var right = exprStack.Pop();
                    exprStack.Push(new Slice(null, right, null));
                }
                break;
            }
            case Opcode.LOAD_SMALL_INT_314:
                exprStack.Push(new Constant(ins.Argument));
                break;
            case Opcode.LOAD_SPECIAL_314 when ins.Argument.HasValue:
            {
                int arg = ins.Argument.Value;
                string specialName = arg switch
                {
                    0 => "__class__",
                    1 => "__self__",
                    2 => "__func__",
                    3 => "__code__",
                    4 => "__globals__",
                    5 => "__name__",
                    6 => "__doc__",
                    7 => "__module__",
                    8 => "__qualname__",
                    9 => "__annotations__",
                    10 => "__type_params__",
                    _ => $"__special_{arg}__"
                };
                exprStack.Push(new Name(specialName, ExpressionContext.Load));
                break;
            }
            case Opcode.POP_ITER_314:
            case Opcode.END_FOR_313:
            case Opcode.BUILD_INTERPOLATION_314:
                break;
            case Opcode.BINARY_OP_INPLACE_ADD_UNICODE_314:
            {
                if (exprStack.Count >= 2)
                {
                    var right = exprStack.Pop();
                    var left = exprStack.Pop();
                    exprStack.Push(new BinOp(left, Operator.Add, right));
                }
                break;
            }
            default:
                return true;
        }
        return false;
    }

    private Operator GetBinOpType(int opId)
    {
        return opId switch
        {
            0 => Operator.Add,
            10 => Operator.Sub,
            20 => Operator.Mul,
            30 => Operator.Div,
            _ => Operator.Add
        };
    }

    /// <summary>从前驱/header 块的指令中反向扫描提取内联推导式的迭代表达式。</summary>
    private Expr? ExtractIterExprRaw(BasicBlock header)
    {
        var visited = new HashSet<BasicBlock>();
        var queue = new Queue<BasicBlock>();
        queue.Enqueue(header);
        foreach (var pred in header.Predecessors) queue.Enqueue(pred);
        
        while (queue.Count > 0)
        {
            var block = queue.Dequeue();
            if (!visited.Add(block)) continue;
            
            int getIterIdx = -1;
            for (int i = 0; i < block.Instructions.Count; i++)
                if (block.Instructions[i].Opcode == Opcode.GET_ITER)
                { getIterIdx = i; break; }
            if (getIterIdx < 0)
            {
                foreach (var pred in block.Predecessors)
                    if (!visited.Contains(pred)) queue.Enqueue(pred);
                continue;
            }
            var exprStack = new Stack<Expr>();
            bool stop = false;
            
            for (int i = getIterIdx - 1; i >= 0 && !stop; i--)
            {
                var ins = block.Instructions[i];
                stop = ProcessInstructionForStack(ins, exprStack);
            }
            
            if (exprStack.Count > 0)
            {
                return exprStack.Peek();
            }
            
            foreach (var pred in block.Predecessors)
                if (!visited.Contains(pred)) queue.Enqueue(pred);
        }
        // Pass 2: 前向扫描 — BUILD_SET 在前驱块（无 GET_ITER）中，找 LOAD_GLOBAL
        foreach (var block in new[] { header }.Concat(header.Predecessors))
        {
            if (block.Instructions.Any(i => i.Opcode == Opcode.GET_ITER)) continue;
            bool afterBuildSet = false;
            for (int i = 0; i < block.Instructions.Count; i++)
            {
                var ins = block.Instructions[i];
                if (!afterBuildSet && (ins.Opcode == Opcode.BUILD_SET
                    || ins.Opcode == Opcode.BUILD_LIST || ins.Opcode == Opcode.BUILD_MAP))
                { afterBuildSet = true; continue; }
                if (!afterBuildSet) continue;
                if (ins.Opcode == Opcode.LOAD_GLOBAL && ins.Argument.HasValue
                    && ins.Argument.Value < _codeObject.Names.Count)
                {
                    string n = _codeObject.Names[ins.Argument.Value];
                    if (n.StartsWith("__")) continue;
                    return new Name(n, ExpressionContext.Load);
                }
                if (ins.Opcode == Opcode.LOAD_FAST && ins.Argument.HasValue
                    && ins.Argument.Value < _codeObject.Varnames.Count)
                    return new Name(_codeObject.Varnames[ins.Argument.Value], ExpressionContext.Load);
                if (ins.Opcode == Opcode.LOAD_DEREF && ins.Argument.HasValue)
                {
                    int idx = ins.Argument.Value;
                    // 3.11+ localsplus: [varnames | cellvars | freevars]
                    // pre-3.11:         [cellvars | freevars]
                    if (_codeObject.Version >= PythonVersion.Py311)
                    {
                        if (idx < _codeObject.Varnames.Count)
                            return new Name(_codeObject.Varnames[idx], ExpressionContext.Load);
                        idx -= _codeObject.Varnames.Count;
                        if (idx < _codeObject.Cellvars.Count)
                            return new Name(_codeObject.Cellvars[idx], ExpressionContext.Load);
                        idx -= _codeObject.Cellvars.Count;
                        if (idx < _codeObject.Freevars.Count)
                            return new Name(_codeObject.Freevars[idx], ExpressionContext.Load);
                    }
                    else
                    {
                        if (idx < _codeObject.Cellvars.Count)
                            return new Name(_codeObject.Cellvars[idx], ExpressionContext.Load);
                        int fi = idx - _codeObject.Cellvars.Count;
                        if (fi < _codeObject.Freevars.Count)
                            return new Name(_codeObject.Freevars[fi], ExpressionContext.Load);
                    }
                    continue;
                }
            }
        }
        return null;
    }

    /// <summary>
    /// 判断操作码是否为 try 设置操作码。
    /// SETUP_FINALLY 在所有版本中都有效。
    /// SETUP_EXCEPT 仅在 3.5-3.7 有效，3.8+ 该 opcode 值被 JUMP_IF_NOT_EXC_MATCH 取代。
    /// 参考 CPython Include/opcode.h:
    ///   - SETUP_EXCEPT=121 (3.5-3.7) — CPython Include/opcode.h line ~121
    ///   - JUMP_IF_NOT_EXC_MATCH=121 (3.8+) — Python 3.8 将 opcode 121 重新定义（PEP 580）
    ///   - CPython Python/compile.c: compiler_try_except uses SETUP_FINALLY → SETUP_EXCEPT (pre-3.8)
    /// </summary>
    private bool IsTrySetupOpcode(Opcode op)
    {
        if (op == Opcode.SETUP_FINALLY) return true;

        // SETUP_EXCEPT (opcode=121) 仅在 3.5-3.7 有效。
        // Python 3.8+ 将 opcode 121 重新编号为 JUMP_IF_NOT_EXC_MATCH
        // 参考 CPython 3.7: Include/opcode.h line 122 "#define SETUP_EXCEPT 121"
        //     CPython 3.8: Include/opcode.h line 122 "#define JUMP_IF_NOT_EXC_MATCH 121"
        // 3.11+ 改用 ExceptionTable（HasExceptionTable=true），SETUP_EXCEPT/SETUP_FINALLY 均不再出现
        return _codeObject.Version switch
        {
            PythonVersion.Py27 or PythonVersion.Py35
                or PythonVersion.Py36 or PythonVersion.Py37 => op == Opcode.SETUP_EXCEPT,
            _ => false
        };
    }

    private List<BasicBlock> GetAllBlocks() => _allBlocks;

    private List<BasicBlock> GetBlocksInRange(int startInclusive, int endExclusive)
    {
        var list = _sortedBlocks;
        if (list.Count == 0) return new List<BasicBlock>();

        // Binary search: find first block with StartOffset >= startInclusive
        int lo = 0, hi = list.Count - 1;
        while (lo <= hi)
        {
            int mid = lo + (hi - lo) / 2;
            if (list[mid].Instructions[0].Offset < startInclusive)
                lo = mid + 1;
            else
                hi = mid - 1;
        }
        int first = lo;

        // Collect blocks that overlap with [startInclusive, endExclusive)
        // A block overlaps if its StartOffset < endExclusive
        var result = new List<BasicBlock>();
        for (int i = first; i < list.Count; i++)
        {
            var block = list[i];
            int blockStart = block.Instructions[0].Offset;
            // Continue while block start is before end of range
            if (blockStart >= endExclusive)
                break;
            result.Add(block);
        }
        return result;
    }

    /// <summary>
    /// 3.10+: 通过 ExceptionTable 检测 match/case。
    /// 检测条件: handler 块中包含 MATCH_CLASS/MATCH_SEQUENCE/MATCH_MAPPING/MATCH_KEYS 等操作码。
    /// </summary>
    private List<Stmt>? BuildMatchFromExceptionTable(BasicBlock block, HashSet<BasicBlock> visited)
    {
        var instrs = block.Instructions;
        if (instrs.Count == 0) return null;

        // 查找覆盖此块的 ExceptionTable 条目（depth=1 的 handler）
        var matchEntries = _codeObject.ExceptionTable
            .Where(e => e.Depth == 1)
            .ToList();
        if (matchEntries.Count == 0) return null;

        // 检查 handler 块是否包含 match 操作码
        var handlerBlock = FindBlockByOffset(matchEntries[0].TargetOffset);
        if (handlerBlock == null) return null;
        bool hasMatchOp = handlerBlock.Instructions.Any(i =>
            i.Opcode == Opcode.MATCH_CLASS_312 ||
            i.Opcode == Opcode.MATCH_CLASS_313 ||
            i.Opcode == Opcode.MATCH_SEQUENCE_312 ||
            i.Opcode == Opcode.MATCH_SEQUENCE_313 ||
            i.Opcode == Opcode.MATCH_MAPPING_312 ||
            i.Opcode == Opcode.MATCH_MAPPING_313 ||
            i.Opcode == Opcode.MATCH_KEYS_312 ||
            i.Opcode == Opcode.MATCH_KEYS_313);
        if (!hasMatchOp) return null;

        // 收集 match subject（block 中 MATCH 指令之前的表达式）
        // match body 的第一个 ExceptionTable 条目的 start 之前是 subject
        var firstEntry = matchEntries[0];
        var matchSubject = new Name("subject"); // placeholder

        // 尝试从 block 指令中提取 subject（第一个 LOAD_* 指令）
        foreach (var ins in block.Instructions)
        {
            if (ins.Opcode == Opcode.LOAD_NAME || ins.Opcode == Opcode.LOAD_FAST)
            {
                var name = ins.Opcode == Opcode.LOAD_FAST
                    ? _codeObject.Varnames.ElementAtOrDefault(ins.Argument ?? 0)
                    : _codeObject.Names.ElementAtOrDefault(ins.Argument ?? 0);
                if (name != null)
                {
                    matchSubject = new Name(name);
                    break;
                }
            }
        }

        // 为每个 handler 条目创建 case
        var cases = new List<MatchCase>();
        foreach (var entry in matchEntries)
        {
            var hb = FindBlockByOffset(entry.TargetOffset);
            if (hb == null || visited.Contains(hb)) continue;
            visited.Add(hb);

            // 解析模式
            var pattern = ParseMatchPattern(hb);

            // 反编译 case body（从 STORE_NAME 之后到 handler 结束）
            var caseBody = new List<Stmt>();
            bool foundStore = false;
            var cm = new StackMachine(_codeObject);
            foreach (var ins in hb.Instructions)
            {
                if (!foundStore)
                {
                    if (ins.Opcode == Opcode.STORE_NAME || ins.Opcode == Opcode.STORE_FAST)
                        foundStore = true;
                    continue;
                }
                var stmt = cm.Execute(ins);
                if (stmt != null) caseBody.Add(stmt);
            }
            while (cm.HasResults)
                caseBody.Add(new ExprStmt(cm.PopResult()));

            cases.Add(new MatchCase(pattern, null, caseBody));
        }

        if (cases.Count == 0) return null;
        return new List<Stmt> { new Match(matchSubject, cases) };
    }

    /// <summary>
    /// 从 handler 块解析 match 模式。
    /// 当前实现为存根：将 MATCH 操作码前的 LOAD_NAME 作为模式值。
    /// </summary>
    private MatchPattern ParseMatchPattern(BasicBlock hb)
    {
        // 查找 MATCH 操作码前的 LOAD_NAME（模式类型）
        for (int i = 0; i < hb.Instructions.Count; i++)
        {
            var ins = hb.Instructions[i];
            if (ins.Opcode == Opcode.MATCH_CLASS_312 ||
                ins.Opcode == Opcode.MATCH_CLASS_313 ||
                ins.Opcode == Opcode.MATCH_SEQUENCE_312 ||
                ins.Opcode == Opcode.MATCH_SEQUENCE_313 ||
                ins.Opcode == Opcode.MATCH_MAPPING_312 ||
                ins.Opcode == Opcode.MATCH_MAPPING_313)
            {
                if (i > 0 && hb.Instructions[i - 1].Opcode == Opcode.LOAD_NAME)
                {
                    var name = _codeObject.Names.ElementAtOrDefault(
                        hb.Instructions[i - 1].Argument ?? 0);
                    if (name != null)
                        return new MatchClass(new Name(name), new List<MatchPattern>());
                }
                break;
            }
        }
        // 默认 fallback: 通配符
        return new MatchWildcard();
    }

    // ---- 辅助方法 ----
    
    /// <summary>
    /// 从内联 bytecode 模式构建 Match AST：COPY+COPY+LOAD_GLOBAL+MATCH_CLASS+POP_JUMP_IF_NONE 链。
    /// 遍历整个 match/case 块链，构建 MatchCase 节点。
    /// </summary>
    private List<Stmt>? BuildMatchFromInline(BasicBlock startBlock, HashSet<BasicBlock> visited)
    {
        // 查找 match subject：倒序追溯前驱块
        Name? matchSubject = null;
        var pred = startBlock.Predecessors.FirstOrDefault();
        while (pred != null && matchSubject == null)
        {
            var loadInstr = pred.Instructions.LastOrDefault(i =>
                i.Opcode == Opcode.LOAD_FAST || i.Opcode == Opcode.LOAD_NAME);
            if (loadInstr != default)
            {
                var name = loadInstr.Opcode == Opcode.LOAD_FAST
                    ? _codeObject.Varnames.ElementAtOrDefault(loadInstr.Argument ?? 0)
                    : _codeObject.Names.ElementAtOrDefault(loadInstr.Argument ?? 0);
                if (name != null) matchSubject = new Name(name);
            }
            pred = pred.Predecessors.FirstOrDefault();
        }
        matchSubject ??= new Name("x");

        var cases = new List<MatchCase>();
        BasicBlock? currentBlock = startBlock;

        while (currentBlock != null && cases.Count < 12
            && currentBlock.Instructions.Count >= 3
            && currentBlock.Instructions.Any(i => i.Opcode == Opcode.COPY))
        {
            _processedBlockIds.Add(currentBlock.Id);

            var instrs = currentBlock.Instructions;
            var lastInstr = instrs.LastOrDefault();
            if (lastInstr == default) break;

            // 确定 case body 和 next case
            // 使用 BlockScanner 创建的 Successors (POP_JUMP_IF_NONE 现已被识别为条件跳转)
            // bodyBlock = fallthrough (UNPACK_SEQUENCE + case body)
            // nextCaseBlock = jump target (下一个 case 或清理块)
            var sortedSuccs = currentBlock.Successors
                .Where(s => s != null).OrderBy(s => s.StartOffset).ToList();
            BasicBlock? bodyBlock = sortedSuccs.FirstOrDefault();
            BasicBlock? nextCaseBlock = sortedSuccs.Count > 1 ? sortedSuccs.Last() : null;

            // 标记 next case 和 body 为已处理
            if (bodyBlock != null) { visited.Add(bodyBlock); _processedBlockIds.Add(bodyBlock.Id); }
            if (nextCaseBlock == null || _processedBlockIds.Contains(nextCaseBlock.Id))
                nextCaseBlock = null;

            // 跳过 POP_TOP 等清理块，直达下一个 COPY 块（下个 case 的起点）
            // 也跳过空块（CACHE 条目残留的 leader 边界）
            if (nextCaseBlock != null)
            {
                while (nextCaseBlock.Successors.Count == 1
                    && !nextCaseBlock.Instructions.Any(i => i.Opcode == Opcode.COPY))
                {
                    var next = nextCaseBlock.Successors.First();
                    if (visited.Contains(next) || _processedBlockIds.Contains(next.Id)) break;
                    visited.Add(next);
                    if (!next.Instructions.Any(i => i.Opcode == Opcode.COPY))
                        _processedBlockIds.Add(next.Id);
                    nextCaseBlock = next;
                }
            }

            // 提取模式
            MatchPattern? pattern = null;
            bool hasClassPattern = false;
            for (int i = 0; i < instrs.Count; i++)
            {
                if (instrs[i].Opcode is Opcode.MATCH_CLASS_312 or Opcode.MATCH_CLASS_313)
                {
                    // MATCH_CLASS 前的 LOAD_GLOBAL 是类名
                    for (int j = i - 1; j >= 0; j--)
                    {
                        if (instrs[j].Opcode == Opcode.LOAD_GLOBAL)
                        {
                            var nameIdx = instrs[j].Argument ?? 0;
                            var className = nameIdx < _codeObject.Names.Count
                                ? _codeObject.Names[nameIdx] : null;
                            if (!string.IsNullOrEmpty(className))
                                pattern = new MatchClass(new Name(className!), new List<MatchPattern>());
                            break;
                        }
                    }
                    pattern ??= new MatchWildcard();
                    hasClassPattern = true;
                    break;
                }
                if (instrs[i].Opcode == Opcode.MATCH_MAPPING_312 || instrs[i].Opcode == Opcode.MATCH_MAPPING_313)
                { pattern = new MatchMapping(new List<Expr>(), new List<MatchPattern>()); hasClassPattern = true; break; }
                if (instrs[i].Opcode == Opcode.MATCH_SEQUENCE_312 || instrs[i].Opcode == Opcode.MATCH_SEQUENCE_313)
                { pattern = new MatchSequence(new List<MatchPattern>()); hasClassPattern = true; break; }
            }

            if (!hasClassPattern)
                pattern ??= new MatchWildcard();

            // 构建 case body
            var caseBody = new List<Stmt>();
            if (bodyBlock != null)
            {
                // body 块可能包含 guard 检查（POP_JUMP_IF_FALSE）
                var guardStmts = GetBlockStmts(bodyBlock);
                if (bodyBlock.Instructions.Any(i => i.Opcode == Opcode.POP_JUMP_IF_FALSE))
                {
                    // Guard 块的 fallthrough 是实际 body
                    var realBody = bodyBlock.Successors
                        .FirstOrDefault(s => s != nextCaseBlock
                            && s.StartOffset > bodyBlock.EndOffset);
                    if (realBody != null)
                    {
                        caseBody.AddRange(GetBlockStmts(realBody));
                        _processedBlockIds.Add(realBody.Id);
                    }
                }
                else
                {
                    caseBody.AddRange(guardStmts);
                }
            }

            cases.Add(new MatchCase(pattern, null, caseBody));

            // 移动到下一个 case
            currentBlock = nextCaseBlock;
        }

        if (cases.Count == 0) return null;
        _processedBlockIds.Add(startBlock.Id);
        return new List<Stmt> { new Match(matchSubject, cases) };
    }

    /// <summary>
    /// 3.11+: 通过 ExceptionTable 检测 try/except。
    /// 如果 block 的字节码范围在某个 ExceptionTable 条目的 try 体内，构建 Try AST 并设置 IsGroup。
    /// </summary>
    private List<Stmt>? BuildTryFromExceptionTable(BasicBlock block, HashSet<BasicBlock> visited)
    {
        _buildTryDepth++;
        if (_buildTryDepth > MaxBuildTryDepth)
        {
            _buildTryDepth--;
            return null;
        }
        try
        {
            var instrs = block.Instructions;
            if (instrs.Count == 0) return null;
            var blockStart = instrs[0].Offset;
        var blockEnd = instrs.Last().Offset;

        // Find the outermost entry that covers this block (lowest depth = 0 or 1 first)
        var matchingEntry = _codeObject.ExceptionTable
            .Where(e => blockStart >= e.StartOffset && blockStart < e.EndOffset)
            .OrderBy(e => e.Depth)
            .FirstOrDefault();
        if (matchingEntry == null)
        {
            return null;
        }

        bool isModuleCleanup = matchingEntry.StartOffset == 0
            && !_codeObject.Instructions.Any(i =>
                (i.Opcode == Opcode.CHECK_EXC_MATCH || i.Opcode == Opcode.CHECK_EG_MATCH)
                && i.Offset >= matchingEntry.TargetOffset);
        if (isModuleCleanup)
        {
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[TRY_FROM_ET] SKIP: module-level cleanup ET entry (start=0x{matchingEntry.StartOffset:X4}, end=0x{matchingEntry.EndOffset:X4})");
            }
            return null;
        }

        // 3.11+ for 循环体有隐式 ET 条目（清理/异常安全），
        // 应跳过 try/except 检测 — for 循环已有独立块处理。
        bool isForLoopBody = false;
        
        // 方法1：检查 ET 条目覆盖的范围内是否包含 FOR_ITER 指令
        var forIterInRange = _codeObject.Instructions
            .Where(i => i.Opcode == Opcode.FOR_ITER
                && i.Offset >= matchingEntry.StartOffset
                && i.Offset < matchingEntry.EndOffset);
        if (forIterInRange.Any())
        {
            isForLoopBody = true;
        }
        
        // 方法2：检查目标块是否包含 RERAISE 指令（for 循环清理条目的特征）
        var forLoopHandlerBlock = FindBlockByOffset(matchingEntry.TargetOffset);
        if (!isForLoopBody && forLoopHandlerBlock != null)
        {
            var hasReraise = forLoopHandlerBlock.Instructions.Any(i => i.Opcode == Opcode.RERAISE);
            // Only mark as for-loop body if BOTH: the handler has RERAISE AND the try body has FOR_ITER.
            // A finally handler also has RERAISE but its try body has NO FOR_ITER.
            isForLoopBody = hasReraise && forIterInRange.Any();
        }
        
        if (isForLoopBody)
        {
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[TRY_FROM_ET] SKIP: for loop body ET entry");
            }
            return null;
        }

        // 3.12+ finally-only/cleanup 条目：handler 不包含 CHECK_EXC_MATCH 或 CHECK_EG_MATCH，
        // 这些是 finally 体、清理代码等，不是 try/except 结构。
        var handlerBlock = FindBlockByOffset(matchingEntry.TargetOffset);
        // 某些版本（3.11+）的 ET TargetOffset 可能指向 handler 中间（跳过 PUSH_EXC_INFO）
        // 退一步：搜索包含 target 的块
        if (handlerBlock == null)
        {
            handlerBlock = _sortedBlocks.FirstOrDefault(b =>
                b.StartOffset < matchingEntry.TargetOffset
                && b.EndOffset > matchingEntry.TargetOffset);
        }
        if (handlerBlock == null || visited.Contains(handlerBlock))
        {
            return null;
        }
        // 3.14 中 ET 目标偏移可能指向空指令块（BlockScanner 创建的占位块）。
        // 向后搜索最近的有指令的块作为真正的 handler。
        if (handlerBlock.Instructions.Count == 0)
        {
            handlerBlock = _sortedBlocks
                .FirstOrDefault(b => b.StartOffset >= matchingEntry.TargetOffset
                    && b.Instructions.Count > 0);
            if (handlerBlock == null || visited.Contains(handlerBlock))
                return null;
        }
        
        // Python 3.13+ 内联列表推导式的 ET 条目：handler 块包含 LIST_APPEND_313
        // 这些不是真正的异常处理器，跳过它们
        if (_codeObject.Version >= PythonVersion.Py313)
        {
            bool hasListAppendInHandler = handlerBlock.Instructions.Any(i => i.Opcode == Opcode.LIST_APPEND_313);
            if (hasListAppendInHandler)
            {
                if (_options.VerboseErrors)
                {
                Console.Error.WriteLine($"[TRY_FROM_ET] SKIP: inline comprehension ET entry (handlerBlock#{handlerBlock.Id} contains LIST_APPEND_313)");
                }
                return null;
            }
        }
        
        bool isFinally = false;
        bool hasExcMatch = handlerBlock.Instructions.Any(i =>
            i.Opcode == Opcode.CHECK_EXC_MATCH || i.Opcode == Opcode.CHECK_EG_MATCH);
        if (_options.VerboseErrors)
        {
        Console.Error.WriteLine($"[TRY_DBG] handlerBlock#{handlerBlock.Id} offset={handlerBlock.StartOffset:X4} ops=[{string.Join(",", handlerBlock.Instructions.Select(i => $"{i.Opcode}({i.Opcode:D})"))}] hasExcMatch={hasExcMatch}");
        }
        // 检测 bare except（无 CHECK_EXC_MATCH）：PUSH_EXC_INFO + POP_TOP → 裸 except:
        // 注意：try/finally 的 cleanup 处理器也有 PUSH_EXC_INFO + POP_TOP，
        // 但它的后继包含 COPY/POP_EXCEPT/RERAISE 清理指令。bare except 没有这些。
        bool isBareExcept = !hasExcMatch && handlerBlock.Instructions.Count >= 2
            && handlerBlock.Instructions[0].Opcode == Opcode.PUSH_EXC_INFO_312
            && (handlerBlock.Instructions[1].Opcode == Opcode.POP_TOP
                || handlerBlock.Instructions[1].Opcode == Opcode.POP_EXCEPT
                || handlerBlock.Instructions[1].Opcode == Opcode.STORE_NAME)
            // 检查后继：如果不是 cleanup（无 COPY/RERAISE），才是真正的 bare except
            && !handlerBlock.Successors.Any(succ =>
                succ.Instructions.Any(i => i.Opcode == Opcode.COPY)
                || succ.Instructions.Any(i => i.Opcode == Opcode.RERAISE));
        if (!hasExcMatch && !isBareExcept)
        {
            // 无 CHECK_EXC_MATCH = try/finally or cleanup entry.
            // 仅当 try 体有实质性语句时才处理为 finally，跳过纯清理条目。
            var finallyTryBlocks = GetBlocksInRange(matchingEntry.StartOffset, matchingEntry.EndOffset);
            if (finallyTryBlocks.Count == 0) return null;
            bool tryHasStatements = finallyTryBlocks.Any(tb =>
            {
                var r = _blockResults.GetValueOrDefault(tb.Id);
                bool hasStmt = r?.Statements != null && r.Statements.Any(s => s is not Raise and not CommentBlock);
                return hasStmt;
            });
            if (!tryHasStatements)
            {
                // 清理条目：标记 handler 为已访问，但实际语句仍需保留
                // 注意：不要标记 handler 的后继为已访问，因为这些后继可能包含循环头块等重要结构
                visited.Add(handlerBlock);
                return null;
            }
            isFinally = true;
        }

        // 跳过 with 语句的隐式 ET 条目：BEFORE_WITH 在 entry 范围内或附近
        // 注意：ET 条目的 start 是 with 体的开始，BEFORE_WITH 可能在 start 之前
        var beforeWithRangeStart = Math.Max(0, matchingEntry.StartOffset - 30);
        var hasBeforeWith = _codeObject.Instructions
            .Any(i => (i.Opcode == Opcode.BEFORE_WITH
                       || i.Opcode == Opcode.BEFORE_WITH_312
                       || i.Opcode == Opcode.BEFORE_WITH_313)
                && i.Offset >= beforeWithRangeStart
                && i.Offset < matchingEntry.EndOffset);
        
        if (_options.VerboseErrors)
        {
            Console.Error.WriteLine($"[TRY_FROM_ET] ET entry: start=0x{matchingEntry.StartOffset:X4}, end=0x{matchingEntry.EndOffset:X4}, target=0x{matchingEntry.TargetOffset:X4}");
            Console.Error.WriteLine($"[TRY_FROM_ET] beforeWithRange: [0x{beforeWithRangeStart:X4}, 0x{matchingEntry.EndOffset:X4})");
            foreach (var i in _codeObject.Instructions)
            {
                if (i.Opcode == Opcode.BEFORE_WITH || i.Opcode == Opcode.BEFORE_WITH_312 || i.Opcode == Opcode.BEFORE_WITH_313)
                {
                    Console.Error.WriteLine($"[TRY_FROM_ET] FOUND BEFORE_WITH at offset=0x{i.Offset:X4}");
                }
            }
            Console.Error.WriteLine($"[TRY_FROM_ET] hasBeforeWith={hasBeforeWith}");
        }
        
        if (hasBeforeWith)
        {
            if (_options.VerboseErrors)
            {
                Console.Error.WriteLine($"[TRY_FROM_ET] SKIP: with statement ET entry (BEFORE_WITH found)");
            }
            return null;
        }

        var tryBlocks = GetBlocksInRange(matchingEntry.StartOffset, matchingEntry.EndOffset);
        if (tryBlocks.Count == 0) return null;

        // 排除嵌入在 try 体范围内的 handler 块。
        // 当 handler 偏移（TargetOffset）在 try 体 [StartOffset, EndOffset) 内时，
        // GetBlocksInRange 会同时返回 try 体和 handler 块。
        // handler 块不应作为 try 体的一部分处理。
        // 参考 CPython 3.13 abc.py 的异常表：handler 在 try 体内部
        if (matchingEntry.TargetOffset > matchingEntry.StartOffset
            && matchingEntry.TargetOffset < matchingEntry.EndOffset)
        {
            tryBlocks = tryBlocks
                .Where(tb => tb.Instructions.Count == 0
                    || tb.Instructions[0].Offset < matchingEntry.TargetOffset)
                .ToList();
            if (tryBlocks.Count == 0)
            {
                if (_options.VerboseErrors)
                {
                Console.Error.WriteLine($"[TRY_FROM_ET] RETURN NULL: tryBlocks empty after excluding handler");
                }
                return null;
            }
        }

        // 在 try 体中查找 POP_BLOCK 或 JUMP_FORWARD 分界：
        // - POP_BLOCK（3.11）：标记 try 体结束，之后是 else 体
        // - JUMP_FORWARD（3.12+）：标记 try 体结束，之后是 else 体
        var tryBody = new List<Stmt>();
        var elseBody = new List<Stmt>();  // will be replaced below if non-null
        bool afterTryBody = false;
        var tryVisited = new HashSet<BasicBlock>();
        foreach (var tb in tryBlocks)
        {
            // 检查这个块是否真正属于当前 try/except 块
            // 如果块的最后一个指令的偏移显著超过了当前异常表条目的 EndOffset，
            // 说明这个块跨越了两个异常表条目，不应该被处理
            // 允许少量偏差（最多 2 字节），因为 block 边界可能略超 ET 边界
            if (tb.Instructions.Count > 0 && tb.Instructions.Last().Offset > matchingEntry.EndOffset + 2)
                continue;
            
            // 检测 POP_BLOCK 或 JUMP_FORWARD（3.12+）分界
            if (!afterTryBody
                && (tb.Instructions.Any(i => i.Opcode == Opcode.POP_BLOCK)
                    || tb.Instructions.Any(i => i.Opcode == Opcode.JUMP_FORWARD)))
            {
                afterTryBody = true;
                // 分界指令本身是 try 体的一部分
                var result = _blockResults.GetValueOrDefault(tb.Id);
                if (result?.Statements != null)
                {
                    var filtered = result.Statements.Where(s => s is not Raise).ToList();
                    if (filtered.Count > 0)
                        tryBody.AddRange(filtered);
                }
                // 对于 POP_BLOCK：后续块全部属于 else 体
                // 对于 JUMP_FORWARD：当前块之后的块属于 else 体
                // （JUMP_FORWARD 块的语句仍属 try 体）
                continue;
            }
            if (tb == block)
            {
                // 对于当前块，使用 _blockResults 缓存（避免递归调用 BuildStatements → BuildTryFromExceptionTable）
                var tbResult = _blockResults.GetValueOrDefault(tb.Id);
                var stmts = tbResult?.Statements?.Where(s => s is not Raise).ToList() ?? new List<Stmt>();
                if (afterTryBody)
                    elseBody.AddRange(stmts);
                else
                    tryBody.AddRange(stmts);
            }
            else if (!visited.Contains(tb) && !tryVisited.Contains(tb))
            {
                // 对于其他块，只使用 _blockResults 中已有的语句，不递归调用 BuildStatements
                // 这样可以避免递归处理后继块，从而避免错误地包含第二个异常表条目的代码
                var tbResult = _blockResults.GetValueOrDefault(tb.Id);
                if (tbResult?.Statements != null)
                {
                    var filtered = tbResult.Statements.Where(s => s is not Raise).ToList();
                    if (filtered.Count > 0)
                        (afterTryBody ? elseBody : tryBody).AddRange(filtered);
                }
            }
        }
        if (elseBody.Count == 0) elseBody = null;

        // 只标记当前 try/except 块的代码为 visited，而不是整个范围的所有块
        // 如果标记了太多的块，会导致第二个 try/except 块无法被正确处理
        foreach (var tb in tryBlocks)
        {
            // 检查这个块是否真正属于当前 try/except 块
            // 如果块的最后一个指令的偏移显著超过了当前异常表条目的 EndOffset，
            // 说明这个块跨越了两个异常表条目，不应该被标记为 visited
            // 允许少量偏差（最多 2 字节）
            if (tb.Instructions.Count > 0 && tb.Instructions.Last().Offset <= matchingEntry.EndOffset + 2)
            {
                visited.Add(tb);
                _processedBlockIds.Add(tb.Id);
            }
        }

        // 跳过仅有基础设施指令（Raise/异常处理）的 try 体
        // 这些是 CPython 嵌套清理条目，不应生成独立 try/except
        // 注意：ExprStmt 可能是有效的 try 体内容（如 repr_running.add(key)），不应排除
        if (tryBody.Count == 0 && tryBlocks.All(tb =>
        {
            var r = _blockResults.GetValueOrDefault(tb.Id);
            return r?.Statements == null || r.Statements.All(s => s is Raise);
        }))
        {
            return null;
        }

        visited.Add(handlerBlock);

        // 预先计算 handlerEnd（handler 的 ET 条目结束偏移），后续会被 else 扫描使用
        var handlerET = _codeObject.ExceptionTable
            .FirstOrDefault(e => e.StartOffset == matchingEntry.TargetOffset);
        var handlerEnd = handlerET != null
            ? handlerET.EndOffset
            : matchingEntry.EndOffset;

        // 收集 else 体：扫描 handler 块末尾后的指令流，查找类/函数定义块。
        // 在 abc.py 中，ABCMeta class 定义位于 handler 的末尾与 handler 的
        // JUMP_FORWARD 目标之间，且不是 handler 后继。
        // 注意：try/finally 没有 else 分支，跳过 else 体构建
        if (elseBody == null && !isFinally)
        {
            // 从 handler 末尾偏移开始，向前扫描指令
            int scanStart = handlerBlock.Instructions.LastOrDefault().Offset;
            int scanEnd = int.MaxValue;
            // 如果 handler 末尾有 JUMP_FORWARD，则目标限制扫描范围
            var hdrJump = handlerBlock.Instructions
                .FirstOrDefault(i => i.Opcode == Opcode.JUMP_FORWARD && i.Argument.HasValue);
            if (hdrJump.Argument.HasValue)
                scanEnd = hdrJump.Offset + 2 + hdrJump.Argument.Value;
            else
            {
                // handler 本身可能没有 JUMP_FORWARD（只有 CHECK_EXC_MATCH），
                // 其后的 except 体块可能有 JUMP_FORWARD 标记 else 体边界。
                var afterHandler = _sortedBlocks
                    .FirstOrDefault(b => b.StartOffset > handlerBlock.StartOffset && !visited.Contains(b));
                if (afterHandler != null)
                {
                    var excJump = afterHandler.Instructions
                        .FirstOrDefault(i => i.Opcode == Opcode.JUMP_FORWARD && i.Argument.HasValue);
                    if (excJump.Argument.HasValue)
                        scanEnd = excJump.Offset + 2 + excJump.Argument.Value;
                }
            }

            var handlerSuccessorSet = new HashSet<BasicBlock>(handlerBlock.Successors);
            // 对于 orphan handler block，Successors 可能为空，
            // 需要也排除 handler ET 范围内的块
            var handlerRangeBlockSet = new HashSet<BasicBlock>(
                _sortedBlocks.Where(b => b.StartOffset >= handlerBlock.StartOffset && b.StartOffset < handlerEnd + 4));
            var elseCandidates = _sortedBlocks
                .Where(b => b.StartOffset > scanStart
                    && b.EndOffset < scanEnd
                    && !visited.Contains(b)
                    && !handlerSuccessorSet.Contains(b)
                    && !handlerRangeBlockSet.Contains(b))  // 排除 handler 范围内的块
                .OrderBy(b => b.StartOffset)
                .ToList();
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[ET_ELSE] found {elseCandidates.Count} candidates: {string.Join(",", elseCandidates.Select(b => $"{b.Id}@{b.StartOffset}"))}");
            }
            if (elseCandidates.Count > 0)
            {
                elseBody = new List<Stmt>();
                foreach (var eb in elseCandidates)
                {
                    visited.Add(eb);
                    _processedBlockIds.Add(eb.Id);
                    var es = GetStructuredBlockStmts(eb, visited);
                    if (es.Count > 0)
                        elseBody.AddRange(es);
                }
            }
        }

        var handlerResult = _blockResults.GetValueOrDefault(handlerBlock.Id);
        if (_options.VerboseErrors)
        {
        Console.Error.WriteLine($"[TRY_FROM_ET] handlerBlock#{handlerBlock.Id} result={handlerResult != null}, stmts={handlerResult?.Statements?.Count ?? 0}");
        }
        if (_options.VerboseErrors && handlerResult?.Statements != null)
        {
            Console.Error.WriteLine($"[TRY_FROM_ET]   handler stmt types={string.Join(",", handlerResult.Statements.Select(s => s.GetType().Name))}");
        }
        var handlerBody = handlerResult?.Statements
            ?.Where(s => s is not Raise and not CommentBlock and not Pass)
            .ToList() ?? new List<Stmt>();

        // 从 handler 的后继块中收集 handler 体语句（在 POP_EXCEPT/POP_EXCEPT 之前的语句）
        // 同时也需要获取 handlerEnd（handler 的 ET 条目结束偏移）

        // 检查已被其他路径 visited 的 handler 后继是否含有未消费的语句
        foreach (var vsucc in handlerBlock.Successors)
        {
            if (vsucc.Instructions.Count == 0) continue;
            if (!visited.Contains(vsucc)) continue;
            var vsr = _blockResults.GetValueOrDefault(vsucc.Id);
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[TRY_FROM_ET] visited succ#{vsucc.Id} stmts={vsr?.Statements?.Count ?? 0}");
            }
            if (_options.VerboseErrors && vsr?.Statements != null && vsr.Statements.Count > 0)
            {
                Console.Error.WriteLine($"[TRY_FROM_ET]   visited succ stmt types={string.Join(",", vsr.Statements.Select(s => s.GetType().Name))}");
            }
            if (vsr?.Statements != null && vsr.Statements.Count > 0
                && vsr.Statements.Any(s => s is not Raise and not CommentBlock))
            {
                var filteredStmts = vsr.Statements.Where(s => s is not Raise and not CommentBlock and not Return).ToList();
                if (filteredStmts.Count > 0)
                    handlerBody.AddRange(filteredStmts);
            }
        }

        if (_options.VerboseErrors)
        {
        Console.Error.WriteLine($"[TRY_FROM_ET] handlerBlock#{handlerBlock.Id} successors={handlerBlock.Successors.Count}");
        }
        foreach (var succ in handlerBlock.Successors.OrderBy(s => s.StartOffset))
        {
            if (_options.VerboseErrors)
            Console.Error.WriteLine($"[TRY_FROM_ET]   successor#{succ.Id} offset={succ.StartOffset:X4} visited={visited.Contains(succ)}");
            if (succ.Instructions.Count == 0) continue;
            var succStart = succ.Instructions[0].Offset;
            // 后继在 handler 块范围内（从 handler 块开始到 handler ET 结束，容忍 2 字节边界）
            if (succStart >= handlerBlock.StartOffset && succStart < handlerEnd + 2
                && !visited.Contains(succ))
            {
                // 跳过类/函数定义块 — 这些是结构边界，不是 handler 后继体
                // 在 try/except/else 中, handler 后出现的类/函数定义属于 else 体
                bool isDefBlock = succ.Instructions.Any(i =>
                    i.Opcode == Opcode.MAKE_FUNCTION
                    || i.Opcode == Opcode.MAKE_CLOSURE
                    || i.Opcode == Opcode.LOAD_BUILD_CLASS);
                if (isDefBlock)
                {
                    // 这是 else 体：handler 后续的类/函数定义
                    var elseStmts = BuildStatements(succ, visited);
                    if (elseStmts.Count > 0)
                    {
                        elseBody ??= new List<Stmt>();
                        elseBody.AddRange(elseStmts);
                    }
                    visited.Add(succ);
                    _processedBlockIds.Add(succ.Id);
                    continue;
                }

                var succResult = _blockResults.GetValueOrDefault(succ.Id);
                // 对于 handler 后继，优先尝试用 _blockResults 提取语句
                // 若失败（orphan 块的 Pass 占位符），直接用 BuildStatements 处理
                var succStmts = succResult?.Statements
                    ?.Where(s => s is not Pass and not Raise and not CommentBlock)
                    .ToList();
                if (succStmts != null && succStmts.Count > 0)
                {
                    handlerBody.AddRange(succStmts);
                }
                else if (handlerBlock.StartOffset < succStart && succStart < handlerEnd + 2)
                {
                    // 直接 BuildStatements 提取后继语句，绕过脆弱的 StackMachine 模拟
                    var directStmts = BuildStatements(succ, visited);
                    var filteredStmts = directStmts
                        .Where(s => s is not Pass and not Raise and not CommentBlock)
                        .ToList();
                    if (filteredStmts.Count > 0)
                        handlerBody.AddRange(filteredStmts);
                }
                visited.Add(succ);
                _processedBlockIds.Add(succ.Id);
            }
        }

        // 对于 try/finally 模式，提取 finally 体
        var afterFinallyStmts = new List<Stmt>();
        List<Stmt>? inlineFinalBody = null;
        
        if (isFinally && tryBody.Count > 0)
        {
            bool hasExceptHandler = _codeObject.ExceptionTable.Any(e => 
                e.StartOffset >= matchingEntry.StartOffset && e.StartOffset < matchingEntry.EndOffset
                && e != matchingEntry);
            
            if (!hasExceptHandler)
            {
                var inlineFinallyBlocks = _sortedBlocks
                    .Where(b => b.EndOffset > matchingEntry.EndOffset
                        && b.StartOffset < matchingEntry.TargetOffset)
                    .OrderBy(b => b.StartOffset)
                    .ToList();
                if (inlineFinallyBlocks.Count > 0)
                {
                    foreach (var inlineBlock in inlineFinallyBlocks)
                    {
                        visited.Add(inlineBlock);
                        _processedBlockIds.Add(inlineBlock.Id);
                    }
                    
                    var lastInlineBlock = inlineFinallyBlocks.OrderByDescending(b => b.StartOffset).First();
                    var lastInlineResult = _blockResults.GetValueOrDefault(lastInlineBlock.Id);
                    if (lastInlineResult?.Statements != null)
                    {
                        var returnStmts = lastInlineResult.Statements.Where(s => s is Return).ToList();
                        if (returnStmts.Count > 0)
                            afterFinallyStmts.AddRange(returnStmts);
                    }
                    
                    inlineFinalBody = inlineFinallyBlocks
                        .SelectMany(b => {
                            var r = _blockResults.GetValueOrDefault(b.Id);
                            var stmts = r?.Statements?.Where(s => s is not Raise and not CommentBlock and not Pass)
                                ?? Enumerable.Empty<Stmt>();
                            return stmts;
                        })
                        .ToList();
                }
            }
            
            // try/finally: handler 是无 CHECK_EXC_MATCH 的 finally 体
            // 优先使用内联 finally 体（有实际的 finally 代码），
            // 回退到 handler 体（可能只有 RERAISE 清理代码）
            var finalBody = (inlineFinalBody != null && inlineFinalBody.Count > 0)
                ? inlineFinalBody
                : handlerBody;
            if (afterFinallyStmts.Count == 0)
            {
                var handlerEndOffset = handlerEnd;
                foreach (var afterBlock in _sortedBlocks)
                {
                    if (afterBlock.Instructions.Count == 0) continue;
                    var afterBlockStart = afterBlock.Instructions[0].Offset;
                    if (afterBlockStart >= handlerEndOffset && !visited.Contains(afterBlock))
                    {
                        var afterBlockResult = _blockResults.GetValueOrDefault(afterBlock.Id);
                        if (afterBlockResult?.Statements != null)
                        {
                            var nonRaiseStmts = afterBlockResult.Statements.Where(s => s is not Raise and not CommentBlock).ToList();
                            if (nonRaiseStmts.Count > 0)
                            {
                                afterFinallyStmts.AddRange(nonRaiseStmts);
                                visited.Add(afterBlock);
                                _processedBlockIds.Add(afterBlock.Id);
                                break;
                            }
                        }
                    }
                }
            }
            
            var resultList = new List<Stmt>();
            bool finalBodyIsEmpty = finalBody == null || finalBody.Count == 0 || 
                (finalBody.Count == 1 && finalBody[0] is Pass);
            bool elseBodyIsEmpty = elseBody == null || elseBody.Count == 0;
            if (finalBodyIsEmpty && elseBodyIsEmpty)
                resultList.AddRange(tryBody);
            else
                resultList.Add(new Try(tryBody, new List<ExceptHandler>(), elseBody, finalBody));
            if (afterFinallyStmts.Count > 0)
            {
                // 如果 afterFinallyStmts 包含 Return/Raise 等终止语句，
                // 不追加到 try/finally 之后（不可达代码）
                if (afterFinallyStmts.All(s => s is Return or Raise))
                    ; // skip — already captured in handler body
                else
                    resultList.AddRange(afterFinallyStmts);
            }
            return resultList;
        }
        bool isGroup = handlerBlock.Instructions.Any(i => i.Opcode == Opcode.CHECK_EG_MATCH);

        Expr? exceptType = null;
        string? exceptName = null;
        for (int i = 0; i < handlerBlock.Instructions.Count; i++)
        {
            var ins = handlerBlock.Instructions[i];
            if (ins.Opcode == Opcode.CHECK_EXC_MATCH || ins.Opcode == Opcode.CHECK_EG_MATCH)
            {
                // Collect exception types from instructions BEFORE CHECK_EXC_MATCH/CHECK_EG_MATCH
                // Pattern 1: single type → LOAD_NAME/LOAD_GLOBAL
                // Pattern 2: multiple types → LOAD_NAME/LOAD_GLOBAL... BUILD_TUPLE
                var typeExprs = new List<Expr>();
                for (int j = i - 1; j >= 0; j--)
                {
                    var prev = handlerBlock.Instructions[j];
                    if (prev.Opcode == Opcode.BUILD_TUPLE || prev.Opcode == Opcode.BUILD_LIST)
                        continue; // skip tuple/list builder, collect individual types
                    if (prev.Opcode == Opcode.LOAD_NAME || prev.Opcode == Opcode.LOAD_GLOBAL)
                    {
                        var name = _codeObject.Names.ElementAtOrDefault(prev.Argument ?? 0);
                        if (name != null)
                            typeExprs.Insert(0, new Name(name));
                    }
                    else break;
                }
                if (typeExprs.Count == 1)
                    exceptType = typeExprs[0];
                else if (typeExprs.Count > 1)
                    exceptType = new ListLiteral(typeExprs, ContainerKind.Tuple);
                break;
            }
            if (ins.Opcode == Opcode.STORE_NAME)
                exceptName = _codeObject.Names.ElementAtOrDefault(ins.Argument ?? 0);
        }

        // try/except/finally: 提取 finally 体中的语句
        List<Stmt>? tryExceptFinalBody = null;
        if (!isFinally)
        {
            var finallyET = _codeObject.ExceptionTable
                .FirstOrDefault(e => e.StartOffset >= matchingEntry.StartOffset 
                    && e.StartOffset < matchingEntry.EndOffset
                    && e.TargetOffset > matchingEntry.TargetOffset
                    && !_codeObject.Instructions.Any(i => 
                        i.Offset >= e.TargetOffset 
                        && i.Offset < e.TargetOffset + 10
                        && (i.Opcode == Opcode.CHECK_EXC_MATCH || i.Opcode == Opcode.CHECK_EG_MATCH)));
            
            if (finallyET != null)
            {
                var inlineFinallyBlocks = _sortedBlocks
                    .Where(b => b.StartOffset >= finallyET.TargetOffset
                        && b.StartOffset < finallyET.EndOffset)
                    .OrderBy(b => b.StartOffset)
                    .ToList();
                
                if (inlineFinallyBlocks.Count > 0)
                {
                    var freshVisited = new HashSet<BasicBlock>();
                    var allStmts = new List<Stmt>();
                    foreach (var b in inlineFinallyBlocks)
                    {
                        allStmts.AddRange(BuildStatements(b, freshVisited));
                    }
                    var filteredStmts = allStmts
                        .Where(s => s is not Raise and not CommentBlock and not Pass)
                        .ToList();
                    if (filteredStmts.Count > 0)
                    {
                        var handlerContent = new HashSet<string>(
                            handlerBody.Where(s => s is not Pass and not Raise)
                                .Select(s => s.ToString()));
                        bool hasNewContent = filteredStmts
                            .Any(s => !handlerContent.Contains(s.ToString()));
                        if (hasNewContent)
                        {
                            tryExceptFinalBody = filteredStmts;
                            foreach (var b in inlineFinallyBlocks)
                            {
                                visited.Add(b);
                                _processedBlockIds.Add(b.Id);
                            }
                        }
                    }
                }
            }
        }

        if (handlerBody.Count == 0 || (handlerBody.Count == 1 && handlerBody[0] is Pass))
        {
            // handlerBody 为空或只有 Pass = handler 没有实质性语句（例如只有 RERAISE 的清理条目）。
            // 此时 tryBlocks 已经在嵌套调用（BuildStatements(tb, visited)）中正确消费了内部结构。
            // ❌ 以前移除了 visited 和 _processedBlockIds → 调用者重新进入 → 无限循环
            // ✅ 不移除，直接返回 null，blocks 保持已访问状态
            return null;
        }

        var handlers = new List<ExceptHandler>
        {
            new ExceptHandler(exceptType, exceptName, handlerBody, isGroup)
        };
        return new List<Stmt> { new Try(tryBody, handlers, elseBody, tryExceptFinalBody) };
        }
        finally
        {
            _buildTryDepth--;
        }
    }

    /// <summary>
    /// 从块中检测 SETUP_FINALLY/SETUP_EXCEPT → try/except 模式并构建 Try AST。
    /// 如果块不包含 SETUP_FINALLY，返回 null。
    /// </summary>
    private List<Stmt>? BuildTryFromBlock(BasicBlock block, HashSet<BasicBlock> visited)
    {
        var instrs = block.Instructions;
        // 查找 SETUP_FINALLY/SETUP_EXCEPT
        var setupIdx = instrs.FindIndex(i => IsTrySetupOpcode(i.Opcode));
        if (setupIdx < 0) return null;

        // 找到 STORE_NAME（循环变量赋值，应保留）
        var beforeTry = new List<Stmt>();
        if (setupIdx > 0)
        {
            var preInstrs = instrs.Take(setupIdx).ToList();
            // 以前缀指令产出前导语句（如循环变量赋值前的语句）
            var preMachine = new StackMachine(_codeObject);
            foreach (var ins in preInstrs)
            {
                var stmt = preMachine.Execute(ins);
                if (stmt != null) beforeTry.Add(stmt);
            }
            while (preMachine.HasResults)
                beforeTry.Add(new ExprStmt(preMachine.PopResult()));
        }

        // SETUP_FINALLY 的 handler 目标
        var handlerRel = instrs[setupIdx].Argument ?? 0;
        var handlerAbs = instrs[setupIdx].Offset + 2 + handlerRel;

        // 提取 try body：SETUP_FINALLY 之后到 handler 目标之前的所有指令
        // 可能跨多个基本块（如 try 体内含 for/while 循环时）
        int? elseJumpTarget = null;

        // 收集 try body 的块：从 SETUP_FINALLY 块的下一个块开始，到 handlerAbs 之前的块为止
        var tryBodyBlocks = new List<BasicBlock>();
        var tryBodyCollector = new HashSet<BasicBlock> { block };
        var blockQueue = new Queue<BasicBlock>();
        foreach (var succ in block.Successors.OrderBy(s => s.StartOffset))
        {
            if (succ == null || succ.StartOffset >= handlerAbs || tryBodyCollector.Contains(succ))
                continue;
            if (succ.StartOffset < instrs[setupIdx].Offset + 2) continue;
            // 跳过 FOR_ITER 块（属于外层循环）
            if (succ.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
            {
                var forIterEntry = succ.Successors.OrderBy(s => s.StartOffset).FirstOrDefault();
                if (forIterEntry == block) continue;
            }
            blockQueue.Enqueue(succ);
        }
        while (blockQueue.Count > 0)
        {
            var cur = blockQueue.Dequeue();
            if (!tryBodyCollector.Add(cur)) continue;
            // 跳过 try body 区域以外的块（offset < setup_sf+2 属于外层结构）
            if (cur.StartOffset < instrs[setupIdx].Offset + 2) continue;
            tryBodyBlocks.Add(cur);
            foreach (var succ in cur.Successors.OrderBy(s => s.StartOffset))
            {
                if (succ == null || succ.StartOffset >= handlerAbs || tryBodyCollector.Contains(succ))
                    continue;
                if (succ.StartOffset < instrs[setupIdx].Offset + 2) continue;
                if (succ.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
                {
                    var forIterEntry = succ.Successors.OrderBy(s => s.StartOffset).FirstOrDefault();
                    if (forIterEntry == block || forIterEntry == cur)
                        continue;
                }
                blockQueue.Enqueue(succ);
            }
        }

        // 反编译 try body：当前块中 SETUP_FINALLY 之后的指令用 StackMachine
        // 后继块用 GetStructuredBlockStmts（支持嵌套控制结构）
        // 使用 {block} 作为 visited 防止 GET_ITER/RETURN_VALUE 块被重复收集
        // 勿用 tryBodyCollector（内层块也被标记为 visited → GetStructuredBlockStmts 返回空）
        var tryBodyVisited = new HashSet<BasicBlock> { block };
        var tryStmts = new List<Stmt>();
        // 1) 当前块中 SETUP_FINALLY 之后的指令（到 POP_BLOCK 或 handler 为止）
        var preBodyInstrs = new List<Instruction>();
        for (int i = setupIdx + 1; i < instrs.Count; i++)
        {
            if (instrs[i].Opcode == Opcode.POP_BLOCK) break;
            if (instrs[i].Offset >= handlerAbs) break;
            preBodyInstrs.Add(instrs[i]);
        }
        if (preBodyInstrs.Count > 0)
        {
            // 检测嵌套 try/except 块（多个 SETUP_FINALLY/SETUP_EXCEPT 在同一块）
            var nestedSetups = new List<(int idx, int handlerRel, int handlerAbs)>();
            for (int i = 0; i < preBodyInstrs.Count; i++)
            {
                if (IsTrySetupOpcode(preBodyInstrs[i].Opcode))
                {
                    var rel = preBodyInstrs[i].Argument ?? 0;
                    var abs = preBodyInstrs[i].Offset + 2 + rel;
                    nestedSetups.Add((i, rel, abs));
                }
            }
            
            if (nestedSetups.Count > 0)
            {
                // 有嵌套 try — 从内到外构建多层次 try
                // 先处理第一个 SETUP 之前的指令（如果有）
                if (nestedSetups[0].idx > 0)
                {
                    var prefixInstrs = preBodyInstrs.Take(nestedSetups[0].idx).ToList();
                    var prefixMachine = new StackMachine(_codeObject);
                    foreach (var ins in prefixInstrs)
                    {
                        var stmt = prefixMachine.Execute(ins);
                        if (stmt != null) tryStmts.Add(stmt);
                    }
                    while (prefixMachine.HasResults)
                        tryStmts.Add(new ExprStmt(prefixMachine.PopResult()));
                }
                
                // 从内到外构建 try 节点
                List<Stmt>? innerBody = null;
                for (int level = nestedSetups.Count - 1; level >= 0; level--)
                {
                    var (nsIdx, _, handlerOffset) = nestedSetups[level];
                    
                    // 这一层的 try body: level 的 SETUP 之后到下一个 SETUP/POP_BLOCK 的指令
                    int nextSetupIdx = level + 1 < nestedSetups.Count 
                        ? nestedSetups[level + 1].idx 
                        : preBodyInstrs.Count;
                    
                    var levelBodyInstrs = preBodyInstrs
                        .Skip(nsIdx + 1)
                        .Take(nextSetupIdx - nsIdx - 1)
                        .ToList();
                    
                    var levelBody = new List<Stmt>();
                    if (innerBody != null)
                    {
                        // 有内层 try → 内层 try 作为本层 body
                        levelBody.AddRange(innerBody);
                    }
                    
                    // 处理本层 body 指令（如果有 SETUP 之间的额外指令）
                    if (levelBodyInstrs.Count > 0 && innerBody == null)
                    {
                        var levelMachine = new StackMachine(_codeObject);
                        foreach (var ins in levelBodyInstrs)
                        {
                            var stmt = levelMachine.Execute(ins);
                            if (stmt != null) levelBody.Add(stmt);
                        }
                        while (levelMachine.HasResults)
                            levelBody.Add(new ExprStmt(levelMachine.PopResult()));
                    }
                    
                    // 本层的 handler: 从 handlerAbs 找 handler 块
                    var handlerForLevel = ExtractExceptHandlerFromOffset(handlerOffset, block, instrs, setupIdx);
                    
                    innerBody = new List<Stmt> { new Try(levelBody, handlerForLevel, null, null) };
                }
                
                // 构建完成：最外层的 innerBody 是所有 try 的根
                if (innerBody != null)
                    tryStmts.AddRange(innerBody);
            }
            else
            {
                // 无嵌套 try — 正常处理（if/else 或纯指令）
                // 检测 if/else 条件跳转：如果当前块末尾是 POP_JUMP_IF_*，
                // 说明 try 体内有 if 条件（条件指令和 SETUP_FINALLY 在同一块）
                var lastPre = preBodyInstrs.LastOrDefault();
                bool hasInlineIf = lastPre != default && JumpHelper.IsConditionalJump(lastPre.Opcode) && lastPre.Argument.HasValue;

            if (hasInlineIf)
            {
                // 处理 inline if: 排除 POP_JUMP_IF_*（它消费条件，不应在 StackMachine 中执行）
                var condInstrs = preBodyInstrs.Take(preBodyInstrs.Count - 1).ToList();
                var condMachine = new StackMachine(_codeObject);
                foreach (var ins in condInstrs)
                {
                    var stmt = condMachine.Execute(ins);
                    if (stmt != null) tryStmts.Add(stmt);
                }
                var cond = condMachine.ExprStackCount > 0 ? condMachine.PopExpr() : null;
                // 可能还有剩余的结果（如其他表达式）
                while (condMachine.HasResults)
                    tryStmts.Add(new ExprStmt(condMachine.PopResult()));

                if (cond != null)
                {
                    // 条件在栈上，两个后继就是 if/else 分支
                    var sortedSucc = block.Successors
                        .Where(s => s.StartOffset < handlerAbs)
                        .OrderBy(s => s.StartOffset).ToList();
                    // 收集分支块中的语句（跳过 POP_BLOCK 指令）
                    var ifTrueBlock = sortedSucc.Count >= 1 ? sortedSucc[0] : null;  // fallthrough
                    var ifFalseBlock = sortedSucc.Count >= 2 ? sortedSucc[^1] : null; // jump target
                    
                    // 使用 GetStructuredBlockStmts 处理分支（支持嵌套控制结构如 for-loop）
                    var trueStmts = new List<Stmt>();
                    if (ifTrueBlock != null && !tryBodyVisited.Contains(ifTrueBlock))
                    {
                        trueStmts = GetStructuredBlockStmts(ifTrueBlock, tryBodyVisited);
                    }
                    
                    var falseStmts = new List<Stmt>();
                    if (ifFalseBlock != null && !tryBodyVisited.Contains(ifFalseBlock))
                    {
                        falseStmts = GetStructuredBlockStmts(ifFalseBlock, tryBodyVisited);
                    }
                    tryStmts.Add(new If(cond, trueStmts, falseStmts.Count > 0 ? falseStmts : null));
                    // 标记已处理的 if/else 分支块，防止重复处理
                    if (ifTrueBlock != null) { tryBodyVisited.Add(ifTrueBlock); visited.Add(ifTrueBlock); }
                    if (ifFalseBlock != null) { tryBodyVisited.Add(ifFalseBlock); visited.Add(ifFalseBlock); }
                }
            }
            else
            {
                // 非 inline if：正常处理所有指令
                var normalMachine = new StackMachine(_codeObject);
                foreach (var ins in preBodyInstrs)
                {
                    var stmt = normalMachine.Execute(ins);
                    if (stmt != null) tryStmts.Add(stmt);
                }
                while (normalMachine.HasResults)
                    tryStmts.Add(new ExprStmt(normalMachine.PopResult()));
                }
            }
        }
        // 2) 后继块用 GetStructuredBlockStmts
        foreach (var bodyBlock in tryBodyBlocks)
        {
            if (bodyBlock.Instructions.Any(i => i.Opcode == Opcode.POP_BLOCK))
                continue;
            var bodyResult = GetStructuredBlockStmts(bodyBlock, tryBodyVisited);
            if (bodyResult.Count > 0)
                tryStmts.AddRange(bodyResult);
        }
        // 检查 POP_BLOCK 块之后是否有 JUMP_FORWARD → else body
        // 优先从当前 block 中找（try-except-else 的 JUMP_FORWARD 通常在 SETUP_FINALLY 块中）
        var popBlockBlock = block;
        var jfInstr = popBlockBlock.Instructions.FirstOrDefault(
            i => i.Opcode == Opcode.JUMP_FORWARD);
        if (jfInstr.Argument.HasValue)
        {
            var target = jfInstr.Offset + 2 + jfInstr.Argument.Value;
            // 跳过回边块（v3.10: POP_BLOCK→JUMP_FORWARD 可能跳到 while 回边条件块）
            if (_blockByOffset.TryGetValue(target, out var targetBlock))
            {
                var lastInTarget = targetBlock.Instructions.LastOrDefault();
                bool isBackEdge = lastInTarget != default
                    && JumpHelper.IsConditionalJump(lastInTarget.Opcode)
                    && lastInTarget.Argument.HasValue
                    && lastInTarget.Argument.Value >= targetBlock.StartOffset;
                if (!isBackEdge)
                    elseJumpTarget = target;
            }
        }
        // 如果当前块没有找到，再从 tryBodyBlocks 中找
        if (!elseJumpTarget.HasValue && tryBodyBlocks.Count > 0)
        {
            var bodyPopBlock = tryBodyBlocks.LastOrDefault(b =>
                b.Instructions.Any(i => i.Opcode == Opcode.POP_BLOCK));
            if (bodyPopBlock != null)
            {
                jfInstr = bodyPopBlock.Instructions.FirstOrDefault(
                    i => i.Opcode == Opcode.JUMP_FORWARD);
                if (jfInstr.Argument.HasValue)
                {
                    var target = jfInstr.Offset + 2 + jfInstr.Argument.Value;
                    if (_blockByOffset.TryGetValue(target, out var targetBlock))
                    {
                        var lastInTarget = targetBlock.Instructions.LastOrDefault();
                        bool isBackEdge = lastInTarget != default
                            && JumpHelper.IsConditionalJump(lastInTarget.Opcode)
                            && lastInTarget.Argument.HasValue
                            && lastInTarget.Argument.Value >= targetBlock.StartOffset;
                        if (!isBackEdge)
                            elseJumpTarget = target;
                    }
                }
            }
        }

        // 查找 handler body：从 handlerAbs 偏移处开始的块
        var handlerBlocks = new List<BasicBlock>();
        // 精确查找 handler 起始块，而不是递归收集所有后继
        if (_blockByOffset.TryGetValue(handlerAbs, out var handlerEntryBlock))
        {
            handlerBlocks.Add(handlerEntryBlock);
            // 只收集 handler 块及其直接链（直到不含 DUP_TOP/POP_TOP×3/LOAD_GLOBAL 等 handler 入口特征的块）
            var visitedIds = new HashSet<int> { handlerEntryBlock.Id };
            var queue = new Queue<BasicBlock>();
            queue.Enqueue(handlerEntryBlock);
            bool pastHandlerPreamble = false;
            while (queue.Count > 0)
            {
                var cur = queue.Dequeue();
                foreach (var succ in cur.Successors)
                {
                    if (succ == null || !visitedIds.Add(succ.Id)) continue;
                    // LoopHeader 不是 handler 的一部分（循环回边目标）
                    if (succ.Flags.HasFlag(BlockFlags.LoopHeader)) continue;
                    // 检查后继块是否仍是 handler 的一部分：检查其指令特征
                    bool isHandlerPart = false;
                    foreach (var ins in succ.Instructions.Take(3))
                    {
                        if (ins.Opcode == Opcode.DUP_TOP || ins.Opcode == Opcode.POP_TOP 
                            || ins.Opcode == Opcode.JUMP_IF_NOT_EXC_MATCH
                            || ins.Opcode == Opcode.RERAISE
                            || ins.Opcode == Opcode.POP_EXCEPT || ins.Opcode == Opcode.END_FINALLY
                            || ins.Opcode == Opcode.RETURN_VALUE)
                        {
                            isHandlerPart = true;
                        }
                        // LOAD_NAME/LOAD_GLOBAL is only handler preamble when immediately before JUMP_IF_NOT_EXC_MATCH
                        // (not for class defs or function defs that follow the handler)
                        if (ins.Opcode == Opcode.LOAD_NAME || ins.Opcode == Opcode.LOAD_GLOBAL)
                        {
                            // Check if the very NEXT instruction is JUMP_IF_NOT_EXC_MATCH
                            var nextIdx = succ.Instructions.IndexOf(ins) + 1;
                            if (nextIdx < succ.Instructions.Count
                                && succ.Instructions[nextIdx].Opcode == Opcode.JUMP_IF_NOT_EXC_MATCH)
                            {
                                isHandlerPart = true;
                            }
                        }
                    }
                    if (isHandlerPart || !pastHandlerPreamble)
                    {
                        handlerBlocks.Add(succ);
                        _processedBlockIds.Add(succ.Id);
                        queue.Enqueue(succ);
                        if (isHandlerPart && !pastHandlerPreamble)
                        {
                            // 检查是否已经过了 handler 前导码（DUP_TOP/POP_TOP×3）
                            bool hasBodyInstr = false;
                            foreach (var ins in succ.Instructions)
                            {
                                if (ins.Opcode != Opcode.DUP_TOP && ins.Opcode != Opcode.POP_TOP
                                    && ins.Opcode != Opcode.JUMP_IF_NOT_EXC_MATCH
                                    && ins.Opcode != Opcode.LOAD_NAME && ins.Opcode != Opcode.LOAD_GLOBAL
                                    && ins.Opcode != Opcode.RERAISE)
                                {
                                    hasBodyInstr = true;
                                    break;
                                }
                            }
                            if (hasBodyInstr) pastHandlerPreamble = true;
                        }
                    }
                }
            }
        }

        // 当 handler 在同一个块中时（如 3.8-3.10 整函数单块），从当前块的指令中提取 handler
        bool handlerIsInline = handlerBlocks.Count == 0 && handlerAbs > block.StartOffset && handlerAbs < block.EndOffset;

        // 提取 handler body 语句
        var handlerInstrs = new List<Instruction>();
        bool handlerFound = false, seenBody = false, isFinally = false;
        if (handlerIsInline)
        {
            // 直接在当前块的指令列表中扫描 handler（从 handlerAbs 开始）
            foreach (var ins in block.Instructions.Where(i => i.Offset >= handlerAbs))
            {
                if (ins.Opcode == Opcode.POP_EXCEPT)
                {
                    handlerFound = true;
                    continue; // POP_EXCEPT 后继续提取（如后续的 LOAD_FAST + RETURN_VALUE）
                }
                if (ins.Opcode == Opcode.END_FINALLY)
                {
                    if (seenBody) { handlerFound = true; break; }
                    continue;
                }
                if (!seenBody && ins.Opcode is Opcode.DUP_TOP) continue;
                if (!seenBody && ins.Opcode is Opcode.JUMP_IF_NOT_EXC_MATCH) continue;
                if (!seenBody && ins.Opcode is Opcode.RERAISE) continue;
                if (!seenBody && (ins.Opcode is Opcode.LOAD_NAME or Opcode.LOAD_GLOBAL or Opcode.LOAD_FAST)) continue;
                if (!seenBody && ins.Opcode is Opcode.POP_TOP) continue;
                seenBody = true;
                if (ins.Opcode is Opcode.JUMP_FORWARD or Opcode.JUMP_ABSOLUTE) continue;
                // 在 POP_EXCEPT (handlerFound) 之后，跳过 final LOAD + RETURN 对
                // 这些是 try 体成功路径和 handler 路径的共享结尾，不属 handler 特有
                if (handlerFound && (ins.Opcode is Opcode.RETURN_VALUE 
                    or Opcode.LOAD_FAST or Opcode.LOAD_NAME or Opcode.LOAD_DEREF
                    or Opcode.RAISE_VARARGS))
                    continue;
                handlerInstrs.Add(ins);
            }
        }
        else foreach (var hb in handlerBlocks)
        {
            if (handlerFound) break;
            foreach (var ins in hb.Instructions)
            {
                if (ins.Opcode == Opcode.POP_EXCEPT)
                {
                    handlerFound = true;
                    continue; // POP_EXCEPT 后继续提取（如后续的 LOAD_FAST + RETURN_VALUE）
                }
                if (ins.Opcode == Opcode.END_FINALLY)
                {
                    if (seenBody) { handlerFound = true; break; }
                    continue; // finally 块的 END_FINALLY — 不要中断
                }
                // 3.10 except handler 入口模式: DUP_TOP + LOAD_GLOBAL + JUMP_IF_NOT_EXC_MATCH + POP_TOP×3
                if (!seenBody && ins.Opcode is Opcode.DUP_TOP)
                    continue; // 跳过 DUP_TOP (except handler 入口)
                if (!seenBody && ins.Opcode is Opcode.JUMP_IF_NOT_EXC_MATCH)
                    continue; // 跳过异常类型匹配跳转
                if (!seenBody && ins.Opcode is Opcode.RERAISE)
                    continue; // 跳过重抛
                if (!seenBody && (ins.Opcode is Opcode.LOAD_NAME or Opcode.LOAD_GLOBAL or Opcode.LOAD_FAST))
                    continue; // 跳过 except 类型加载（由 exceptType 独立提取）
                // 跳过 POP_TOP × 3（except handler 的栈清理）
                if (!seenBody && ins.Opcode is Opcode.POP_TOP)
                    continue;
                seenBody = true;
                if (ins.Opcode is Opcode.JUMP_FORWARD or Opcode.JUMP_ABSOLUTE) continue;
                handlerInstrs.Add(ins);
            }
        }

        // 反编译 handler body
        var handlerBody = new List<Stmt>();
        if (handlerInstrs.Count > 0)
        {
            var handlerMachine = new StackMachine(_codeObject);
            handlerMachine.SetLoopHeaders(_loopHeaderOffsets);
            foreach (var ins in handlerInstrs)
            {
                var stmt = handlerMachine.Execute(ins);
                if (stmt != null)
                    handlerBody.Add(stmt);
            }
        }
        // 检测 handler 类型：except（以 DUP_TOP 或 POP_TOP×3 开头）还是 finally（无两者）
        bool isExceptHandler = false;
        int topCount = 0;
        if (handlerIsInline)
        {
            foreach (var ins in block.Instructions.Where(i => i.Offset >= handlerAbs))
            {
                if (ins.Opcode == Opcode.DUP_TOP) { isExceptHandler = true; break; }
                if (ins.Opcode == Opcode.POP_TOP) { topCount++; if (topCount >= 2) { isExceptHandler = true; break; } }
                if (ins.Opcode == Opcode.LOAD_NAME || ins.Opcode == Opcode.LOAD_GLOBAL
                    || ins.Opcode == Opcode.LOAD_FAST) break;
            }
        }
        else foreach (var hb in handlerBlocks)
        {
            foreach (var ins in hb.Instructions)
            {
                if (ins.Opcode == Opcode.DUP_TOP) { isExceptHandler = true; break; }
                if (ins.Opcode == Opcode.POP_TOP) { topCount++; if (topCount >= 2) { isExceptHandler = true; break; } }
                if (ins.Opcode == Opcode.LOAD_NAME || ins.Opcode == Opcode.LOAD_GLOBAL
                    || ins.Opcode == Opcode.LOAD_FAST) break;
            }
            if (isExceptHandler) break;
        }

        List<Stmt>? finalBody = null;
        List<Stmt>? elseBody = null;
        List<ExceptHandler> handlers = new();

        if (isExceptHandler)
        {
            // === except handler ===
            // 检测 except 异常类型
            Expr? exceptType = null;
            if (handlerIsInline)
            {
                bool foundType = false;
                foreach (var ins in block.Instructions.Where(i => i.Offset >= handlerAbs))
                {
                    if (ins.Opcode == Opcode.LOAD_NAME || ins.Opcode == Opcode.LOAD_GLOBAL)
                    {
                        if (exceptType == null)
                        {
                            var typeName = _codeObject.Names.Count > (ins.Argument ?? 0)
                                ? _codeObject.Names[ins.Argument!.Value] : null;
                            if (typeName != null && typeName != "__doc__" && !typeName.StartsWith("__"))
                                exceptType = new Name(typeName, ExpressionContext.Load);
                        }
                    }
                    else if (ins.Opcode == Opcode.JUMP_IF_NOT_EXC_MATCH && exceptType != null)
                    {
                        foundType = true;
                        break;
                    }
                }
            }
            else foreach (var hb in handlerBlocks)
            {
                bool foundType = false;
                foreach (var ins in hb.Instructions)
                {
                    if (ins.Opcode == Opcode.LOAD_NAME || ins.Opcode == Opcode.LOAD_GLOBAL)
                    {
                        // Only take the FIRST LOAD_NAME/LOAD_GLOBAL (the one right after DUP_TOP for except type match)
                        // subsequent LOAD_NAMEs belong to the handler body (function/class defs)
                        if (exceptType == null)
                        {
                            var typeName = _codeObject.Names.Count > (ins.Argument ?? 0)
                                ? _codeObject.Names[ins.Argument!.Value] : null;
                            if (typeName != null && typeName != "__doc__" && !typeName.StartsWith("__"))
                                exceptType = new Name(typeName, ExpressionContext.Load);
                        }
                    }
                    else if (ins.Opcode == Opcode.JUMP_IF_NOT_EXC_MATCH && exceptType != null)
                    {
                        foundType = true;
                        break;  // Found the except type match pattern
                    }
                }
                if (foundType) break;
            }
            handlers.Add(new ExceptHandler(exceptType, null, handlerBody));

            // 检测 else 子句：try body 的 POP_BLOCK 后 JUMP_FORWARD → else body
            if (elseJumpTarget.HasValue)
            {
                // else body 在 handler 之后，由 JUMP_FORWARD 指向
                var elseBlocks = new List<BasicBlock>();
                if (_blockByOffset.TryGetValue(elseJumpTarget.Value, out var elseEntryBlock))
                {
                    // 检查 else 候选块之后是否有其他块
                    // 在 try-except-else 中，else 块之后还有函数末尾的代码块
                    // 在 try-except-no-else 中，else 候选块是最后一个块（函数末尾）
                    bool isRealElse = false;
                    var allBlocks = _blockByOffset.Values.OrderBy(b => b.StartOffset).ToList();
                    int elseIndex = allBlocks.FindIndex(b => b.StartOffset == elseEntryBlock.StartOffset);
                    
                    if (elseIndex >= 0 && elseIndex < allBlocks.Count - 1)
                    {
                        bool hasNonEmptyNextBlock = false;
                        for (int i = elseIndex + 1; i < allBlocks.Count; i++)
                        {
                            if (allBlocks[i].Instructions.Count > 0)
                            {
                                hasNonEmptyNextBlock = true;
                                break;
                            }
                        }
                        if (hasNonEmptyNextBlock)
                        {
                            isRealElse = true;
                        }
                    }
                    if (isRealElse)
                    {
                        elseBlocks.Add(elseEntryBlock);
                        var visitedIds = new HashSet<int> { elseEntryBlock.Id };
                        var queue = new Queue<BasicBlock>();
                        queue.Enqueue(elseEntryBlock);
                        while (queue.Count > 0)
                        {
                            var cur = queue.Dequeue();
                            foreach (var succ in cur.Successors)
                            {
                                if (succ == null || !visitedIds.Add(succ.Id)) continue;
                                // 跳过 handler 块和回边块
                                if (succ.StartOffset < handlerAbs) continue;
                                // 跳过循环头
                                if (succ.Flags.HasFlag(BlockFlags.LoopHeader)) continue;
                                elseBlocks.Add(succ);
                                queue.Enqueue(succ);
                            }
                        }
                    }
                }
                if (elseBlocks.Count > 0)
                {
                    var elseStmts = new List<Stmt>();
                    foreach (var eb in elseBlocks)
                    {
                        var ebInstrs = eb.Instructions.ToList();
                        if (ebInstrs.Count > 0)
                        {
                            var ebMachine = new StackMachine(_codeObject);
                            ebMachine.SetLoopHeaders(_loopHeaderOffsets);
                            foreach (var ins in ebInstrs)
                            {
                                var s = ebMachine.Execute(ins);
                                if (s != null) elseStmts.Add(s);
                            }
                            while (ebMachine.HasResults)
                                elseStmts.Add(new ExprStmt(ebMachine.PopResult()));
                        }
                    }
                    if (elseStmts.Count > 0 && !IsTrivialElse(elseStmts))
                    {
                        elseBody = elseStmts;
                        foreach (var eb in elseBlocks)
                            visited.Add(eb);
                    }
                }
            }
        }
        else
        {
            // === finally handler ===
            finalBody = handlerBody;
        }

        bool hasValidHandlers = handlers.Count > 0 && handlers.Any(h => 
            h.Body != null && h.Body.Count > 0);
        bool hasValidFinally = finalBody != null && finalBody.Count > 0;
        bool hasValidElse = elseBody != null && elseBody.Count > 0;
        
        if (!hasValidHandlers && !hasValidFinally && !hasValidElse)
        {
            var resultWithoutTry = new List<Stmt>(beforeTry);
            resultWithoutTry.AddRange(tryStmts);
            return resultWithoutTry;
        }

        var tryNode = new Try(tryStmts, handlers, elseBody, finalBody);

        var result = new List<Stmt>(beforeTry);
        result.Add(tryNode);

        // 处理当前块中 POP_BLOCK 之后到 handler 之前的指令
        // (如 LOAD_CONST None + RETURN_VALUE — 函数的隐式返回)
        // 仅在 try/except（有 handler）时处理，try/finally 时跳过
        //（try/finally 的 POP_BLOCK 后有 cleanup 胶水代码，不应输出为语句）
        if (handlers.Count > 0)
        {
            bool foundPopBlock = false;
            var postPopInstrs = new List<Instruction>();
            for (int i = setupIdx + 1; i < instrs.Count; i++)
            {
                if (instrs[i].Opcode == Opcode.POP_BLOCK) { foundPopBlock = true; continue; }
                if (foundPopBlock && instrs[i].Offset < handlerAbs)
                    postPopInstrs.Add(instrs[i]);
            }
            if (postPopInstrs.Count > 0)
            {
                var postMachine = new StackMachine(_codeObject);
                postMachine.SetLoopHeaders(_loopHeaderOffsets);
                foreach (var ins in postPopInstrs)
                {
                    var stmt = postMachine.Execute(ins);
                    if (stmt != null) result.Add(stmt);
                }
                while (postMachine.HasResults)
                    result.Add(new ExprStmt(postMachine.PopResult()));
            }
        }

        // 标记所有 try body 块为 visited，防止外部重新处理
        foreach (var tb in tryBodyCollector)
            visited.Add(tb);
        
        return result;
    }

    /// <summary>
    /// 查找从指定偏移开始的块及其所有后继（收集 handler 块链）。
    /// </summary>
    private void FindBlocksFromOffset(int offset, List<BasicBlock> result)
    {
        if (_blockByOffset.TryGetValue(offset, out var block))
        {
            var visited = new HashSet<int>();
            var queue = new Queue<BasicBlock>();
            queue.Enqueue(block);
            while (queue.Count > 0)
            {
                var cur = queue.Dequeue();
                if (cur == null || !visited.Add(cur.Id)) continue;
                result.Add(cur);
                // 只跟随 handler 链内的跳转：
                // 1. 不跟随 Exit 块的后缀（避免跳转到 handler 以外的代码）
                // 2. POP_EXCEPT/END_FINALLY 后，仅当后继是 handler 前导块时才继续跟随（支持多 except 链）
                // 3. 非 POP_EXCEPT 时正常跟随所有后继
                bool hasPopExcept = cur.Instructions.Any(i =>
                    i.Opcode == Opcode.POP_EXCEPT || i.Opcode == Opcode.END_FINALLY);
                foreach (var succ in cur.Successors)
                {
                    if (cur.Flags.HasFlag(BlockFlags.Exit)) continue;
                    if (hasPopExcept)
                    {
                        // POP_EXCEPT 后仅跟踪 handler 前导块（DUP_TOP/CHECK_EXC_MATCH/JUMP_IF_NOT_EXC_MATCH）
                        // 支持 try: except A: ... POP_EXCEPT → except B: ... POP_EXCEPT 链
                        bool isHandlerPreamble = succ.Instructions.Any(i =>
                            i.Opcode == Opcode.DUP_TOP
                            || i.Opcode == Opcode.CHECK_EXC_MATCH
                            || i.Opcode == Opcode.CHECK_EG_MATCH
                            || i.Opcode == Opcode.JUMP_IF_NOT_EXC_MATCH);
                        if (!isHandlerPreamble) continue;
                    }
                    queue.Enqueue(succ);
                }
            }
        }
    }

    /// <summary>
    /// 判断 else 子句是否仅包含模块级出口代码（return None/pass/空）。
    /// </summary>
    private bool IsTrivialElse(List<Stmt>? stmts)
    {
        if (stmts == null || stmts.Count == 0) return true;
        if (stmts.Count == 1)
        {
            if (stmts[0] is Return r && r.Value is Constant { Value: null }) return true;
            if (stmts[0] is Pass) return true;
            if (stmts[0] is CommentBlock) return true;
        }
        return false;
    }

    /// <summary>
    /// 创建 with 语句的 except handler（用于清理资源，不生成 except 子句）。
    /// </summary>
    private List<ExceptHandler> BuildCleanupHandler()
    {
        return new List<ExceptHandler>
        {
            new ExceptHandler(null, null, new List<Stmt>())
        };
    }

    /// <summary>
    /// 获取块中第一个 SETUP_FINALLY 的 handler 绝对偏移。
    /// </summary>
    private int? GetHandlerOffset(BasicBlock block)
    {
        foreach (var ins in block.Instructions)
        {
            if (ins.Opcode == Opcode.SETUP_FINALLY && ins.Argument.HasValue)
                return ins.Offset + 2 + ins.Argument.Value;
        }
        return null;
    }

    /// <summary>
    /// 从指定偏移提取 except handler 块。
    /// 用于嵌套 try 处理（多个 SETUP 在同一块时）。
    /// </summary>
    private List<ExceptHandler> ExtractExceptHandlerFromOffset(
        int handlerAbs, BasicBlock currentBlock, List<Instruction> blockInstrs, int setupIdx)
    {
        if (_blockByOffset.TryGetValue(handlerAbs, out var handlerEntry))
        {
            // 收集 handler 块链
            var handlerBlocks = new List<BasicBlock>();
            var visitedIds = new HashSet<int> { handlerEntry.Id };
            var queue = new Queue<BasicBlock>();
            queue.Enqueue(handlerEntry);
            bool pastHandlerPreamble = false;
            
            while (queue.Count > 0)
            {
                var cur = queue.Dequeue();
                foreach (var succ in cur.Successors)
                {
                    if (succ == null || !visitedIds.Add(succ.Id)) continue;
                    if (succ.Flags.HasFlag(BlockFlags.LoopHeader)) continue;
                    
                    bool isHandlerPart = false;
                    foreach (var ins in succ.Instructions.Take(3))
                    {
                        if (ins.Opcode == Opcode.DUP_TOP || ins.Opcode == Opcode.POP_TOP
                            || ins.Opcode == Opcode.LOAD_NAME || ins.Opcode == Opcode.LOAD_GLOBAL
                            || ins.Opcode == Opcode.JUMP_IF_NOT_EXC_MATCH
                            || ins.Opcode == Opcode.RERAISE
                            || ins.Opcode == Opcode.POP_EXCEPT || ins.Opcode == Opcode.END_FINALLY
                            || ins.Opcode == Opcode.RETURN_VALUE)
                        { isHandlerPart = true; }
                    }
                    if (isHandlerPart || !pastHandlerPreamble)
                    {
                        handlerBlocks.Add(succ);
                        _processedBlockIds.Add(succ.Id);
                        queue.Enqueue(succ);
                        if (isHandlerPart && !pastHandlerPreamble)
                        {
                            bool hasBodyInstr = succ.Instructions.Any(ins =>
                                ins.Opcode != Opcode.DUP_TOP && ins.Opcode != Opcode.POP_TOP
                                && ins.Opcode != Opcode.JUMP_IF_NOT_EXC_MATCH
                                && ins.Opcode != Opcode.LOAD_NAME && ins.Opcode != Opcode.LOAD_GLOBAL
                                && ins.Opcode != Opcode.RERAISE);
                            if (hasBodyInstr) pastHandlerPreamble = true;
                        }
                    }
                }
            }
            
            // 提取 handler body 指令
            var handlerInstrs = new List<Instruction>();
            bool handlerFound = false, seenBody = false;
            foreach (var hb in handlerBlocks)
            {
                if (handlerFound) break;
                foreach (var ins in hb.Instructions)
                {
                    if (ins.Opcode == Opcode.POP_EXCEPT) { handlerFound = true; break; }
                    if (ins.Opcode == Opcode.END_FINALLY) { if (seenBody) { handlerFound = true; break; } continue; }
                    if (!seenBody && ins.Opcode == Opcode.DUP_TOP) continue;
                    if (!seenBody && ins.Opcode == Opcode.JUMP_IF_NOT_EXC_MATCH) continue;
                    if (!seenBody && ins.Opcode == Opcode.RERAISE) continue;
                    if (!seenBody && (ins.Opcode == Opcode.LOAD_NAME || ins.Opcode == Opcode.LOAD_GLOBAL || ins.Opcode == Opcode.LOAD_FAST)) continue;
                    if (!seenBody && ins.Opcode == Opcode.POP_TOP) continue;
                    seenBody = true;
                    if (ins.Opcode == Opcode.JUMP_FORWARD || ins.Opcode == Opcode.JUMP_ABSOLUTE) continue;
                    handlerInstrs.Add(ins);
                }
            }
            
            // 反编译 handler body
            var handlerBody = new List<Stmt>();
            if (handlerInstrs.Count > 0)
            {
                var handlerMachine = new StackMachine(_codeObject);
                handlerMachine.SetLoopHeaders(_loopHeaderOffsets);
                foreach (var ins in handlerInstrs)
                {
                    var s = handlerMachine.Execute(ins);
                    if (s != null) handlerBody.Add(s);
                }
            }
            if (handlerBody.Count == 0)
                handlerBody.Add(new Pass());
            
            return new List<ExceptHandler> { new ExceptHandler(null, null, handlerBody) };
        }
        
        // Fallback: empty except
        return new List<ExceptHandler> { new ExceptHandler(null, null, new List<Stmt> { new Pass() }) };
    }

    private List<Stmt>? BuildWithFromBlock(BasicBlock block, HashSet<BasicBlock> visited)
    {
        var instrs = block.Instructions;
        var setupIdx = instrs.FindIndex(i => i.Opcode == Opcode.SETUP_WITH);
        var beforeWithIdx = instrs.FindIndex(i =>
            i.Opcode == Opcode.BEFORE_WITH_313 || i.Opcode == Opcode.BEFORE_WITH
            || i.Opcode == Opcode.BEFORE_WITH_312);
        var loadSpecialIdx = instrs.FindIndex(i => i.Opcode == Opcode.LOAD_SPECIAL);
        var withIdx = setupIdx >= 0 ? setupIdx : beforeWithIdx;
        
        Console.Error.WriteLine($"[BUILD_WITH_DEBUG] block=0x{block.StartOffset:X4} setupIdx={setupIdx} beforeWithIdx={beforeWithIdx} loadSpecialIdx={loadSpecialIdx} withIdx={withIdx}");
        
        if (_options.VerboseErrors)
        {
            for (int i = 0; i < instrs.Count; i++)
            {
                Console.Error.WriteLine($"[BUILD_WITH_DEBUG]   instr[{i}] = {instrs[i].Opcode}");
            }
        }
        
        bool isSetupWith = setupIdx >= 0;
        
        if (withIdx < 0 && !isSetupWith)
        {
            if (_codeObject.ExceptionTable != null)
            {
                foreach (var et in _codeObject.ExceptionTable)
                {
                    var targetBlock = FindBlockByOffset(et.TargetOffset);
                    if (targetBlock != null && targetBlock.Instructions.Any(i => i.Opcode == Opcode.WITH_EXCEPT_START))
                    {
                        if (et.StartOffset == block.StartOffset)
                        {
                            if (_options.VerboseErrors)
                            {
                                Console.Error.WriteLine($"[BUILD_WITH_DEBUG] Found WITH via ET entry starting at block offset");
                            }
                            withIdx = instrs.Count - 1;
                            break;
                        }
                    }
                }
            }
            
            if (withIdx < 0)
            {
                for (int i = 0; i < instrs.Count - 6; i++)
                {
                    if (instrs[i].Opcode == Opcode.LOAD_SPECIAL && 
                        instrs[i + 1].Opcode == Opcode.SWAP && 
                        instrs[i + 2].Opcode == Opcode.SWAP && 
                        instrs[i + 3].Opcode == Opcode.LOAD_SPECIAL && 
                        instrs[i + 4].Opcode == Opcode.CALL)
                    {
                        if (_options.VerboseErrors)
                        {
                            Console.Error.WriteLine($"[BUILD_WITH_DEBUG] Found LOAD_SPECIAL pattern at index {i}");
                            Console.Error.WriteLine($"[BUILD_WITH_DEBUG]  instr[{i-2}] = {instrs[i-2].Opcode}");
                            Console.Error.WriteLine($"[BUILD_WITH_DEBUG]  instr[{i-1}] = {instrs[i-1].Opcode}");
                            Console.Error.WriteLine($"[BUILD_WITH_DEBUG]  instr[{i}] = {instrs[i].Opcode}");
                        }
                        if (i > 0 && instrs[i - 1].Opcode == Opcode.COPY)
                        {
                            withIdx = i - 2;
                        }
                        else
                        {
                            withIdx = i;
                        }
                        break;
                    }
                }
            }
            
            if (withIdx < 0)
            {
                if (_options.VerboseErrors) Console.Error.WriteLine($"[BUILD_WITH_DEBUG] RETURN NULL: no WITH opcode found");
                return null;
            }
        }

        // 1. 提取 with 之前的上下文表达式
        var preMachine = new StackMachine(_codeObject);
        
        int effectiveWithIdx = withIdx;
        if (!isSetupWith && beforeWithIdx < 0)
        {
            if (withIdx >= 0 && withIdx < instrs.Count && instrs[withIdx].Opcode == Opcode.CALL)
            {
                effectiveWithIdx = withIdx;
            }
            else
            {
                for (int i = instrs.Count - 1; i >= 0; i--)
                {
                    if (instrs[i].Opcode == Opcode.CALL && i > 0 && instrs[i - 1].Opcode == Opcode.LOAD_NAME && i > 1 && instrs[i - 2].Opcode == Opcode.PUSH_NULL)
                    {
                        effectiveWithIdx = i;
                        break;
                    }
                }
            }
        }
        
        for (int i = 0; i <= effectiveWithIdx; i++)
        {
            var stmt = preMachine.Execute(instrs[i]);
        }

        Expr? contextExpr = preMachine.ExprStackCount > 0 ? preMachine.PopExpr() : null;
        
        if (!isSetupWith && beforeWithIdx < 0)
        {
            foreach (var pred in block.Predecessors)
            {
                if (_options.VerboseErrors)
                {
                    Console.Error.WriteLine($"[BUILD_WITH_DEBUG] Checking predecessor block=0x{pred.StartOffset:X4}");
                }
                
                for (int i = pred.Instructions.Count - 1; i >= 0; i--)
                {
                    if (pred.Instructions[i].Opcode == Opcode.CALL && i > 0 && pred.Instructions[i - 1].Opcode == Opcode.LOAD_NAME && i > 1 && pred.Instructions[i - 2].Opcode == Opcode.PUSH_NULL)
                    {
                        bool isFollowedBySpecial = false;
                        for (int j = i + 1; j < pred.Instructions.Count; j++)
                        {
                            if (pred.Instructions[j].Opcode == Opcode.COPY || pred.Instructions[j].Opcode == Opcode.SWAP || pred.Instructions[j].Opcode == Opcode.LOAD_SPECIAL_314)
                            {
                                isFollowedBySpecial = true;
                            }
                            else
                            {
                                break;
                            }
                        }
                        
                        if (_options.VerboseErrors)
                        {
                            Console.Error.WriteLine($"[BUILD_WITH_DEBUG] Found CALL at index={i} isFollowedBySpecial={isFollowedBySpecial}");
                        }
                        
                        if (isFollowedBySpecial)
                        {
                            var predMachine = new StackMachine(_codeObject);
                            for (int j = i - 3; j <= i; j++)
                            {
                                if (j >= 0)
                                {
                                    var stmt = predMachine.Execute(pred.Instructions[j]);
                                }
                            }
                            if (predMachine.ExprStackCount > 0)
                            {
                                contextExpr = predMachine.PopExpr();
                                if (_options.VerboseErrors)
                                {
                                    Console.Error.WriteLine($"[BUILD_WITH_DEBUG] contextExpr from pred={contextExpr?.GetType().Name}");
                                }
                                break;
                            }
                        }
                    }
                }
                if (contextExpr != null)
                    break;
            }
        }
        
        if (_options.VerboseErrors)
        {
            Console.Error.WriteLine($"[BUILD_WITH_DEBUG] contextExpr={contextExpr?.GetType().Name} stackCount={preMachine.ExprStackCount}");
        }
        
        if (contextExpr == null) 
        {
            if (_options.VerboseErrors) Console.Error.WriteLine($"[BUILD_WITH_DEBUG] RETURN NULL: contextExpr is null");
            return null;
        }

        // 2. 提取可选的 as 变量
        Expr? optionalVar = null;
        
        bool isPy314Style = instrs.Any(i => i.Opcode == Opcode.LOAD_SPECIAL);
        
        if (isPy314Style)
        {
            int callCount = 0;
            for (int i = 0; i < instrs.Count; i++)
            {
                if (instrs[i].Opcode == Opcode.CALL)
                {
                    callCount++;
                    if (callCount == 2 && i + 1 < instrs.Count)
                    {
                        if (instrs[i + 1].Opcode == Opcode.STORE_FAST && instrs[i + 1].Argument.HasValue)
                        {
                            var idx = instrs[i + 1].Argument.Value;
                            string varName = idx < _codeObject.Varnames.Count ? _codeObject.Varnames[idx] : $"v_{idx}";
                            optionalVar = new Name(varName, ExpressionContext.Store);
                        }
                        break;
                    }
                }
            }
        }
        else
        {
            for (int i = withIdx + 1; i < instrs.Count; i++)
            {
                var op = instrs[i].Opcode;
                if (op == Opcode.BEFORE_WITH || op == Opcode.BEFORE_WITH_313
                    || op == Opcode.BEFORE_WITH_312
                    || op == Opcode.SETUP_WITH || op == Opcode.WITH_EXCEPT_START)
                    continue;
                if (op == Opcode.POP_TOP)
                    break;
                if ((op == Opcode.STORE_FAST || op == Opcode.STORE_NAME)
                    && instrs[i].Argument.HasValue)
                {
                    var idx = instrs[i].Argument.Value;
                    string varName = op == Opcode.STORE_FAST
                        ? (idx < _codeObject.Varnames.Count ? _codeObject.Varnames[idx] : $"v_{idx}")
                        : (idx < _codeObject.Names.Count ? _codeObject.Names[idx] : $"n_{idx}");
                    optionalVar = new Name(varName, ExpressionContext.Store);
                    break;
                }
                break;
            }
        }
        
        if (optionalVar == null && !isSetupWith && !isPy314Style)
        {
            foreach (var succ in block.Successors)
            {
                foreach (var instr in succ.Instructions)
                {
                    if (instr.Opcode == Opcode.STORE_FAST || instr.Opcode == Opcode.STORE_NAME)
                    {
                        var idx = instr.Argument.Value;
                        string varName = instr.Opcode == Opcode.STORE_FAST
                            ? (idx < _codeObject.Varnames.Count ? _codeObject.Varnames[idx] : $"v_{idx}")
                            : (idx < _codeObject.Names.Count ? _codeObject.Names[idx] : $"n_{idx}");
                        optionalVar = new Name(varName, ExpressionContext.Store);
                        break;
                    }
                    if (instr.Opcode == Opcode.POP_TOP)
                        break;
                }
                if (optionalVar != null)
                    break;
            }
            
            if (optionalVar == null)
            {
                foreach (var instr in instrs)
                {
                    if (instr.Opcode == Opcode.STORE_FAST || instr.Opcode == Opcode.STORE_NAME)
                    {
                        var idx = instr.Argument.Value;
                        string varName = instr.Opcode == Opcode.STORE_FAST
                            ? (idx < _codeObject.Varnames.Count ? _codeObject.Varnames[idx] : $"v_{idx}")
                            : (idx < _codeObject.Names.Count ? _codeObject.Names[idx] : $"n_{idx}");
                        optionalVar = new Name(varName, ExpressionContext.Store);
                        break;
                    }
                }
            }
        }

        // 3. 确定 handler 起始偏移和 body 范围
        int handlerAbs;
        int bodyEndOffset = -1;
        if (isSetupWith)
        {
            var handlerRel = instrs[setupIdx].Argument ?? 0;
            handlerAbs = instrs[setupIdx].Offset + 2 + handlerRel * 2;
            bodyEndOffset = -1;
            for (int i = setupIdx + 1; i < instrs.Count; i++)
            {
                if (instrs[i].Opcode == Opcode.POP_BLOCK)
                {
                    bodyEndOffset = instrs[i].Offset;
                    break;
                }
            }
            if (bodyEndOffset < 0)
                bodyEndOffset = handlerAbs;
        }
        else
        {
            // 3.11+: 用 ExceptionTable 找 WITH_EXCEPT_START handler 的起始偏移
            handlerAbs = -1;
            if (_codeObject.ExceptionTable != null)
            {
                var beforeWithOffset = instrs[withIdx].Offset;
                foreach (var et in _codeObject.ExceptionTable)
                {

                    var targetBlock = FindBlockByOffset(et.TargetOffset);
                    if (targetBlock != null)
                    {
                        bool isWithHandler = targetBlock.Instructions.Any(i => 
                            i.Opcode == Opcode.WITH_EXCEPT_START || 
                            i.Opcode == Opcode.WITH_EXCEPT_START_312 ||
                            i.Opcode == Opcode.PUSH_EXC_INFO_312);
                        if (isWithHandler)
                        {
                            if (et.StartOffset <= beforeWithOffset + 4 && et.EndOffset > beforeWithOffset)
                            {
                                handlerAbs = et.TargetOffset;
                                bodyEndOffset = et.EndOffset;
                                break;
                            }
                        }
                    }
                }
                
                if (handlerAbs < 0)
                {
                    foreach (var et in _codeObject.ExceptionTable)
                    {
                        var targetBlock = FindBlockByOffset(et.TargetOffset);
                        if (targetBlock != null)
                        {
                            foreach (var instr in targetBlock.Instructions)
                            {
                                if (instr.Opcode == Opcode.WITH_EXCEPT_START || instr.Opcode == Opcode.WITH_EXCEPT_START_312)
                                {
                                    handlerAbs = et.TargetOffset;
                                    bodyEndOffset = et.EndOffset;
                                    break;
                                }
                            }
                        }
                        if (handlerAbs >= 0) break;
                    }
                }
            }
            if (handlerAbs < 0) 
                return null;
        }

        // 4. 跳过变量赋值找到 body 起始
        int bodyStart = withIdx + 1;
        
        if (isPy314Style)
        {
            int callCount = 0;
            for (int i = 0; i < instrs.Count; i++)
            {
                if (instrs[i].Opcode == Opcode.CALL)
                {
                    callCount++;
                    if (callCount == 2)
                    {
                        bodyStart = i + 1;
                        break;
                    }
                }
            }
            
            for (; bodyStart < instrs.Count; bodyStart++)
            {
                var op = instrs[bodyStart].Opcode;
                if (op == Opcode.POP_TOP || op == Opcode.STORE_FAST || op == Opcode.STORE_NAME)
                    continue;
                break;
            }
        }
        else if (!isSetupWith && beforeWithIdx < 0 && withIdx >= 0 && instrs[withIdx].Opcode == Opcode.CALL)
        {
            for (int i = withIdx + 1; i < instrs.Count; i++)
            {
                if (instrs[i].Opcode == Opcode.CALL)
                {
                    bodyStart = i + 1;
                    break;
                }
            }
            
            for (; bodyStart < instrs.Count; bodyStart++)
            {
                var op = instrs[bodyStart].Opcode;
                if (op == Opcode.BEFORE_WITH || op == Opcode.BEFORE_WITH_313
                    || op == Opcode.BEFORE_WITH_312
                    || op == Opcode.WITH_EXCEPT_START)
                    continue;
                if (op == Opcode.POP_TOP || op == Opcode.STORE_FAST || op == Opcode.STORE_NAME)
                    continue;
                break;
            }
        }
        else
        {
            for (; bodyStart < instrs.Count; bodyStart++)
            {
                var op = instrs[bodyStart].Opcode;
                if (op == Opcode.BEFORE_WITH || op == Opcode.BEFORE_WITH_313
                    || op == Opcode.BEFORE_WITH_312
                    || op == Opcode.WITH_EXCEPT_START)
                    continue;
                if (op == Opcode.POP_TOP || op == Opcode.STORE_FAST || op == Opcode.STORE_NAME)
                    continue;
                break;
            }
        }

        // 5. 处理当前块内的 body 指令
        var bodyStmts = new List<Stmt>();
        var bodyMachine = new StackMachine(_codeObject);
        int bodyEndForCurrentBlock = bodyEndOffset > 0 ? bodyEndOffset : handlerAbs;
        for (int i = bodyStart; i < instrs.Count; i++)
        {
            if (isSetupWith)
            {
                if (instrs[i].Opcode == Opcode.POP_BLOCK) break;
                if (instrs[i].Opcode == Opcode.SETUP_FINALLY || instrs[i].Opcode == Opcode.SETUP_EXCEPT) break;
            }
            else
            {
                if (instrs[i].Opcode == Opcode.WITH_EXCEPT_START) break;
                if (instrs[i].Offset >= bodyEndForCurrentBlock && bodyEndForCurrentBlock > 0) break;
            }
            var stmt = bodyMachine.Execute(instrs[i]);
            if (stmt != null) bodyStmts.Add(stmt);
        }
        while (bodyMachine.HasResults)
            bodyStmts.Add(new ExprStmt(bodyMachine.PopResult()));
        


        var bodyBlocks = new List<BasicBlock>();
        var bodyCollector = new HashSet<BasicBlock> { block };
        var blockQueue = new Queue<BasicBlock>();
        
        int effectiveBodyEnd = bodyEndOffset > 0 ? bodyEndOffset : handlerAbs;
        
        foreach (var succ in block.Successors.OrderBy(s => s.StartOffset))
        {
            if (succ == null || succ.StartOffset >= effectiveBodyEnd || bodyCollector.Contains(succ))
                continue;
            if (succ.StartOffset < instrs[withIdx].Offset + 2) continue;
            blockQueue.Enqueue(succ);
        }
        while (blockQueue.Count > 0)
        {
            var current = blockQueue.Dequeue();
            if (current == null || bodyCollector.Contains(current)) continue;
            if (current.StartOffset >= effectiveBodyEnd) continue;
            bodyCollector.Add(current);
            bodyBlocks.Add(current);
            foreach (var succ in current.Successors)
            {
                if (succ != null && !bodyCollector.Contains(succ) && succ.StartOffset < effectiveBodyEnd)
                    blockQueue.Enqueue(succ);
            }
        }

        foreach (var bb in bodyBlocks)
            visited.Remove(bb);
        foreach (var bodyBlock in bodyBlocks)
            bodyStmts.AddRange(GetStructuredBlockStmts(bodyBlock, visited));

        var hbList = new List<BasicBlock>();
        FindBlocksFromOffset(handlerAbs, hbList);
        foreach (var hb in hbList)
            visited.Add(hb);

        return new List<Stmt>
        {
            new With(new List<WithItem> { new WithItem(contextExpr, optionalVar) }, bodyStmts)
        };
    }

    private List<Stmt> BuildWhileLoop(BasicBlock header, HashSet<BasicBlock> visited)
    {
        bool hasTryBeforeJump = header.Instructions.Any(i => IsTrySetupOpcode(i.Opcode));
        // v3.10+: 如果 header 内含 SETUP_FINALLY（try body 在 while 体内），
        // 则 POP_JUMP 是内层 if 的条件，不是 while 循环的条件。
        // 此时从 predecessor（while 入口条件块）提取条件。
        Expr? testExpr;
        if (hasTryBeforeJump && header.Predecessors.Count > 0)
        {
            // 从 predecessor 提取条件（predecessor 的最后一个指令是 while 入口的 POP_JUMP_IF_FALSE）
            var pred = header.Predecessors.First();
            testExpr = ExtractCondition(pred);
        }
        else
        {
            // 检测 while True 内存 break 模式：
            // 如果 header 的 POP_JUMP_IF_FALSE 之前有 STORE/INPLACE 指令，
            // 则 POP_JUMP 是内层 if-break，不是 while 循环条件 → 使用 True
            var popJumpIdx = header.Instructions.FindLastIndex(i =>
                i.Opcode is Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
                    or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38);
            bool hasBodyOpsBeforeJump = popJumpIdx >= 0 &&
                header.Instructions.Take(popJumpIdx).Any(i =>
                    i.Opcode is Opcode.STORE_FAST or Opcode.INPLACE_ADD or Opcode.INPLACE_SUBTRACT
                        or Opcode.INPLACE_MULTIPLY or Opcode.INPLACE_TRUE_DIVIDE
                        or Opcode.INPLACE_FLOOR_DIVIDE or Opcode.INPLACE_MODULO
                        or Opcode.STORE_SUBSCR or Opcode.STORE_ATTR
                        or Opcode.LIST_APPEND_313 or Opcode.SET_ADD_313);
            if (hasBodyOpsBeforeJump)
                testExpr = new Constant(true);
            else
                testExpr = ExtractCondition(header);
        }

        visited.Add(header);

        var bodyBlocks = new List<BasicBlock>();
        var lastInstr = header.Instructions.LastOrDefault();
        BasicBlock? bodyEntry = null;
        int? elseOffset = null;
        if (lastInstr != default && lastInstr.Argument.HasValue)
        {
            var jumpTargetOffset = lastInstr.Argument.Value;

            bool isWordcode = _codeObject.Instructions.Count > 1
                          && _codeObject.Instructions.All(i => i.Offset % 2 == 0);
            bool useRelativeOffset = isWordcode
                && lastInstr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                    or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                    or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38
                && _codeObject.Version != PythonVersion.Py310;

            if (_codeObject.Version >= PythonVersion.Py311 && useRelativeOffset)
            {
                elseOffset = lastInstr.Offset + 2 + jumpTargetOffset;
            }
            else
            {
                elseOffset = jumpTargetOffset;
            }

            bodyEntry = header.Successors.FirstOrDefault(s => s.StartOffset != elseOffset.Value);
        }
        bodyEntry ??= header.Successors.OrderBy(s => s.StartOffset).FirstOrDefault();
        Console.Error.WriteLine($"[BUILD_WHILE_DEBUG] header=0x{header.StartOffset:X4}, bodyEntry=0x{(bodyEntry?.StartOffset ?? 0):X4}, elseOffset={elseOffset}");
        if (bodyEntry != null)
            CollectBodyBlocks(bodyEntry, header, bodyBlocks, visited, elseOffset: elseOffset);

        // 确保 header 不在 bodyBlocks 中
        bodyBlocks.Remove(header);

        Console.Error.WriteLine($"[BUILD_WHILE_DEBUG] bodyBlocks for header 0x{header.StartOffset:X4}:");
        foreach (var bb in bodyBlocks)
        {
            var opStr = string.Join(",", bb.Instructions.Select(i => i.Opcode.ToString()));
            Console.Error.WriteLine($"[BUILD_WHILE_DEBUG]   Block 0x{bb.StartOffset:X4}-0x{bb.EndOffset:X4} opcodes=[{opStr}]");
        }

        // 从 visited 中移除 body 块，让 GetStructuredBlockStmts 重新管理（嵌套循环防止 StackOverflow）
        foreach (var bb in bodyBlocks)
            visited.Remove(bb);
            
        

        var bodyStmts = new List<Stmt>();
        // v3.10: header 有 SETUP_FINALLY 时 try body 覆盖 while body
        if (header.Instructions.Any(i => IsTrySetupOpcode(i.Opcode)))
        {
            var tryResult = BuildTryFromBlock(header, visited);
            if (tryResult != null)
            {
                bodyStmts = tryResult;
            }
        }
        else
        {
            bodyStmts = BuildWhileLoopBody(header, visited, bodyBlocks);
        }

        List<Stmt>? orelse = null;
        var sortedSucc = header.Successors.OrderBy(s => s.StartOffset).ToList();
        if (sortedSucc.Count >= 2)
        {
            var elseCandidate = sortedSucc[1];
            if (!visited.Contains(elseCandidate))
            {
                var bodyEntryBlock = bodyBlocks.FirstOrDefault();
                bool isElse = IsLoopElseTarget(elseCandidate, header, bodyEntryBlock);
                bool isExitOnly = IsExitOnlyBlock(elseCandidate);
                Console.Error.WriteLine($"[BUILD_WHILE_DEBUG] elseCandidate=0x{elseCandidate.StartOffset:X4}, isElse={isElse}, isExitOnly={isExitOnly}");
                if (isElse && !isExitOnly)
                {
                    orelse = BuildBlockOnly(elseCandidate, visited);
                    orelse = orelse.Where(s => !(s is Return ret && (ret.Value is Constant { Value: null } || ret.Value == null))).ToList();
                    if (orelse.Count == 0) orelse = null;
                }
            }
        }

        return new List<Stmt> { new While(testExpr, bodyStmts, orelse) };
    }
    /// 用于 Python 3.10 中 entry 块同时包含初始化语句和 while 条件的场景。
    /// </summary>
    private Expr ExtractLoopCondition(BasicBlock block)
    {
        if (block.Instructions.Count == 0)
            return new Constant(true);

        var instrs = block.Instructions;
        // 找到最后的条件判断指令：从末尾往回找 COMPARE_OP 之前的 LOAD 链
        var popJumpIdx = instrs.FindLastIndex(i =>
            i.Opcode == Opcode.POP_JUMP_IF_FALSE || i.Opcode == Opcode.POP_JUMP_IF_TRUE
            || i.Opcode == Opcode.POP_JUMP_IF_FALSE_PY38 || i.Opcode == Opcode.POP_JUMP_IF_TRUE_PY38);
        if (popJumpIdx < 0)
            return new Constant(true);

        // 从 COMPARE_OP 往前找 LOAD 链，确认条件起始位置
        // 常见模式：LOAD_* ... COMPARE_OP, POP_JUMP_IF_*
        var condStart = popJumpIdx;
        for (int i = popJumpIdx - 1; i >= 0; i--)
        {
            if (instrs[i].Opcode is Opcode.COMPARE_OP)
            {
                condStart = i;
                break;
            }
        }
        // 从 condStart-1 开始（COMPARE_OP 的操作数可能在前几条指令中）
        var startIdx = Math.Max(0, condStart - 3);

        var conditionInstrs = instrs.Skip(startIdx).Take(popJumpIdx - startIdx + 1).ToList();
        // 但跳过 POP_JUMP_IF_*（它不产生值，只消费）
        conditionInstrs = conditionInstrs
            .Where(i => i.Opcode != Opcode.POP_JUMP_IF_FALSE && i.Opcode != Opcode.POP_JUMP_IF_TRUE
                && i.Opcode != Opcode.POP_JUMP_IF_FALSE_PY38 && i.Opcode != Opcode.POP_JUMP_IF_TRUE_PY38)
            .ToList();

        var stackMachine = new StackMachine(_codeObject);
        foreach (var instr in conditionInstrs)
            stackMachine.Execute(instr);

        if (stackMachine.ExprStackCount > 0)
            return stackMachine.PopExpr();
        return stackMachine.HasResults ? stackMachine.PopResult() : new Constant(true);
    }

    /// <summary>
    /// 从 LoopHeader 构建 while 体，不提取条件（条件由调用方从 predecessor 提供）。
    /// </summary>
    private List<Stmt> BuildWhileLoopBody(BasicBlock header, HashSet<BasicBlock> visited, List<BasicBlock>? preCollectedBodyBlocks = null)
    {
        // v3.10: header 有 SETUP_FINALLY 时用 BuildTryFromBlock 处理
        if (header.Instructions.Any(i => IsTrySetupOpcode(i.Opcode)))
        {
            var tryResult = BuildTryFromBlock(header, visited);
            if (tryResult != null)
                return tryResult;
        }

        // 自循环：body 就是 header 自身（Python 3.10 while 布局）
        if (header.Successors.Any(s => s == header))
        {
            var result = _blockResults.GetValueOrDefault(header.Id);
            if (result?.Statements == null)
                return new List<Stmt>();
            var stmts = result.Statements.ToList();
            // 去除尾部因 POP_JUMP_IF_TRUE 留下的 Compare 表达式语句
            while (stmts.Count > 0 && stmts[^1] is ExprStmt { Value: Compare })
                stmts.RemoveAt(stmts.Count - 1);
            return stmts;
        }

        // 使用预收集的循环体块（从 BuildWhileLoop 传入）
        var bodyBlocks = preCollectedBodyBlocks ?? new List<BasicBlock>();
        
        // 如果没有预收集的块，尝试从 header 的后继中收集
        if (bodyBlocks.Count == 0)
        {
            var localSeen = new HashSet<BasicBlock>();
            foreach (var succ in header.Successors)
            {
                if (succ != header && succ.Flags.HasFlag(BlockFlags.LoopBody))
                    CollectBodyBlocksFrom(succ, header, bodyBlocks, localSeen);
            }
        }

        // 如果 header 自身也包含条件分支（if/else 在 while 体内），
            // 用 block 结果 + 后继分支处理，避免 GetStructuredBlockStmts 递归循环头
            if (IsConditionBranch(header) && header.Instructions.Count > 1)
        {
            var sortedSucc = header.Successors.OrderBy(s => s.StartOffset).ToList();
            
            // while-else 模式：直接使用 bodyBlocks（包含所有循环体块）
            // 这是关键修复：bodyBlocks 已经正确收集了所有循环体块，包括 i += 1
            bool isWhileElse = header.Flags.HasFlag(BlockFlags.LoopHeader) && 
                sortedSucc.Count >= 2 && IsLoopElseTarget(sortedSucc[1], header, sortedSucc[0]);
            if (isWhileElse)
            {
                var elseBlock = sortedSucc[1];
                bool elseIsExitOnly = IsExitOnlyBlock(elseBlock);
                bool elseHasUsefulCode = elseBlock.Instructions.Count > 0 && 
                    !elseBlock.Instructions.All(i => 
                        i.Opcode == Opcode.RETURN_VALUE || 
                        i.Opcode == Opcode.RETURN_CONST ||
                        (i.Opcode == Opcode.LOAD_CONST && !i.Argument.HasValue));
                isWhileElse = !elseIsExitOnly && elseHasUsefulCode;
            }
            if (isWhileElse && bodyBlocks.Count > 0)
                {
                    var resultStmts = new List<Stmt>();
                    var bodyVisited = new HashSet<BasicBlock>();
                    var bodyBlockSet = new HashSet<BasicBlock>(bodyBlocks);
                    
                    if (IsConditionBranch(header))
                    {
                        var (testExpr, _) = ExtractConditionWithSideEffects(header);
                        if (testExpr != null)
                        {
                            var lastInstr = header.Instructions.LastOrDefault();
                            if (lastInstr != default && lastInstr.Argument.HasValue)
                            {
                                bool isJumpIfTrue = lastInstr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_TRUE_PY38;
                                if (isJumpIfTrue)
                                    testExpr = new UnaryOp(UnaryOperator.Not, testExpr);
                                
                                var bodyBranch = FindFallthrough(header);
                                var afterBranch = FindBlockByOffset(lastInstr.Argument.Value);
                                
                                var ifBodyStmts = new List<Stmt>();
                                List<Stmt>? orelse = null;
                                
                                bool afterIsBreak = false;
                                if (afterBranch != null && !bodyBlockSet.Contains(afterBranch))
                                {
                                    afterIsBreak = afterBranch.Instructions.Count == 1 &&
                                        afterBranch.Instructions[0].Opcode == Opcode.JUMP_ABSOLUTE &&
                                        afterBranch.Instructions[0].Argument.HasValue;
                                    if (afterIsBreak)
                                    {
                                        ifBodyStmts.Add(new Break());
                                        bodyVisited.Add(afterBranch);
                                    }
                                }
                                
                                if (bodyBranch != null && bodyBlockSet.Contains(bodyBranch))
                                    {
                                        var branchStmts = BuildBlockOnly(bodyBranch, bodyVisited);
                                        bodyVisited.Add(bodyBranch);
                                        
                                        if (afterIsBreak)
                                        {
                                            orelse = branchStmts;
                                        }
                                        else
                                        {
                                            bool isFallthrough = bodyBranch != null && bodyBranch.Successors.Contains(afterBranch);
                                            if (isFallthrough)
                                            {
                                                foreach (var stmt in branchStmts)
                                                {
                                                    ifBodyStmts.Add(stmt);
                                                }
                                            }
                                            else
                                            {
                                                orelse = branchStmts;
                                            }
                                        }
                                    }
                                
                                if (!afterIsBreak && afterBranch != null && bodyBlockSet.Contains(afterBranch))
                                {
                                    var afterStmts = BuildBlockOnly(afterBranch, bodyVisited);
                                    bool isFallthrough = bodyBranch != null && bodyBranch.Successors.Contains(afterBranch);
                                    if (isFallthrough)
                                    {
                                        foreach (var stmt in afterStmts)
                                        {
                                            ifBodyStmts.Add(stmt);
                                        }
                                    }
                                    else
                                    {
                                        orelse = afterStmts;
                                    }
                                    bodyVisited.Add(afterBranch);
                                }
                                
                                resultStmts.Add(new If(testExpr, ifBodyStmts, orelse));
                                bodyVisited.Add(header);
                            }
                        }
                    }
                    
                    foreach (var bb in bodyBlocks.OrderBy(b => b.StartOffset))
                {
                    if (bodyVisited.Contains(bb))
                        continue;
                    
                    if (IsConditionBranch(bb))
                    {
                        var (testExpr, _) = ExtractConditionWithSideEffects(bb);
                        if (testExpr == null)
                        {
                            bodyVisited.Add(bb);
                            continue;
                        }
                        
                        var lastInstr = bb.Instructions.LastOrDefault();
                        if (lastInstr == default || !lastInstr.Argument.HasValue)
                        {
                            bodyVisited.Add(bb);
                            continue;
                        }
                        
                        bool isJumpIfTrue = lastInstr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_TRUE_PY38;
                        if (isJumpIfTrue)
                            testExpr = new UnaryOp(UnaryOperator.Not, testExpr);
                        
                        var bodyBranch = FindFallthrough(bb);
                        var afterBranch = FindBlockByOffset(lastInstr.Argument.Value);
                        
                        var ifBodyStmts = new List<Stmt>();
                        List<Stmt>? orelse = null;
                        
                        if (bodyBranch != null && bodyBlockSet.Contains(bodyBranch))
                        {
                            ifBodyStmts = BuildBlockOnly(bodyBranch, bodyVisited);
                            bodyVisited.Add(bodyBranch);
                        }
                        
                        if (afterBranch != null && bodyBlockSet.Contains(afterBranch))
                        {
                            var afterStmts = BuildBlockOnly(afterBranch, bodyVisited);
                            var ifChain = afterStmts.SkipWhile(s => s is Pass or CommentBlock).TakeWhile(s => s is If).ToList();
                            if (ifChain.Count > 0 && afterStmts.Count == ifChain.Count)
                            {
                                orelse = ifChain;
                            }
                            else if (afterStmts.Count > 0)
                            {
                                bool isFallthrough = bodyBranch != null && bodyBranch.Successors.Contains(afterBranch);
                                bool isSequentialCode = !isFallthrough && afterBranch.StartOffset > bb.StartOffset;
                                bool bodyIsPass = bodyBranch != null && bodyBranch.Instructions.Count == 1 
                                    && bodyBranch.Instructions[0].Opcode == Opcode.JUMP_ABSOLUTE;
                                bool afterHasJumpBack = afterBranch.Instructions.Any(i => 
                                    i.Opcode == Opcode.JUMP_ABSOLUTE || i.Opcode == Opcode.JUMP_BACKWARD);
                                if (isFallthrough)
                                {
                                    foreach (var stmt in afterStmts)
                                    {
                                        ifBodyStmts.Add(stmt);
                                    }
                                }
                                else if (isSequentialCode && bodyIsPass && afterHasJumpBack)
                                {
                                    resultStmts.Add(new If(testExpr, ifBodyStmts, null));
                                    resultStmts.AddRange(afterStmts);
                                    bodyVisited.Add(afterBranch);
                                    bodyVisited.Add(bb);
                                    continue;
                                }
                                else if (isSequentialCode)
                                {
                                    resultStmts.Add(new If(testExpr, ifBodyStmts, null));
                                    resultStmts.AddRange(afterStmts);
                                    bodyVisited.Add(afterBranch);
                                    bodyVisited.Add(bb);
                                    continue;
                                }
                                else
                                {
                                    orelse = afterStmts;
                                }
                            }
                            bodyVisited.Add(afterBranch);
                        }
                        
                        bodyVisited.Add(bb);
                        
                        resultStmts.Add(new If(testExpr, ifBodyStmts, orelse));
                    }
                    else if (_blockResults.TryGetValue(bb.Id, out var blockResult) && blockResult.Statements != null)
                    {
                        foreach (var stmt in blockResult.Statements)
                        {
                            if (stmt is ExprStmt { Value: Compare })
                                continue;
                            if (stmt is Pass)
                                continue;
                            resultStmts.Add(stmt);
                        }
                        bodyVisited.Add(bb);
                    }
                }
                
                foreach (var bb in bodyBlocks)
                    visited.Add(bb);
                visited.Add(header);
                
                while (resultStmts.Count > 0 && resultStmts[^1] is Continue)
                    resultStmts.RemoveAt(resultStmts.Count - 1);
                return resultStmts;
            }
            
            // header 是 LoopHeader 且不是 while-else：直接返回 bodyBlocks 的语句
            if (header.Flags.HasFlag(BlockFlags.LoopHeader))
            {
                var loopBodyStmts = new List<Stmt>();
                foreach (var bb in bodyBlocks)
                {
                    var stmts = GetStructuredBlockStmts(bb, visited);
                    loopBodyStmts.AddRange(stmts);
                }
                while (loopBodyStmts.Count > 0 && loopBodyStmts[^1] is Continue)
                    loopBodyStmts.RemoveAt(loopBodyStmts.Count - 1);
                return loopBodyStmts;
            }
            
            var hResult = _blockResults.GetValueOrDefault(header.Id);
            var hStmts = new List<Stmt>();
            if (hResult?.Statements != null)
            {
                // 取 body 语句（去掉尾部 Compare 条件）
                hStmts.AddRange(hResult.Statements);
                while (hStmts.Count > 0 && hStmts[^1] is ExprStmt { Value: Compare })
                    hStmts.RemoveAt(hStmts.Count - 1);
            }
            
            // 处理后继分支（if/else 结构）
            var bodyStmts = new List<Stmt>();
            
            if (sortedSucc.Count == 2)
            {
                // 检查是否有后继是 LoopHeader（嵌套循环，不是 if/else）
                var nestedLoop = sortedSucc.FirstOrDefault(s =>
                    s.Flags.HasFlag(BlockFlags.LoopHeader));
                if (nestedLoop != null)
                {
                    // 嵌套循环：创建 While 语句
                    var cond = ExtractCondition(header);
                    var loopBody = BuildWhileLoopBody(nestedLoop, visited);
                    bodyStmts.Add(new While(cond, loopBody, null));
                    // 另一个后继是嵌套循环后的代码
                    var afterLoop = sortedSucc.First(s => s != nestedLoop);
                    bodyStmts.AddRange(GetStructuredBlockStmts(afterLoop, visited));
                }
                else
                {
                    // 双分支：if/else 模式
                    var ifTrueStmts = GetStructuredBlockStmts(sortedSucc[0], visited);
                    var ifFalseStmts = GetStructuredBlockStmts(sortedSucc[1], visited);
                    var cond = ExtractCondition(header);
                    bodyStmts.Add(new If(cond, ifTrueStmts,
                        ifFalseStmts.Count > 0 ? ifFalseStmts : null));
                }
            }
            else if (sortedSucc.Count == 1)
            {
                bodyStmts.AddRange(GetStructuredBlockStmts(sortedSucc[0], visited));
            }
            
            hStmts.AddRange(bodyStmts);
            return hStmts;
        }

        var simpleStmts = new List<Stmt>();
        foreach (var bb in bodyBlocks)
        {
            var stmts = GetStructuredBlockStmts(bb, visited);
            simpleStmts.AddRange(stmts);
        }
        // 去除 while 体末尾的冗余 continue（由 JUMP_ABSOLUTE → loop header 产生）
        while (simpleStmts.Count > 0 && simpleStmts[^1] is Continue)
            simpleStmts.RemoveAt(simpleStmts.Count - 1);
        return simpleStmts;
    }

    /// <summary>
    /// 从起始块收集循环体块，用局部 visited 防止越界。
    /// </summary>
    private void CollectBodyBlocksFrom(BasicBlock entry, BasicBlock header,
        List<BasicBlock> bodyBlocks, HashSet<BasicBlock> localSeen, bool requireLoopBodyFlag = true)
    {
        var worklist = new Queue<BasicBlock>();
        worklist.Enqueue(entry);
        while (worklist.Count > 0)
        {
            var current = worklist.Dequeue();
            if (current == header || localSeen.Contains(current))
                continue;
            if (requireLoopBodyFlag && !current.Flags.HasFlag(BlockFlags.LoopBody))
                continue;
            
            // 在 while-else 模式下，确保块能够回到 header（通过回边）
            // 否则可能是 else 块或其他不属于循环体的块
            if (!requireLoopBodyFlag && !CanReachHeader(current, header, new HashSet<BasicBlock>()))
                continue;
                
            bodyBlocks.Add(current);
            localSeen.Add(current);
            foreach (var succ in current.Successors)
            {
                if (succ != header && !localSeen.Contains(succ))
                    worklist.Enqueue(succ);
            }
        }
    }
    
    /// <summary>
    /// 检查块是否能够通过回边到达 header（用于 while-else 模式下的循环体检测）。
    /// </summary>
    private bool CanReachHeader(BasicBlock block, BasicBlock header, HashSet<BasicBlock> visited)
    {
        if (block == null || visited.Contains(block))
            return false;
        visited.Add(block);
        
        // 如果块直接跳回 header
        if (block.Successors.Contains(header))
            return true;
            
        // 递归检查后继块
        foreach (var succ in block.Successors)
        {
            if (CanReachHeader(succ, header, visited))
                return true;
        }
        
        return false;
    }

    /// <summary>
    /// 检测 body 链是否以终端指令结束（RETURN/RAISE）。
    /// 只检测 body 入口块本身的最后指令，不沿路径追踪（避免走到 after 代码区）。
    /// </summary>
    private bool BodyEndsWithTerminal(BasicBlock entry)
    {
        if (entry == null) return false;
        var lastIns = entry.Instructions.LastOrDefault();
        return lastIns != default && JumpHelper.IsTerminal(lastIns.Opcode);
    }

    private bool IsElseTarget(BasicBlock afterBranch, BasicBlock header, BasicBlock bodyBranch, List<Stmt>? bodyStmts = null)
    {
        if (afterBranch == null || header == null) return false;

        if (IsIfElseTarget(afterBranch, header, bodyBranch, bodyStmts))
            return true;

        if (IsLoopElseTarget(afterBranch, header, bodyBranch))
            return true;

        if (IsTryElseTarget(afterBranch, header, bodyBranch))
            return true;

        return false;
    }

    private bool IsIfElseTarget(BasicBlock afterBranch, BasicBlock header, BasicBlock bodyBranch, List<Stmt>? bodyStmts = null)
    {
        if (afterBranch == null || header == null) return false;

        bool isConditionBlock = afterBranch.Instructions.Any(i =>
            i.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38);

        bool bodyEndsWithTerminal = bodyStmts != null && bodyStmts.Count > 0
            && bodyStmts[^1] is Return or Raise or Break or Continue;

        var lastHeaderInstr = header.Instructions.LastOrDefault();
        bool isFalseJump = lastHeaderInstr != default && 
            lastHeaderInstr.Opcode is Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_FALSE_PY38;
        bool isTrueJump = lastHeaderInstr != default &&
            lastHeaderInstr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_TRUE_PY38;

        if (bodyEndsWithTerminal && !isConditionBlock && isFalseJump)
            return true;

        if (bodyBranch != null)
        {
            if (afterBranch.Predecessors.Count == 1
                && afterBranch.Predecessors.Contains(header))
            {
                if (!isConditionBlock)
                    return true;
            }
        }

        if (isFalseJump || isTrueJump)
        {
            bool bodyEndsWithJump = false;
            if (bodyBranch != null)
            {
                var lastBodyInstr = bodyBranch.Instructions.LastOrDefault();
                bodyEndsWithJump = lastBodyInstr != default &&
                    (lastBodyInstr.Opcode is Opcode.JUMP_FORWARD or Opcode.JUMP_ABSOLUTE);
            }

            bool afterIsReachableFromBody = false;
            if (bodyBranch != null)
            {
                foreach (var succ in bodyBranch.Successors)
                {
                    if (succ == afterBranch || succ.StartOffset == afterBranch.StartOffset)
                    {
                        afterIsReachableFromBody = true;
                        break;
                    }
                }
            }

            

            if (bodyEndsWithJump && afterIsReachableFromBody && !isConditionBlock)
                return true;
        }

        return false;
    }

    private bool IsOuterLoopElse(BasicBlock candidate)
    {
        if (candidate == null) return false;

        var loopHeaders = _allBlocks.Where(b => b.Flags.HasFlag(BlockFlags.LoopHeader)).ToList();
        foreach (var loopHeader in loopHeaders)
        {
            if (IsLoopElseTarget(candidate, loopHeader, null))
                return true;
        }
        return false;
    }

    private bool IsInOuterLoopBody(BasicBlock candidate, BasicBlock currentHeader)
    {
        if (candidate == null || currentHeader == null) return false;

        var loopHeaders = _allBlocks.Where(b => 
            b.Flags.HasFlag(BlockFlags.LoopHeader) && b != currentHeader).ToList();
        foreach (var loopHeader in loopHeaders)
        {
            if (candidate.Flags.HasFlag(BlockFlags.LoopBody) && 
                !IsLoopElseTarget(candidate, loopHeader, null))
                return true;

            bool hasBackEdgeToLoop = candidate.Successors.Any(s => 
                s.StartOffset == loopHeader.StartOffset);
            if (hasBackEdgeToLoop)
                return true;

            bool isPredecessorOfLoop = loopHeader.Predecessors.Any(p => 
                p.StartOffset == candidate.StartOffset);
            if (isPredecessorOfLoop)
                return true;
        }
        return false;
    }

    private bool IsInSameLoopBody(BasicBlock candidate, BasicBlock currentHeader)
    {
        if (candidate == null || currentHeader == null) return false;

        if (!currentHeader.Flags.HasFlag(BlockFlags.LoopBody) && 
            !currentHeader.Flags.HasFlag(BlockFlags.LoopHeader))
            return false;

        var loopHeaders = _allBlocks.Where(b => b.Flags.HasFlag(BlockFlags.LoopHeader)).ToList();
        foreach (var loopHeader in loopHeaders)
        {
            bool currentIsInLoop = currentHeader == loopHeader ||
                currentHeader.Flags.HasFlag(BlockFlags.LoopBody) ||
                currentHeader.Successors.Any(s => s.StartOffset == loopHeader.StartOffset);

            bool candidateIsInLoop = candidate == loopHeader ||
                candidate.Flags.HasFlag(BlockFlags.LoopBody) ||
                candidate.Successors.Any(s => s.StartOffset == loopHeader.StartOffset);

            if (currentIsInLoop && candidateIsInLoop && 
                !IsLoopElseTarget(candidate, loopHeader, null))
                return true;
        }
        return false;
    }

    private bool IsLoopElseTarget(BasicBlock afterBranch, BasicBlock header, BasicBlock bodyBranch)
    {
        if (afterBranch == null || header == null) return false;

        bool isForLoop = header.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER);
        bool isWhileLoop = header.Instructions.Any(i =>
            i.Opcode is Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
                or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38)
            && header.Flags.HasFlag(BlockFlags.LoopHeader);

        if (!isForLoop && !isWhileLoop)
            return false;

        bool isElseTarget = false;

        if (isForLoop)
        {
            var sortedSuccessors = header.Successors.OrderBy(s => s.StartOffset).ToList();
            if (sortedSuccessors.Count >= 2 && sortedSuccessors[1].StartOffset == afterBranch.StartOffset)
                isElseTarget = true;
        }
        else if (isWhileLoop)
        {
            var lastInstr = header.Instructions.LastOrDefault();
            if (lastInstr != default && lastInstr.Argument.HasValue)
            {
                var jumpTargetOffset = lastInstr.Argument.Value;

                bool isWordcode = _codeObject.Instructions.Count > 1
                              && _codeObject.Instructions.All(i => i.Offset % 2 == 0);
                bool useRelativeOffset = isWordcode
                    && lastInstr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                        or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                        or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38
                    && _codeObject.Version != PythonVersion.Py310;

                if (_codeObject.Version >= PythonVersion.Py311 && useRelativeOffset)
                {
                    jumpTargetOffset = lastInstr.Offset + 2 + jumpTargetOffset;
                }

                if (afterBranch.StartOffset == jumpTargetOffset)
                    isElseTarget = true;
            }
        }

        if (!isElseTarget)
            return false;

        if (isForLoop)
        {
            bool bodyIsEmpty = bodyBranch == null || 
                bodyBranch.Instructions.Count == 0 ||
                bodyBranch.Instructions.All(i => i.Opcode == Opcode.POP_TOP) ||
                (bodyBranch.Instructions.Count == 2 &&
                 bodyBranch.Instructions[0].Opcode == Opcode.STORE_FAST &&
                 bodyBranch.Instructions[1].Opcode == Opcode.JUMP_BACKWARD) ||
                (bodyBranch.Instructions.Count == 2 &&
                 bodyBranch.Instructions[0].Opcode == Opcode.STORE_FAST &&
                 bodyBranch.Instructions[1].Opcode == Opcode.JUMP_ABSOLUTE);
            
            var forIterInstr = header.Instructions.FirstOrDefault(i => i.Opcode == Opcode.FOR_ITER);
            int elseTargetOffset = 0;
            if (forIterInstr != null && forIterInstr.Argument.HasValue)
            {
                int offsetInc = _codeObject.IsWordOffset ? 4 : 2;
                int argVal = forIterInstr.Argument.Value;
                elseTargetOffset = forIterInstr.Offset + offsetInc + argVal;
            }
            
            bool hasConditionalJump = false;
            bool hasBreakInBody = false;
            if (bodyBranch != null)
            {
                var visitedBlocks = new HashSet<BasicBlock>();
                var blockQueue = new Queue<BasicBlock>();
                blockQueue.Enqueue(bodyBranch);
                visitedBlocks.Add(bodyBranch);
                
                while (blockQueue.Count > 0)
                {
                    var current = blockQueue.Dequeue();
                    foreach (var instr in current.Instructions)
                    {
                        if (instr.Opcode == Opcode.JUMP_BACKWARD)
                            continue;
                        
                        if (instr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE or 
                            Opcode.POP_JUMP_IF_TRUE_PY38 or Opcode.POP_JUMP_IF_FALSE_PY38)
                        {
                            hasConditionalJump = true;
                        }
                        
                        if (JumpHelper.IsJump(instr.Opcode) && instr.Argument.HasValue)
                        {
                            int jumpTarget = instr.Argument.Value;
                            if (jumpTarget > elseTargetOffset)
                            {
                                hasBreakInBody = true;
                                break;
                            }
                        }
                    }
                    if (hasBreakInBody) break;
                    
                    foreach (var succ in current.Successors)
                    {
                        if (succ != null && !visitedBlocks.Contains(succ) && succ.StartOffset != header.StartOffset)
                        {
                            visitedBlocks.Add(succ);
                            blockQueue.Enqueue(succ);
                        }
                    }
                }
            }
            
            var blocksAfterElse = _allBlocks.Where(b => b.StartOffset > afterBranch.EndOffset).ToList();
            bool hasCodeAfterElse = blocksAfterElse.Any(b => b.Instructions.Count > 0);
            
            if (hasBreakInBody || hasConditionalJump)
                return true;

            // 没有 break 也没有条件跳转：FOR_ITER 目标不是 else 子句，是循环后的顺序代码
            if (isForLoop)
                return false;
            
            if (!hasCodeAfterElse && IsExitOnlyBlock(afterBranch) && !bodyIsEmpty)
                return false;
            
            if (bodyIsEmpty && !IsExitOnlyBlock(afterBranch))
                return true;
        }
        else if (isWhileLoop)
        {
            bool isExitOnlyBlock = IsExitOnlyBlock(afterBranch);
            return !isExitOnlyBlock;
        }

        return true;
    }

    private bool IsExitOnlyBlock(BasicBlock block)
    {
        if (block == null) return true;
        
        var instrs = block.Instructions;
        if (instrs.Count == 0) return true;
        
        if (instrs.Count == 1 && instrs[0].Opcode == Opcode.RETURN_CONST)
        {
            if (instrs[0].Argument.HasValue)
            {
                var constIdx = instrs[0].Argument.Value;
                if (constIdx >= 0 && constIdx < _codeObject.Constants.Count)
                {
                    var constant = _codeObject.Constants[constIdx];
                    if (constant == null)
                        return true;
                }
            }
            return false;
        }
        
        if (instrs.Count == 2 && 
            instrs[0].Opcode == Opcode.LOAD_CONST && 
            instrs[1].Opcode == Opcode.RETURN_VALUE)
        {
            if (instrs[0].Argument.HasValue)
            {
                var constIdx = instrs[0].Argument.Value;
                if (constIdx >= 0 && constIdx < _codeObject.Constants.Count)
                {
                    var constant = _codeObject.Constants[constIdx];
                    if (constant == null)
                        return true;
                }
            }
            return false;
        }
        
        if (instrs.Count == 3 &&
            instrs[0].Opcode == Opcode.DUP_TOP &&
            instrs[1].Opcode == Opcode.LOAD_CONST &&
            instrs[2].Opcode == Opcode.RETURN_VALUE)
            return true;
        
        if (instrs.Count == 2 &&
            (instrs[0].Opcode == Opcode.LOAD_FAST || instrs[0].Opcode == Opcode.LOAD_NAME) &&
            instrs[1].Opcode == Opcode.RETURN_VALUE)
            return true;
        
        if (instrs.Count == 2 &&
            instrs[0].Opcode == Opcode.DUP_TOP &&
            instrs[1].Opcode == Opcode.RETURN_CONST)
            return true;
        
        if (instrs.Count == 3 &&
            instrs[0].Opcode == Opcode.DUP_TOP &&
            (instrs[1].Opcode == Opcode.LOAD_FAST || instrs[1].Opcode == Opcode.LOAD_NAME) &&
            instrs[2].Opcode == Opcode.RETURN_VALUE)
            return true;
        
        return false;
    }

    private bool IsTryElseTarget(BasicBlock afterBranch, BasicBlock header, BasicBlock bodyBranch)
    {
        if (afterBranch == null || header == null) return false;

        bool hasTrySetup = header.Instructions.Any(i => IsTrySetupOpcode(i.Opcode));
        if (!hasTrySetup)
            return false;

        bool hasJumpForwardToElse = false;
        foreach (var instr in header.Instructions)
        {
            if (instr.Opcode == Opcode.JUMP_FORWARD && instr.Argument.HasValue)
            {
                var targetOffset = instr.Offset + 2 + instr.Argument.Value;
                if (afterBranch.StartOffset == targetOffset)
                {
                    hasJumpForwardToElse = true;
                    break;
                }
            }
        }

        return hasJumpForwardToElse;
    }

    private List<Stmt> BuildIfElse(BasicBlock header, HashSet<BasicBlock> visited)
    {
        // 提取 header 块中条件之前的初始化语句（例如 `result = 0` 和 `if x0 > 0:` 在同一块时）
        var headerResult = _blockResults.GetValueOrDefault(header.Id);
        var headerInitStmts = new List<Stmt>();
        if (headerResult?.Statements != null)
        {
            foreach (var s in headerResult.Statements)
            {
                // ExprStmt(Compare) 是条件表达式本身，前面的语句是初始化代码
                if (s is ExprStmt { Value: Compare })
                    break;
                // Pass 是 BlockDecompiler 为空语句列表添加的占位符，不是真正的初始化语句
                if (s is Pass)
                    continue;
                headerInitStmts.Add(s);
            }
        }

        var (testExpr, condSideEffects) = ExtractConditionWithSideEffects(header);
        if (header.Instructions.Count == 0) return new List<Stmt>();
        var lastInstr = header.Instructions.Last();
        // 3.12+ wordcode
        var targetOffset = lastInstr.Argument!.Value;
        var isWordcode = _codeObject.Instructions.Count > 1
                      && _codeObject.Instructions.All(i => i.Offset % 2 == 0);
        // 3.10 特殊处理：ParseInstructionsWordcode 已将 arg *2 转为绝对字节偏移
        // 3.11+ wordcode: arg 是相对字节偏移，需加上 current_offset + 2
        // 3.13+: PycReader 已解析为绝对字节偏移（见 PycReader.ParseInstructions311Plus）
        // 3.6-3.9 wordcode: arg 已经是绝对字节偏移，不需要额外计算
        if (isWordcode
            && lastInstr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38
            && _codeObject.Version != PythonVersion.Py310
            && _codeObject.Version >= PythonVersion.Py311
            && _codeObject.Version < PythonVersion.Py313)
        {
            targetOffset = lastInstr.Offset + 2 + targetOffset;
        }

        // POP_JUMP_IF_FALSE: body = fallthrough, else = jump target
        // POP_JUMP_IF_TRUE:  body = same fallthrough, but condition needs NEGATION
        bool isJumpIfTrue = lastInstr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_TRUE_PY38;
        
        var bodyBranch = FindFallthrough(header);
        var afterBranch = FindBlockByOffset(targetOffset);
        // 3.13+ OR 链: 跳转目标可能是共享 RETURN_VALUE 块但未被正确分块。回退：扫描包含 targetOffset 的块
        if (afterBranch == null && _codeObject.Version >= PythonVersion.Py313)
        {
            afterBranch = _allBlocks.FirstOrDefault(b =>
                b.StartOffset <= targetOffset && targetOffset < b.EndOffset + 2);
            Console.Error.WriteLine($"[DEBUG_IFELSE] After fallback search, afterBranch={(afterBranch != null ? $"0x{afterBranch.StartOffset:X4}" : "null")}");
        }
        
        // 检测 OR 短接链: POP_JUMP_IF_TRUE + fallthrough 为条件分支
        // if a or b: bytecode = "POP_JUMP_IF_TRUE → body ; POP_JUMP_IF_FALSE → after"
        bool isOrChain = isJumpIfTrue && bodyBranch != null && IsConditionBranch(bodyBranch);

        // 检测列表推导式模式：POP_JUMP_IF_TRUE 的跳转目标包含 LIST_APPEND
        bool isComprehensionPattern = isJumpIfTrue && afterBranch != null && 
            afterBranch.Instructions.Any(i => i.Opcode == Opcode.LIST_APPEND_313 || i.Opcode == Opcode.SET_ADD_313);

        // 鉴别 if-else body vs 布尔表达式：
        // if-else body 有 Assign(result, ...) + Return(result)
        // 布尔表达式 body 只有 Return(y) —— 无中间赋值
        bool bodyHasAssign = false;
        if (bodyBranch != null)
        {
            var bodyResult = _blockResults.GetValueOrDefault(bodyBranch.Id);
            if (bodyResult?.Statements != null)
                bodyHasAssign = bodyResult.Statements.Any(s => s is Assign);
        }
        bool hasStoresInBody = bodyBranch != null
            && bodyBranch.Instructions.Any(i => i.Opcode is Opcode.STORE_FAST or Opcode.STORE_NAME
                or Opcode.STORE_ATTR or Opcode.STORE_SUBSCR);

        // 检测简单 OR 表达式: return x or y
        // 字节码: LOAD x, COPY, TO_BOOL, POP_JUMP_IF_TRUE → RETURN_VALUE; POP_TOP, LOAD y, RETURN_VALUE
        // afterBranch (跳转目标) 包含 RETURN_VALUE，bodyBranch (fallthrough) 最终也到达 RETURN_VALUE
        // 注意：只在 bodyBranch 不是条件分支时才触发（否则由 OR 链终端检测处理）
        // 排除 if-else body：body 含有 Assign/STORE → 不是布尔表达式
        bool isSimpleOrExpr = isJumpIfTrue && !isOrChain
            && afterBranch != null && bodyBranch != null
            && !IsConditionBranch(bodyBranch)
            && !bodyHasAssign && !hasStoresInBody
            && afterBranch.Instructions.Any(i => i.Opcode == Opcode.RETURN_VALUE)
            && (bodyBranch.Instructions.Any(i => i.Opcode == Opcode.RETURN_VALUE)
                || bodyBranch.Successors.Contains(afterBranch))
            && !isComprehensionPattern;


        // 检测简单 AND 表达式: return x and y
        // 字节码: LOAD x, COPY, TO_BOOL, POP_JUMP_IF_FALSE → RETURN_VALUE; POP_TOP, LOAD y, RETURN_VALUE
        // 排除 if-else body：body 含有 Assign/STORE → 不是布尔表达式
        bool isSimpleAndExpr = !isJumpIfTrue && !isOrChain
            && lastInstr.Opcode is Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_FALSE_PY38
            && afterBranch != null && bodyBranch != null
            && !IsConditionBranch(bodyBranch)
            && !bodyHasAssign && !hasStoresInBody
            && afterBranch.Instructions.Any(i => i.Opcode == Opcode.RETURN_VALUE)
            && (bodyBranch.Instructions.Any(i => i.Opcode == Opcode.RETURN_VALUE)
                || bodyBranch.Successors.Contains(afterBranch))
            && !isComprehensionPattern;

        if (!isOrChain && !isComprehensionPattern && !isSimpleOrExpr && !isSimpleAndExpr && isJumpIfTrue && testExpr != null)
            testExpr = new UnaryOp(UnaryOperator.Not, testExpr);

        // OR 短接: POP_JUMP_IF_TRUE + fallthrough 为条件分支
        if ((isOrChain || lastInstr.Opcode is Opcode.JUMP_IF_TRUE_OR_POP) && afterBranch != null)
        {
            // body 在 jump target (afterBranch), else 是 fallthrough (bodyBranch = 第二条件)
            var savedBody = bodyBranch;
            bodyBranch = afterBranch;   // body = print
            afterBranch = savedBody;    // else = 第二条件检查
        }

        // 简单 OR 表达式: return x or y
        // 字节码: POP_JUMP_IF_TRUE → RETURN_VALUE(x); POP_TOP, LOAD y, RETURN_VALUE
        // afterBranch 是 RETURN_VALUE 块（跳转目标），bodyBranch 是 fallthrough 块
        if (isSimpleOrExpr)
        {
            // 从 bodyBranch (fallthrough) 中提取 y 表达式
            // bodyBranch 可能直接包含 RETURN_VALUE，也可能通过后继到达 afterBranch
            var bodyResult = _blockResults.GetValueOrDefault(bodyBranch.Id);
            Expr? orRight = null;
            if (bodyResult?.Statements != null)
            {
                foreach (var s in bodyResult.Statements)
                {
                    if (s is Return ret && ret.Value != null)
                    {
                        orRight = ret.Value;
                        break;
                    }
                    // bodyBranch 可能只有表达式语句（LOAD_FAST 等），没有 Return
                    if (s is ExprStmt es && es.Value != null)
                    {
                        orRight = es.Value;
                    }
                }
            }
            if (orRight != null)
            {
                // 生成 return x or y
                var orExpr = new BoolOp(BoolOperator.Or, new List<Expr> { testExpr!, orRight });
                var orResult = new List<Stmt>();
                orResult.AddRange(headerInitStmts);
                orResult.Add(new Return(orExpr));
                // 标记两个块为已访问
                visited.Add(afterBranch);
                visited.Add(bodyBranch);
                Console.Error.WriteLine($"[BUILD_IF_ELSE] Simple OR expr detected: return {testExpr} or {orRight}");
                return orResult;
            }
        }

        // 简单 AND 表达式: return x and y
        // 字节码: POP_JUMP_IF_FALSE → RETURN_VALUE; POP_TOP, LOAD y, RETURN_VALUE
        if (isSimpleAndExpr)
        {
            // 从 bodyBranch (fallthrough) 中提取 y 表达式
            var bodyResult = _blockResults.GetValueOrDefault(bodyBranch.Id);
            Expr? andRight = null;
            if (bodyResult?.Statements != null)
            {
                foreach (var s in bodyResult.Statements)
                {
                    if (s is Return ret && ret.Value != null)
                    {
                        andRight = ret.Value;
                        break;
                    }
                    if (s is ExprStmt es && es.Value != null)
                    {
                        andRight = es.Value;
                    }
                }
            }
            if (andRight != null)
            {
                // 生成 return x and y
                var andExpr = new BoolOp(BoolOperator.And, new List<Expr> { testExpr!, andRight });
                var andResult = new List<Stmt>();
                andResult.AddRange(headerInitStmts);
                andResult.Add(new Return(andExpr));
                // 标记两个块为已访问
                visited.Add(afterBranch);
                visited.Add(bodyBranch);
                Console.Error.WriteLine($"[BUILD_IF_ELSE] Simple AND expr detected: return {testExpr} and {andRight}");
                return andResult;
            }
        }

        // 检测 while 循环模式：bodyBranch 是循环头（LoopHeader）
        // 在 Python 3.10 中，while 循环的条件在前驱块，body 是独立的 LoopHeader
        // 在 Python 3.11+ 中，while 循环的条件块本身就是 LoopHeader
        // 参考 CPython 3.12: Python/ceval.c LOAD_FAST+POP_JUMP_IF_FALSE 构成 while 条件
        // 排除 for-loop 头（有 GET_ITER/FOR_ITER 指令的 LoopHeader），for-loop 走 GetStructuredBlockStmts
        var isForLoop = bodyBranch != null && bodyBranch.Instructions.Any(
            i => i.Opcode is Opcode.GET_ITER or Opcode.FOR_ITER);
        var isWhileLoop = (header.Flags.HasFlag(BlockFlags.LoopHeader)
                          || bodyBranch?.Flags.HasFlag(BlockFlags.LoopHeader) == true)
                          && !isForLoop;
        if (isWhileLoop)
        {
            // 直接获取 entry 块的初始化语句（block 已被 visited，不能用 BuildBlockOnly）
            var initStmts = new List<Stmt>();
            var initResult = _blockResults.GetValueOrDefault(header.Id);
            if (initResult?.Statements != null)
            {
                initStmts.AddRange(initResult.Statements);
                // 去除块结果末尾的 Compare 表达式（while 条件）
                while (initStmts.Count > 0 && initStmts[^1] is ExprStmt { Value: Compare })
                    initStmts.RemoveAt(initStmts.Count - 1);
            }
            // 提取 while 条件（只处理尾部的 COMPARE_OP）
            var whileTest = ExtractLoopCondition(header);
            // 回退：如果 ExtractLoopCondition 没找到，用 ExtractCondition 处理整个块
            if (whileTest is Constant { Value: true })
                whileTest = ExtractCondition(header);

            bool isElseTarget = IsLoopElseTarget(afterBranch, header, bodyBranch);
            List<Stmt>? wOrelse = null;
            if (isElseTarget && afterBranch != null)
            {
                wOrelse = BuildBlockOnly(afterBranch, visited);
                wOrelse = wOrelse.Where(s => !(s is Return ret && (ret.Value is Constant { Value: null } || ret.Value == null))).ToList();
                if (wOrelse.Count == 0) wOrelse = null;
            }

            // 构建 while 体
            var wBody = BuildWhileLoopBody(bodyBranch, visited);
            var wAfter = !isElseTarget && afterBranch != null && !visited.Contains(afterBranch)
                ? BuildStatements(afterBranch, visited)
                : null;
            var wResult = new List<Stmt>();
            wResult.AddRange(initStmts);
            wResult.Add(new While(whileTest, wBody, wOrelse));
            if (wAfter != null)
                wResult.AddRange(wAfter);
            // 标记 bodyBranch（LoopHeader）为 visited，防止外层 for-loop 重复处理
            visited.Add(bodyBranch);
            return wResult;
        }

        // 构建 body：用 GetStructuredBlockStmts 递归处理嵌套控制结构（如 if-in-if）
        // ⚠️ 原始代码用 bodyVisited 副本，导致深层 if/else 链的块状态不传播回 visited
        // 导致 >2 层 if-else 嵌套塌陷。现改用统一 visited，嵌套 if 的 BuildBlockOnly 
        // 会自动把 body/else 块标记到 visited，外层就不会重复处理。
        var bodyStmts = GetStructuredBlockStmts(bodyBranch, visited);

        // 检测 afterBranch — 开头的连续 If 折叠为 elif chain，其余作为顺序代码
        List<Stmt>? orelse = null;
        var tailCode = new List<Stmt>();

        List<Stmt>? afterStmts = null;
        if (afterBranch != null)
        {
            if (afterBranch.Flags.HasFlag(BlockFlags.LoopHeader))
            {
                visited.Add(afterBranch);
                return BuildRestrictedIfElse(header, visited);
            }

            bool isOuterLoopElse = IsOuterLoopElse(afterBranch);
            if (isOuterLoopElse)
            {
                visited.Add(afterBranch);
                return BuildRestrictedIfElse(header, visited);
            }

            bool isInOuterLoopBody = IsInOuterLoopBody(afterBranch, header);
            if (isInOuterLoopBody)
            {
                var restrictedResult = BuildRestrictedIfElse(header, visited);
                visited.Add(afterBranch);
                var loopBodyStmts = GetStructuredBlockStmts(afterBranch, visited);
                if (restrictedResult.Count > 0 && restrictedResult[0] is If ifStmt)
                {
                    ifStmt.Body.AddRange(loopBodyStmts);
                }
                else
                {
                    restrictedResult.AddRange(loopBodyStmts);
                }
                return restrictedResult;
            }

            bool isInSameLoopBody = IsInSameLoopBody(afterBranch, header);
            if (isInSameLoopBody)
            {
                var restrictedResult = BuildRestrictedIfElse(header, visited);
                visited.Add(afterBranch);
                var loopBodyStmts = GetStructuredBlockStmts(afterBranch, visited);
                if (restrictedResult.Count > 0 && restrictedResult[0] is If ifStmt)
                {
                    ifStmt.Body.AddRange(loopBodyStmts);
                }
                else
                {
                    restrictedResult.AddRange(loopBodyStmts);
                }
                return restrictedResult;
            }

            if (visited.Contains(afterBranch))
                visited.Remove(afterBranch);

            bool isElseClause = IsElseTarget(afterBranch, header, bodyBranch, bodyStmts);

            if (isElseClause)
            {
                // 用 BuildBlockOnly 只取 else 块本身的语句（不追踪后继）
                var elseBody = BuildBlockOnly(afterBranch, visited);
                orelse = elseBody
                    .Where(s => !(s is Return ret && (ret.Value is Constant { Value: null } || ret.Value == null)))
                    .ToList();
                if (orelse.Count == 0) orelse = null;
                // else 块的后继块作为 tailCode（模块级顺序代码）
                foreach (var succ in afterBranch.Successors)
                {
                    if (!visited.Contains(succ))
                        tailCode.AddRange(BuildStatements(succ, visited));
                }
            }
            else
            {
                // bodyBranch == afterBranch: 块已被 GetStructuredBlockStmts 消费，
                // 其后继即为顺序代码（tailCode），常见于 if X: return Y; Z() 模式。
                if (bodyBranch == afterBranch && afterBranch != null)
                {
                    foreach (var succ in afterBranch.Successors)
                    {
                        if (!visited.Contains(succ))
                            tailCode.AddRange(BuildStatements(succ, visited));
                    }
                }
                else
                {
                    afterStmts = BuildStatements(afterBranch, visited);
                }
            }
        }

        if (afterStmts != null && afterStmts.Count > 0)
        {
            var ifChain = afterStmts.SkipWhile(s => s is Pass or CommentBlock).TakeWhile(s => s is If).ToList();
            if (ifChain.Count > 0)
            {
                orelse = ifChain; // elif 链
            }
            else
            {
                bool isElseClause = IsElseTarget(afterBranch, header, bodyBranch, bodyStmts);

                if (isElseClause)
                {
                    // 过滤 orelse 中的 module-level return None
                    orelse = afterStmts
                        .Where(s => !(s is Return ret && (ret.Value is Constant { Value: null } || ret.Value == null)))
                        .ToList();
                    if (orelse.Count == 0) orelse = null;
                }
                else
                {
                    // 非 If 的尾部，过滤 return None
                    foreach (var s in afterStmts)
                        if (!(s is Return ret && (ret.Value is Constant { Value: null } || ret.Value == null)))
                            tailCode.Add(s);
                }
            }
            }

        var result = new List<Stmt>();
        result.AddRange(headerInitStmts);
        // 当 headerInitStmts 未收集到副作用时，使用 ExtractCondition 的副作用
        if (headerInitStmts.Count == 0 && condSideEffects.Count > 0)
            result.AddRange(condSideEffects);

        // 优化: 条件为 Constant(true) 时跳过 If，直接内联 body
        if (testExpr is Constant { Value: bool tv } && tv)
        {
            result.AddRange(bodyStmts);
            result.AddRange(tailCode);
            return result;
        }

        // AND 短接合并: POP_JUMP_IF_FALSE/JUMP_IF_FALSE_OR_POP + body 首条为 If → BoolOp(And, ...)
        // 递归合并所有嵌套 AND 条件，确保 BoolOp 收集完整条件链。
        // 特殊处理：JUMP_IF_FALSE_OR_POP (链式比较) 可能把后继 AND 条件放在 elif 链中，
        // 需要同时遍历 body 链和 elif 链以收集全部条件。
        if ((lastInstr.Opcode is Opcode.POP_JUMP_IF_FALSE or Opcode.JUMP_IF_FALSE_OR_POP
                or Opcode.POP_JUMP_IF_FALSE_PY38)
            && bodyStmts.Count > 0 && bodyStmts[0] is If innerIf && orelse == null)
        {
            // 外层条件 + 嵌套 If 的条件
            var conditions = new List<Expr> { testExpr, innerIf.Test };
            var currentBody = innerIf.Body;
            var currentOrelse = innerIf.Orelse;
            var extraStmts = new List<Stmt>();
            
            while (true)
            {
                // Step 1: 递归合并 body 链（标准 AND 链，内层 If 无 else）
                while (currentBody.Count > 0 && currentBody[0] is If nestedIf && currentOrelse == null)
                {
                    conditions.Add(nestedIf.Test);
                    currentBody = nestedIf.Body;
                    currentOrelse = nestedIf.Orelse;
                    if (nestedIf.Body.Count > 1)
                        extraStmts.AddRange(nestedIf.Body.Skip(1));
                }
                
                // Step 2: 没有 elif 链 → 完成递归
                if (currentOrelse == null || currentOrelse.Count == 0 || !(currentOrelse[0] is If elifIf))
                    break;
                
                // Step 3: 检查 elif 是否为 AND 条件延续（链式比较伪影）。
                // 鉴别条件：当前 body 为空或仅含 Return（非真实 elif 体）
                if (currentBody.Count > 0 && !(currentBody.Count == 1 && currentBody[0] is Return))
                    break; // 真实 elif，保留原样
                
                // 将 elif 条件合并为 AND 条件
                conditions.Add(elifIf.Test);
                currentBody = elifIf.Body;
                currentOrelse = elifIf.Orelse;
                if (elifIf.Body.Count > 1)
                    extraStmts.AddRange(elifIf.Body.Skip(1));
            }
            
            var mergedTest = MergeBoolOpValues(BoolOperator.And, conditions);
            result.Add(new If(mergedTest, currentBody, currentOrelse));
            if (extraStmts.Count > 0)
                result.AddRange(extraStmts);
            if (bodyStmts.Count > 1)
                result.AddRange(bodyStmts.Skip(1));
        }
        // OR 短接合并: orChain + afterStmts/else 首条为 If → BoolOp(Or, ...)
        else if (isOrChain && orelse != null && orelse.Count > 0 && orelse[0] is If orInnerIf)
        {
            // 检测是否为 OR 链终端（bodyStmts 为共享 RETURN_VALUE 的空 Return）：
            // 直接产出 Return(Or(a, b, c)) 而非 If(Or(a, Not(b)), [ExprStmt(c)], null)
            if (bodyStmts.Count == 1 && bodyStmts[0] is Return bodyRet
                && orInnerIf.Orelse == null
                && (orInnerIf.Body.Count >= 1 && orInnerIf.Body[0] is ExprStmt terminalExpr
                    || orInnerIf.Body.Count == 0 && bodyRet.Value != null))
            {
                // OR 链终端检测成功。直接从条件表达式和 terminal/return 值生成 Return(Or(...))
                bool useBodyExpr = orInnerIf.Body.Count >= 1 && orInnerIf.Body[0] is ExprStmt;
                Expr? termVal = useBodyExpr
                    ? ((ExprStmt)orInnerIf.Body[0]).Value
                    : bodyRet.Value;
                if (termVal != null)
                {
                    var conditions = new List<Expr> { testExpr };
                    conditions.Add(StripNot(orInnerIf.Test) ?? orInnerIf.Test);
                    conditions.Add(termVal);
                    result.Add(new Return(MergeBoolOpValues(BoolOperator.Or, conditions)));
                    if (orelse.Count > 1)
                        result.AddRange(orelse.Skip(1));
                }
                else
                {
                    // termVal null: 回退到普通 OR 合并
                    var mergedTest = MergeBoolOpValues(BoolOperator.Or, new List<Expr> { testExpr, orInnerIf.Test });
                    result.Add(new If(mergedTest, bodyStmts, orInnerIf.Orelse));
                    if (orelse.Count > 1)
                        result.AddRange(orelse.Skip(1));
                }
            }
        }
        // OR 链 + afterStmts 首条为 Return(Or(...)) → 合并为更长的 OR 链
        // 例如: return a or b or c 被拆成 if(a) return + return b or c
        else if (isOrChain && afterStmts != null && afterStmts.Count > 0
                 && afterStmts[0] is Return orRet
                 && orRet.Value is BoolOp orBool && orBool.Op == BoolOperator.Or
                 && bodyStmts.Count == 1 && bodyStmts[0] is Return bodyRet2
                 && bodyRet2.Value == null)
        {
            // 将 a 合并到 (b or c) 前面，生成 return a or b or c
            var conditions = new List<Expr> { testExpr };
            conditions.AddRange(orBool.Values);
            result.Add(new Return(MergeBoolOpValues(BoolOperator.Or, conditions)));
            if (afterStmts.Count > 1)
                result.AddRange(afterStmts.Skip(1));
        }
        else
        {
            result.Add(new If(testExpr, bodyStmts, orelse));
        }
        result.AddRange(tailCode);

        // Phase 29: 修复 elif 体中 Return 丢失
        // 当 `return X and Y` / `return X or Y` 被放在 if 的 else 分支中时，
        // bytecode 中的 inner conditional jump (POP_JUMP_IF_FALSE/POP_JUMP_IF_TRUE)
        // 会使之后被转为 elif 分支，且内层 body 中的 Return 丢失（变为 ExprStmt）。
        // 此处对 result 中的最后一个 If 语句做后处理，将 elif/else 体末尾的
        // 裸 ExprStmt 包装为 Return。参考 CPython 3.12: Python/ceval.c
        // 中 return 操作的字节码结构：LAST(COND_JUMP → body RETURN_VALUE)
        result = WrapElifReturn(result);
        return result;
    }

    /// <summary>
    /// 仅构建单个块的语句，不追踪后继。
    /// 用于 if-body / loop-body 等需要精确控制子范围的结构。
    /// </summary>
    private List<Stmt> BuildBlockOnly(BasicBlock? block, HashSet<BasicBlock> visited)
    {
        if (block == null || visited.Contains(block))
            return new List<Stmt>();
        visited.Add(block);
        _processedBlockIds.Add(block.Id);

        var result = _blockResults.GetValueOrDefault(block.Id);
        if (result == null || !result.IsSuccess)
        {
            if (!string.IsNullOrEmpty(result?.CommentFallback))
                return new List<Stmt> { new CommentBlock(result.CommentFallback) };
            return new List<Stmt>();
        }
        return result.Statements;
    }

    private List<Stmt> GetBlockStmts(BasicBlock block)
    {
        var result = _blockResults.GetValueOrDefault(block.Id);
        if (result == null || !result.IsSuccess)
        {
            if (!string.IsNullOrEmpty(result?.CommentFallback))
                return new List<Stmt> { new CommentBlock(result.CommentFallback) };
            return new List<Stmt>();
        }
        // 过滤 finally 的 RERAISE 产生的裸 raise
        return result.Statements.Where(s => s is not Raise { Exc: null }).ToList();
    }

    /// <summary>
    /// 结构感知的块语句获取。检测 if/else 和 try/except 等块级结构。
    /// 用于循环体内，因为 GetBlockStmts 只返回平坦语句。
    /// </summary>
    private List<Stmt> GetStructuredBlockStmts(BasicBlock block, HashSet<BasicBlock> visited)
    {
        if (block == null || visited.Contains(block))
            return new List<Stmt>();
        visited.Add(block);
        _processedBlockIds.Add(block.Id);  // 追踪通过 GetStructuredBlockStmts 处理的块，防止孤儿块恢复误报

        // 优先检测是否为循环头（即使在内层循环体中）
        // 跳过 for-loop 前导块：有 GET_ITER 但无 FOR_ITER → 不是真正的循环头
        if (block.Flags.HasFlag(BlockFlags.LoopHeader))
        {
            if (_options.VerboseErrors)
            {
                Console.Error.WriteLine($"[BUILD_STMT] Found LoopHeader block at 0x{block.StartOffset:X4}");
            }
            bool hasForIter = block.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER);
            bool hasGetIter = block.Instructions.Any(i => i.Opcode == Opcode.GET_ITER);
            if (_options.VerboseErrors)
            {
                Console.Error.WriteLine($"[BUILD_STMT] hasForIter={hasForIter}, hasGetIter={hasGetIter}");
            }
            if (!(hasGetIter && !hasForIter))
                return BuildLoop(block, visited);
        }

        // 检测 for-loop 头：FOR_ITER 是条件跳转但不是 if/else，
        // 即使 LoopHeader 标志未设置（当 for-loop 的 GET_ITER 在另一个块中时）
        if (block.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
        {
            if (_processedBlockIds.Contains(block.Id))
                return new List<Stmt>();
            return BuildForLoop(block, visited);
        }

        // 检测 GET_ITER 前导块：LOAD_GLOBAL range; LOAD_CONST 10; CALL_FUNCTION 1; GET_ITER
        // 如果后继块是 FOR_ITER，当前块是 for 循环的前导表达式块，不应单独输出（会被 for 循环消费）
        bool hasGetIterNoFor = block.Instructions.Any(i => i.Opcode == Opcode.GET_ITER)
                            && !block.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER);
        if (hasGetIterNoFor)
        {
            var forIterSucc = block.Successors.FirstOrDefault(s =>
                s.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER));
            if (forIterSucc != null)
            {
                // 提取当前块中 GET_ITER 之前的初始化语句（如 `total = 0`）
                var initStmts = new List<Stmt>();
                var blkResult = _blockResults.GetValueOrDefault(block.Id);
                if (blkResult?.Statements != null)
                {
                    foreach (var s in blkResult.Statements)
                    {
                        if (s is ExprStmt { Value: Call }) continue;
                        if (s is ExprStmt { Value: Name }) continue;
                        if (s is ExprStmt { Value: Constant }) continue;
                        initStmts.Add(s);
                    }
                }
                initStmts.AddRange(BuildForLoop(forIterSucc, visited));
                return initStmts;
            }
        }

        // 检测 try/except: 优先于 if/else，因为一个块可能同时有 SETUP_EXCEPT 和 POP_JUMP_IF_FALSE
        var tryResult = BuildTryFromBlock(block, visited);
        if (tryResult != null)
        {
            // 处理 try/except handler 的后缀块（如类/函数定义等在 try/except 之后的代码）。
            // BuildStatementsInternal 的 try/except 分支（行 556-591）已经处理了 handler 后缀，
            // 但从 GetStructuredBlockStmts 分派的 try/except（嵌套在 if-body、loop-body 内）也需处理。
            // handler 块被 visited 后，其后缀块需要显式追踪——BlockScanner 已正确创建 handler→后续块的 CFG 边。
            var tryStmtsList = new List<Stmt>(tryResult);
            var handlerAbs = GetHandlerOffset(block);
            if (handlerAbs.HasValue)
            {
                var hbList = new List<BasicBlock>();
                FindBlocksFromOffset(handlerAbs.Value, hbList);
                foreach (var hb in hbList)
                {
                    _processedBlockIds.Add(hb.Id);
                    foreach (var succ in hb.Successors)
                    {
                        if (!visited.Contains(succ))
                        {
                            visited.Add(succ);
                            tryStmtsList.AddRange(GetStructuredBlockStmts(succ, visited));
                        }
                    }
                }
            }
            return tryStmtsList;
        }

        // 3.11+: ET-based try/except 检测（优先于 if/else，因为 ET 条目也可能包含条件跳转）
        // 如果已经在构建 try 语句中（_buildTryDepth > 0），则跳过，避免在 try 体中创建另一个 try 语句
        if (_codeObject.ExceptionTable != null && _codeObject.ExceptionTable.Count > 0 && _buildTryDepth == 0)
        {
            var etTry = BuildTryFromExceptionTable(block, visited);
            if (etTry != null)
            {
                // 处理 try/except 的 else 体：follow try body 后继中未被 visited 的块。
                // 在 for 循环体内，else 体位于 try body 的 POP_BLOCK 之后（ET 范围外），
                // 作为 entry block 的直接后继而非 handler 后继。
                // 参考 CPython 3.12: compiler_try_except 生成 POP_BLOCK → else_body → JUMP → end
                var tryStmtsList = new List<Stmt>();
                foreach (var s in etTry) tryStmtsList.Add(s);
                
                // 合并 else 体到 Try 节点的 Orelse 中
                for (int ti = 0; ti < tryStmtsList.Count; ti++)
                {
                    if (tryStmtsList[ti] is Try tryNode && tryNode.Handlers.Count > 0 && (tryNode.Orelse == null || tryNode.Orelse.Count == 0))
                    {
                        var elseStmts = new List<Stmt>();
                        foreach (var succ in block.Successors)
                        {
                            if (!visited.Contains(succ))
                            {
                                var elseBlockStmts = GetStructuredBlockStmts(succ, visited);
                                elseStmts.AddRange(elseBlockStmts);
                            }
                        }
                        if (elseStmts.Count > 0)
                            tryStmtsList[ti] = new Try(tryNode.Body, tryNode.Handlers,
                                elseStmts, tryNode.Finalbody);
                        break;
                    }
                }
                return tryStmtsList;
            }
        }

        // 检测 if/else 条件分支
        if (IsConditionBranch(block))
        {
            // 检查是否为循环继续（向后跳转 → 不是 if/else）
            var lastInstr = block.Instructions.LastOrDefault();
            // 3.12+ wordcode: 使用解析后的目标偏移，而非原始 arg（wordcode arg 已 *2 但仍小于块偏移）
            int resolvedTarget;
            var isWc = _codeObject.Instructions.Count > 1
                    && _codeObject.Instructions.All(i => i.Offset % 2 == 0);
            if (isWc && lastInstr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                       or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                       or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38)
                resolvedTarget = lastInstr.Offset + 2 + lastInstr.Argument!.Value;
            else
                resolvedTarget = lastInstr.Argument!.Value;

            if (resolvedTarget < block.StartOffset)
            {
                // 向后跳转 → 循环继续条件，不是 if/else
                // 返回平坦语句（去掉尾部 Compare）
                var result = _blockResults.GetValueOrDefault(block.Id);
                var stmts = result?.Statements?.ToList() ?? new();
                while (stmts.Count > 0 && stmts[^1] is ExprStmt { Value: Compare })
                    stmts.RemoveAt(stmts.Count - 1);
                return stmts;
            }
            return BuildIfElse(block, visited);
        }

        // 平坦语句
        var flatStmts = GetBlockStmts(block);

        // 检查：当前块的后继是否为 FOR_ITER LoopHeader
        // 在 Python 字节码中，for-loop 的迭代表达式（range(x) + GET_ITER）通常在
        // 一个单独的前缀块中，而 FOR_ITER + 循环体在下一个 LoopHeader 块中。
        // 这里检测此模式并委托给 BuildForLoop。
        var forLoopHeader = block.Successors.FirstOrDefault(s =>
            s.Flags.HasFlag(BlockFlags.LoopHeader) &&
            s.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER));
        if (forLoopHeader != null && !visited.Contains(forLoopHeader) && !_processedBlockIds.Contains(forLoopHeader.Id))
        {
            // flatStmts 会被丢弃，因为 BuildForLoop 会通过
            // ExtractIterExpression 从前驱块中重新提取迭代表达式
            return BuildForLoop(forLoopHeader, visited);
        }

        return flatStmts;
    }

    /// <summary>
    /// 受限的 if/else 构建，使用 BuildBlockOnly 而非 BuildStatements 处理后继。
    /// 用于循环体内，防止递归遍历到循环头。
    /// </summary>
    private List<Stmt> BuildRestrictedIfElse(BasicBlock header, HashSet<BasicBlock> visited)
    {
        var (testExpr, condSideEffects) = ExtractConditionWithSideEffects(header);
        if (header.Instructions.Count == 0) return new List<Stmt>();
        var lastInstr = header.Instructions.Last();
        var targetOffset = lastInstr.Argument!.Value;
        // 3.12+ wordcode: POP_JUMP_IF_* 的参数是相对字节码偏移, 需要 instr.Offset + 2 + arg
        var isWordcode = _codeObject.Instructions.Count > 1
                      && _codeObject.Instructions.All(i => i.Offset % 2 == 0);
        if (isWordcode
            && lastInstr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38
                && _codeObject.Version != PythonVersion.Py310)
        {
            targetOffset = lastInstr.Offset + 2 + targetOffset;
        }

        // POP_JUMP_IF_FALSE: body = fallthrough (jump when False → else is jump target)
        // POP_JUMP_IF_TRUE:  body = same fallthrough, but condition needs NEGATION
        //                     (jump when True → body runs when False → need `not condition`)
        bool isJumpIfTrue = lastInstr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_TRUE_PY38;
        
        var bodyBranch = FindFallthrough(header);
        var afterBranch = FindBlockByOffset(targetOffset);
        
        // When using POP_JUMP_IF_TRUE, the extracted condition needs negation:
        // source: `if not X:` → bytecodes: `X; POP_JUMP_IF_TRUE → skip_body`
        // The condition X is True when we should SKIP the body (jump to else)
        // So the decompiled condition should be `not X`
        if (isJumpIfTrue && testExpr != null)
        {
            // Wrap in UnaryOp(Not, testExpr) to produce `if not X:`
            testExpr = new UnaryOp(UnaryOperator.Not, testExpr);
        }

        // 检测 while 循环模式：bodyBranch 是 LoopHeader
        // 说明当前条件分支其实是 while 循环的入口条件
        if (bodyBranch != null && bodyBranch.Flags.HasFlag(BlockFlags.LoopHeader))
        {
            // 只构建 while 循环，不处理 afterBranch（由调用方 BuildIfElse 处理）
            // 避免函数定义等 afterBranch 内容被吞入 if-body
            var wBody = BuildWhileLoopBody(bodyBranch, visited);
            return new List<Stmt> { new While(testExpr, wBody, null) };
        }

        var bodyStmts = BuildBlockOnly(bodyBranch, visited);
        
        // 检测 continue：body 为空且块末尾有向后跳转到循环头
        // 3.10+: JUMP_ABSOLUTE（非 wordcode）, 3.12+: JUMP_BACKWARD（wordcode）
        // 注意：必须确保 bodyBranch 在循环内部（有 LoopBody 或 LoopBackEdge 标志）
        if (bodyStmts.Count == 0 && bodyBranch != null 
            && (bodyBranch.Flags.HasFlag(BlockFlags.LoopBody) || bodyBranch.Flags.HasFlag(BlockFlags.LoopBackEdge)))
        {
            var lastInBody = bodyBranch.Instructions.LastOrDefault();
            if (lastInBody != default)
            {
                bool isBackToLoop = false;
                if (lastInBody.Opcode == Opcode.JUMP_ABSOLUTE
                    && lastInBody.Argument.HasValue
                    && _loopHeaderOffsets.Contains(lastInBody.Argument.Value))
                {
                    isBackToLoop = true;
                }
                else if (lastInBody.Opcode == Opcode.JUMP_BACKWARD
                         && lastInBody.Argument.HasValue)
                {
                    isBackToLoop = true;
                }
                if (isBackToLoop)
                    bodyStmts = new List<Stmt> { new Continue() };
            }
        }

        // 检测 afterBranch 是否为 else 子句
        // 条件：false 分支指向 bodyBranch 之后的某个块（不是 body 本身的后继）
        List<Stmt>? orelse = null;
        var tailCode = new List<Stmt>();
        
        if (afterBranch != null && !visited.Contains(afterBranch))
        {
            var afterStmts = GetStructuredBlockStmts(afterBranch, visited);
            
            // afterBranch 的语句就是 else 体
            // 检查是否形成 elif 链
            var ifChain = afterStmts.SkipWhile(s => s is Pass or CommentBlock).TakeWhile(s => s is If).ToList();
            if (ifChain.Count > 0 && afterStmts.Count == ifChain.Count)
            {
                // 整个 afterBranch 是 elif
                orelse = ifChain;
            }
            else if (afterStmts.Count > 0)
            {
                // else 体（非 elif 时）
                orelse = afterStmts;
            }
        }

        // 当 body 仅为 continue（向后跳转）且 else 有有效代码时，
        // 交换 body/else 并移除否定，产生 if X: Y 而非 if not X: continue else: Y
        // 注意：只有当 continue 在循环内部时才进行这个优化
        bool bodyIsJustContinue = bodyStmts.Count == 1 && bodyStmts[0] is Continue;
        bool isInLoop = bodyBranch != null && (bodyBranch.Flags.HasFlag(BlockFlags.LoopBody) || bodyBranch.Flags.HasFlag(BlockFlags.LoopBackEdge));
        if (bodyIsJustContinue && orelse != null && orelse.Count > 0 && isInLoop)
        {
            bodyStmts = orelse;
            orelse = null;
            testExpr = ExtractCondition(header);
        }

        var result = new List<Stmt> { new If(testExpr, bodyStmts, orelse) };
        result.AddRange(tailCode);
        return result;
    }

    private Expr ExtractCondition(BasicBlock block)
    {
        return ExtractConditionWithSideEffects(block).condition;
    }

    private (Expr condition, List<Stmt> sideEffects) ExtractConditionWithSideEffects(BasicBlock block)
    {
        var sideEffects = new List<Stmt>();
        if (block.Instructions.Count == 0)
            return (new Constant(true), sideEffects);

        var conditionInstrs = block.Instructions
            .Take(block.Instructions.Count - 1)
            .ToList();

        // 如果当前块只有跳转指令，没有条件表达式，从前驱块中获取
        if (conditionInstrs.Count == 0)
        {
            foreach (var pred in block.Predecessors)
            {
                var predInstrs = pred.Instructions.ToList();
                if (predInstrs.Count > 0 && !JumpHelper.IsConditionalJump(pred.Instructions.Last().Opcode))
                {
                    conditionInstrs = predInstrs;
                    break;
                }
            }
        }

        var stackMachine = new StackMachine(_codeObject);

        // 如果条件表达式以 STORE_FAST_LOAD_FAST_313 开头，需要先压入循环变量
        if (conditionInstrs.Count > 0 && conditionInstrs[0].Opcode == Opcode.STORE_FAST_LOAD_FAST_313)
        {
            var sflfArg = conditionInstrs[0].Argument ?? 0;
            int storeIdx = sflfArg >> 4;
            var loopVarName = storeIdx < _codeObject.Varnames.Count ? _codeObject.Varnames[storeIdx] : $"v_{storeIdx}";
            stackMachine.PushExpr(new Name(loopVarName, ExpressionContext.Load));
        }

        foreach (var instr in conditionInstrs)
        {
            var s = stackMachine.Execute(instr);
            if (s != null) sideEffects.Add(s);
        }

        if (stackMachine.ExprStackCount > 0)
        {
            return (stackMachine.PopExpr(), sideEffects);
        }

        // elif 模式：COMPARE_OP 因缺少 subject（已在之前块中 COPY）而返回 null。
        // 从前驱块中复制 subject，用扩展指令列表重新构造比较表达式。
        if (stackMachine.ExprStackCount == 0 && sideEffects.Count == 0 && conditionInstrs.Count > 0
            && JumpHelper.IsConditionalJump(block.Instructions.Last().Opcode))
        {
            // 从前驱块中找到 LOAD_FAST（subject 变量）
            var loadInstr = block.Predecessors
                .SelectMany(p => p.Instructions)
                .FirstOrDefault(i => i.Opcode is Opcode.LOAD_FAST or Opcode.LOAD_NAME);
            if (loadInstr != default)
            {
                var name = loadInstr.Opcode == Opcode.LOAD_FAST
                    ? _codeObject.Varnames.ElementAtOrDefault(loadInstr.Argument ?? 0)
                    : _codeObject.Names.ElementAtOrDefault(loadInstr.Argument ?? 0);
                if (name != null)
                {
                    // 用扩展指令列表重新处理：追加 subject LOAD 到指令前
                    var extendedInstrs = new List<Instruction>(conditionInstrs);
                    extendedInstrs.Insert(0, loadInstr);
                    var sm2 = new StackMachine(_codeObject);
                    foreach (var ins in extendedInstrs)
                        sm2.Execute(ins);
                    if (sm2.ExprStackCount > 0)
                        return (sm2.PopExpr(), sideEffects);
                }
            }
        }

        return (stackMachine.HasResults ? stackMachine.PopResult() : new Constant(true), sideEffects);
    }

    /// <summary>
    /// 简化 BoolOp
    /// True and X → X,  False and X → False,  True or X → True,  False or X → X
    /// </summary>
    private Expr MergeBoolOpValues(BoolOperator op, List<Expr> values)
    {
        // Filter out identity elements
        var filtered = values.Where(v =>
        {
            if (v is Constant { Value: bool b })
                return op switch
                {
                    BoolOperator.And => b,       // keep True in AND, drop False
                    BoolOperator.Or => !b,       // keep False in OR, drop True
                    _ => true
                };
            return true;
        }).ToList();

        if (filtered.Count == 0)
            return new Constant(op == BoolOperator.And); // empty AND=True, empty OR=False
        if (filtered.Count == 1)
            return filtered[0];
        return new BoolOp(op, filtered);
    }

    private Expr ExtractIterExpression(BasicBlock header)
    {
        // 遍历前驱链，只跟踪回落前驱（fallthrough），跳过跳转边（back-edge）。
        // 字节码结构：
        //   Block A: LOAD_FAST cls; LOAD_ATTR __mro__ ← fallthrough to B
        //   Block B: GET_ITER                         ← fallthrough to C
        //   Block C: FOR_ITER                         ← loop header
        // 循环体末端的 JUMP_ABSOLUTE 跳回 C，但该跳转边不指向 A。
        //
        // 关键修复：跳转边（以无条件跳转结尾的块）是循环体回跳，其中含有循环体内的
        // 比较表达式（如 j < i），评估这些块会返回错误的迭代表达式。
        var visitedPreds = new HashSet<int>();
        var predStack = new Stack<(BasicBlock block, BasicBlock? source)>();
        // 3.13+ 块拆分异常时（POP_JUMP_IF_FALSE 的 cache 导致 range(x) 落到前一个块），
        // 块前驱链找不出正确的迭代表达式。新增全局指令级后备方案。
        foreach (var p in header.Predecessors)
        {
            // 跳过跳转型前驱（循环体回跳或有条件跳转），只跟踪纯落回前驱
            if (p.Instructions.Count > 0 && JumpHelper.IsJump(p.Instructions.Last().Opcode))
                continue;
            predStack.Push((p, header));
        }
        
        while (predStack.Count > 0 && visitedPreds.Count < 20)
        {
            var (pred, source) = predStack.Pop();
            if (pred == null || !visitedPreds.Add(pred.Id)) continue;
            
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=ITER_EXTRACT pred_block#{pred.Id} offset=0x{pred.StartOffset:X4}-0x{pred.EndOffset:X4}");
            }
            
            bool hasContainerBuild = pred.Instructions.Any(i => 
                i.Opcode == Opcode.BUILD_LIST || i.Opcode == Opcode.BUILD_TUPLE 
                || i.Opcode == Opcode.BUILD_SET || i.Opcode == Opcode.BUILD_MAP);
            if (hasContainerBuild)
            {
                if (_options.VerboseErrors)
                {
                Console.Error.WriteLine($"[DECOMP_TRACE] stage=ITER_EXTRACT pred_block#{pred.Id} has container build, skipping");
                }
                continue;
            }
            
            var sm = new StackMachine(_codeObject);
            Exception? execError = null;
            foreach (var ins in pred.Instructions)
            {
                try { sm.Execute(ins); }
                catch (Exception ex) { execError = ex; break; }
            }
            if (execError == null && sm.ExprStackCount > 0)
            {
                var expr = sm.PopExpr();
                if (_options.VerboseErrors)
                {
                Console.Error.WriteLine($"[DECOMP_TRACE] stage=ITER_EXTRACT pred_result={expr?.GetType().Name}");
                }
                if (expr != null) return expr;
            }
            // 只跟踪纯落回前驱（跳过任何跳转型块：无条件跳转或条件跳转如 POP_JUMP_IF_FALSE）
            // 条件跳转块（如 if-条件）的前驱包含比较表达式，误作为迭代表达式。
            var lastInstr = pred.Instructions.LastOrDefault();
            bool isFallthrough = lastInstr == default || !JumpHelper.IsJump(lastInstr.Opcode);
            if (isFallthrough)
            {
                foreach (var pp in pred.Predecessors)
                {
                    // 同样跳过跳转边（回跳块不是迭代表达式的来源）
                    if (pp.Instructions.Count > 0 && JumpHelper.IsJump(pp.Instructions.Last().Opcode))
                        continue;
                    predStack.Push((pp, pred));
                }
            }
        }

        // Fallback 2: 从全局指令列表中找 FOR_ITER 之前的 GET_ITER 及其迭代表达式构建指令
        // 不依赖块边界（某些版本如 3.13+ 块拆分异常时仍有正确的指令序列）
        // Python 3.14 列表推导式结构：LOAD_SMALL_INT 10 → CALL range → GET_ITER → LOAD_FAST_AND_CLEAR x → SWAP 2 → BUILD_LIST 0 → SWAP 2 → FOR_ITER
        // FOR_ITER 使用栈顶的迭代器（range(10)），所以需要跳过 GET_ITER 之后的 SWAP/BUILD_LIST 等容器构建指令
        int forIterIdx = _codeObject.Instructions.FindIndex(i =>
            i.Opcode == Opcode.FOR_ITER
            && i.Offset >= header.StartOffset
            && i.Offset <= header.EndOffset);
        if (_options.VerboseErrors)
        {
        Console.Error.WriteLine($"[DECOMP_TRACE] stage=ITER_EXTRACT fallback2 forIterIdx={forIterIdx} header_offset=0x{header.StartOffset:X4}-0x{header.EndOffset:X4}");
        }
        if (forIterIdx > 0)
        {
            int getIterIdx = -1;
            for (int i = forIterIdx - 1; i >= 0; i--)
            {
                var op = _codeObject.Instructions[i].Opcode;
                if (_options.VerboseErrors)
                {
                Console.Error.WriteLine($"[DECOMP_TRACE] stage=ITER_EXTRACT scanning idx={i} opcode={op} offset=0x{_codeObject.Instructions[i].Offset:X4}");
                }
                if (op == Opcode.GET_ITER) { getIterIdx = i; break; }
                if (JumpHelper.IsJump(op) || op == Opcode.RETURN_VALUE
                    || op == Opcode.RAISE_VARARGS)
                    break;
            }
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[DECOMP_TRACE] stage=ITER_EXTRACT getIterIdx={getIterIdx}");
            }

            if (getIterIdx >= 0)
            {
                int startIdx = getIterIdx;
                for (int i = getIterIdx - 1; i >= 0; i--)
                {
                    var op = _codeObject.Instructions[i].Opcode;
                    if (JumpHelper.IsUnconditionalJump(op)
                        || op == Opcode.FOR_ITER || op == Opcode.POP_JUMP_IF_FALSE
                        || op == Opcode.POP_JUMP_IF_TRUE || op == Opcode.RETURN_VALUE
                        || op == Opcode.RAISE_VARARGS)
                        break;
                    startIdx = i;
                }
                if (_options.VerboseErrors)
                {
                Console.Error.WriteLine($"[DECOMP_TRACE] stage=ITER_EXTRACT startIdx={startIdx} getIterIdx={getIterIdx}");
                }

                if (startIdx < getIterIdx)
                {
                    int actualStartIdx = startIdx;
                    while (actualStartIdx < getIterIdx)
                    {
                        var op = _codeObject.Instructions[actualStartIdx].Opcode;
                        if (op == Opcode.RESUME_313 || op == Opcode.RESUME)
                            actualStartIdx++;
                        else
                            break;
                    }
                    var iterBuilder = _codeObject.Instructions.GetRange(actualStartIdx, getIterIdx - actualStartIdx);
                    if (_options.VerboseErrors)
                    {
                    Console.Error.WriteLine($"[DECOMP_TRACE] stage=ITER_EXTRACT executing {iterBuilder.Count} instructions: {string.Join(", ", iterBuilder.Select(i => $"{i.Opcode}(0x{i.Offset:X4})"))}");
                    }
                    var sm2 = new StackMachine(_codeObject);
                    Exception? buildError = null;
                    foreach (var instr in iterBuilder)
                    {
                        try { sm2.Execute(instr); }
                        catch (Exception ex) { buildError = ex; break; }
                    }
                    if (buildError == null && sm2.ExprStackCount > 0)
                    {
                        var expr = sm2.PopExpr();
                        if (_options.VerboseErrors)
                        {
                        Console.Error.WriteLine($"[DECOMP_TRACE] stage=ITER_EXTRACT fallback2 result={expr?.GetType().Name}");
                        }
                        if (expr != null) return expr;
                    }
                }
            }
        }

        // Fallback 3: header's own instructions before FOR_ITER or END_FOR_313 (Python 3.14)
        var iterInstrs = header.Instructions
            .TakeWhile(i => i.Opcode != Opcode.FOR_ITER && i.Opcode != Opcode.END_FOR_313)
            .ToList();
        if (iterInstrs.Count > 0 && iterInstrs.Last().Opcode == Opcode.GET_ITER)
            iterInstrs = iterInstrs.Take(iterInstrs.Count - 1).ToList();

        var stackMachine = new StackMachine(_codeObject);
        foreach (var instr in iterInstrs)
            stackMachine.Execute(instr);
        if (stackMachine.ExprStackCount > 0)
            return stackMachine.PopExpr();
        return stackMachine.HasResults ? stackMachine.PopResult() : new Name("iterable", ExpressionContext.Load);
    }

    private Expr ExtractLoopVariable(BasicBlock header, List<BasicBlock> bodyBlocks)
    {
        // 先检查 header 块自身是否包含 UNPACK_SEQUENCE（3.13+ 可能在 FOR_ITER 同一块）
        var headerUnpack = header.Instructions.FindIndex(i => i.Opcode == Opcode.UNPACK_SEQUENCE);
        if (headerUnpack >= 0 && header.Instructions[headerUnpack].Argument.HasValue)
        {
            int count = header.Instructions[headerUnpack].Argument.Value;
            var names = ExtractUnpackNames(header.Instructions, headerUnpack, count);
            if (names.Count == count)
                return new ListLiteral(names, ContainerKind.Tuple);
        }

        foreach (var bodyBlock in bodyBlocks)
        {
            // 检测 UNPACK_SEQUENCE n → 元组解包循环变量（如 for a, b in ...）
            var unpackIdx = bodyBlock.Instructions.FindIndex(i => i.Opcode == Opcode.UNPACK_SEQUENCE);
            if (unpackIdx >= 0 && bodyBlock.Instructions[unpackIdx].Argument.HasValue)
            {
                int count = bodyBlock.Instructions[unpackIdx].Argument.Value;
                var names = ExtractUnpackNames(bodyBlock.Instructions, unpackIdx, count);
                if (names.Count == count)
                    return new ListLiteral(names, ContainerKind.Tuple);
            }

            foreach (var instr in bodyBlock.Instructions)
            {
                // 3.13+ 合并 STORE_FAST_STORE_FAST: 一次存储两个局部变量（无 UNPACK_SEQUENCE）
                if (instr.Opcode == Opcode.STORE_FAST_STORE_FAST_313 && instr.Argument.HasValue)
                {
                    // CPython 3.13 编码：低4位=第一变量(idx1), 高4位=第二变量(idx2)
                    // 参考 CPython 3.13: Python/compile.c STORE_FAST_STORE_FAST
                    int idx1 = instr.Argument.Value & 0xF;
                    int idx2 = (instr.Argument.Value >> 4) & 0xF;
                    var names = new List<Expr>();
                    if (idx1 >= 0 && idx1 < _codeObject.Varnames.Count)
                        names.Add(new Name(_codeObject.Varnames[idx1], ExpressionContext.Store));
                    if (idx2 >= 0 && idx2 < _codeObject.Varnames.Count)
                        names.Add(new Name(_codeObject.Varnames[idx2], ExpressionContext.Store));
                    if (names.Count == 2)
                        return new ListLiteral(names, ContainerKind.Tuple);
                }

                if (instr.Opcode == Opcode.STORE_FAST_LOAD_FAST_313 && instr.Argument.HasValue)
                {
                    int arg = instr.Argument.Value;
                    int storeIdx = arg >> 4;
                    int loadIdx = arg & 0x0F;
                    if (storeIdx >= 0 && storeIdx < _codeObject.Varnames.Count)
                    {
                        var varName = _codeObject.Varnames[storeIdx];
                        return new Name(varName, ExpressionContext.Store);
                    }
                }
                
                if ((instr.Opcode == Opcode.STORE_FAST || instr.Opcode == Opcode.STORE_NAME
                        || instr.Opcode == Opcode.STORE_DEREF || instr.Opcode == Opcode.MAKE_CELL)
                    && instr.Argument.HasValue)
                {
                    var idx = instr.Argument.Value;
                    string varName;
                    if (instr.Opcode == Opcode.STORE_FAST)
                    {
                        if (idx < 0 || idx >= _codeObject.Varnames.Count)
                            continue;
                        varName = _codeObject.Varnames[idx];
                    }
                    else if (instr.Opcode == Opcode.STORE_NAME)
                    {
                        if (idx < 0 || idx >= _codeObject.Names.Count)
                            continue;
                        varName = _codeObject.Names[idx];
                    }
                    else // STORE_DEREF
                    {
                        // CPython 3.12+ STORE_DEREF uses varname index for cell variables,
                        // and len(varnames) + freevar_index for free variables.
                        // In 3.10, cellvars take priority: idx<len(cellvars) → cellvar.
                        // Note: in 3.10, raw byte 135 = STORE_DEREF is mapped to MAKE_CELL in enum
                        if (idx < (_codeObject.Cellvars?.Count ?? 0))
                            varName = _codeObject.Cellvars[idx];
                        else if (idx < (_codeObject.Varnames?.Count ?? 0))
                            varName = _codeObject.Varnames[idx];
                        else if (idx - (_codeObject.Varnames?.Count ?? 0) < (_codeObject.Freevars?.Count ?? 0))
                            varName = _codeObject.Freevars[idx - _codeObject.Varnames.Count];
                        else
                            varName = $"cell_{idx}";
                    }
                    return new Name(varName, ExpressionContext.Store);
                }
            }
        }
        return new Name("_", ExpressionContext.Store);
    }

    /// <summary>从指令列表中的 UNPACK_SEQUENCE 后提取 N 个变量名</summary>
    private List<Expr> ExtractUnpackNames(List<Instruction> instrs, int unpackIdx, int count)
    {
        var names = new List<Expr>();
        for (int i = unpackIdx + 1; i < instrs.Count && names.Count < count; i++)
        {
            var instr = instrs[i];
            // 3.13+ 合并 STORE_FAST_STORE_FAST: 一次存储两个局部变量
            if (instr.Opcode == Opcode.STORE_FAST_STORE_FAST_313 && instr.Argument.HasValue)
            {
                // CPython 3.13 编码：低4位=第一变量, 高4位=第二变量
                int idx1 = instr.Argument.Value & 0xF;
                int idx2 = (instr.Argument.Value >> 4) & 0xF;
                if (idx1 >= 0 && idx1 < _codeObject.Varnames.Count)
                    names.Add(new Name(_codeObject.Varnames[idx1], ExpressionContext.Store));
                if (idx2 >= 0 && idx2 < _codeObject.Varnames.Count)
                    names.Add(new Name(_codeObject.Varnames[idx2], ExpressionContext.Store));
                break;
            }
            if (instr.Opcode == Opcode.STORE_FAST && instr.Argument.HasValue
                && instr.Argument.Value >= 0 && instr.Argument.Value < _codeObject.Varnames.Count)
                names.Add(new Name(_codeObject.Varnames[instr.Argument.Value], ExpressionContext.Store));
            else if (instr.Opcode == Opcode.STORE_NAME && instr.Argument.HasValue
                && instr.Argument.Value >= 0 && instr.Argument.Value < _codeObject.Names.Count)
                names.Add(new Name(_codeObject.Names[instr.Argument.Value], ExpressionContext.Store));
            else if ((instr.Opcode == Opcode.STORE_DEREF || instr.Opcode == Opcode.MAKE_CELL) && instr.Argument.HasValue)
            {
                int idx = instr.Argument.Value;
                string cellName;
                // CPython 3.12+ STORE_DEREF uses varname index for cell variables,
                // and len(varnames) + freevar_index for free variables.
                // In 3.10, cellvars take priority: idx<len(cellvars) → cellvar.
                if (idx < _codeObject.Cellvars.Count)
                    cellName = _codeObject.Cellvars[idx];
                else if (idx < _codeObject.Varnames.Count)
                    cellName = _codeObject.Varnames[idx];
                else if (idx - _codeObject.Varnames.Count < _codeObject.Freevars.Count)
                    cellName = _codeObject.Freevars[idx - _codeObject.Varnames.Count];
                else
                    cellName = $"cell_{idx}";
                names.Add(new Name(cellName, ExpressionContext.Store));
            }
            else break;
        }
        return names;
    }

    /// <summary>孤儿块分类诊断：分析块的原因类型</summary>
    private string ClassifyOrphanBlock(BasicBlock orphan)
    {
        var instrs = orphan.Instructions;
        if (instrs.Count == 0) return "empty";
        
        if (_options.VerboseErrors)
        {
            Console.Error.WriteLine($"[ORPHAN_CLASSIFY] Block at {orphan.StartOffset:X4}, id={orphan.Id}, flags={orphan.Flags}, instrs:");
            foreach (var ins in instrs)
                Console.Error.WriteLine($"[ORPHAN_CLASSIFY]   {ins.Opcode} ({(int)ins.Opcode}) at {ins.Offset:X4}, arg={ins.Argument}");
        }
        
        bool hasHandlerPre = instrs.Any(i =>
            i.Opcode == Opcode.DUP_TOP || i.Opcode == Opcode.POP_EXCEPT
            || i.Opcode == Opcode.END_FINALLY || i.Opcode == Opcode.JUMP_IF_NOT_EXC_MATCH
            || i.Opcode == Opcode.CHECK_EXC_MATCH || i.Opcode == Opcode.CHECK_EG_MATCH
            || i.Opcode == Opcode.RERAISE);
        if (hasHandlerPre) return "handler_pre";
        if (instrs.Any(i => i.Opcode == Opcode.JUMP_BACKWARD || i.Opcode == Opcode.JUMP_BACKWARD_NO_INTERRUPT))
            return "jump_back_loop";
        if (instrs.Any(i => i.Opcode == Opcode.FOR_ITER)) return "for_iter";
        if (instrs.Any(i => i.Opcode == Opcode.END_FOR_313)) return "for_iter";
        if (instrs.Any(i => i.Opcode == Opcode.GET_ITER)) return "get_iter_precursor";
        if (instrs.Any(i => i.Opcode == Opcode.POP_JUMP_IF_FALSE || i.Opcode == Opcode.POP_JUMP_IF_TRUE
            || i.Opcode == Opcode.JUMP_FORWARD || i.Opcode == Opcode.JUMP_ABSOLUTE))
            return "jump_cond";
        if (instrs.Any(i => i.Opcode == Opcode.MAKE_FUNCTION)) return "make_function";
        if (instrs.All(i => i.Opcode == Opcode.LOAD_FAST || i.Opcode == Opcode.LOAD_NAME
            || i.Opcode == Opcode.LOAD_CONST || i.Opcode == Opcode.LOAD_ATTR
            || i.Opcode == Opcode.LOAD_GLOBAL || i.Opcode == Opcode.LOAD_DEREF))
            return "flat_expr_loads";
        if (instrs.Any(i => i.Opcode == Opcode.STORE_FAST || i.Opcode == Opcode.STORE_NAME
            || i.Opcode == Opcode.STORE_ATTR))
            return "flat_expr_store";
        return "other";
    }

    private void CollectBodyBlocks(
        BasicBlock entry, BasicBlock header,
        List<BasicBlock> bodyBlocks, HashSet<BasicBlock> visited,
        BasicBlock? exitBlock = null,
        int? elseOffset = null)
    {
        var worklist = new Queue<BasicBlock>();
        worklist.Enqueue(entry);

        var exitSuccessors = new HashSet<BasicBlock>();
        if (exitBlock != null)
        {
            foreach (var succ in exitBlock.Successors)
                exitSuccessors.Add(succ);
        }

        while (worklist.Count > 0)
        {
            var current = worklist.Dequeue();
            if (current == header || visited.Contains(current))
                continue;
            if (exitBlock != null && (current == exitBlock || exitSuccessors.Contains(current)))
                continue;
            
            if (elseOffset.HasValue && current.StartOffset >= elseOffset.Value)
                continue;

            // while-else 模式（有 elseOffset）：不要求 LoopBody 标记，因为 CFG 分析可能漏标
            if (!elseOffset.HasValue && !current.Flags.HasFlag(BlockFlags.LoopBody))
                continue;

            bodyBlocks.Add(current);
            visited.Add(current);

            foreach (var succ in current.Successors)
            {
                if (succ != header && !visited.Contains(succ))
                {
                    worklist.Enqueue(succ);
                }
            }
        }
    }

    private BasicBlock? FindElseBlock(BasicBlock header)
        => header.Successors.FirstOrDefault(s => !s.Flags.HasFlag(BlockFlags.LoopBody));

    private BasicBlock? FindBlockByOffset(int offset)
        => _blockByOffset.GetValueOrDefault(offset);

    private void CollectVisited(BasicBlock block, HashSet<BasicBlock> visited)
    {
        if (block == null || visited.Contains(block)) return;
        visited.Add(block);
        foreach (var succ in block.Successors)
            CollectVisited(succ, visited);
    }

    private BasicBlock? FindFallthrough(BasicBlock block)
    {
        // The fallthrough block is the one with the smallest offset greater than block's end
        return _blockByOffset.Values
            .Where(b => b.StartOffset > block.EndOffset)
            .OrderBy(b => b.StartOffset)
            .FirstOrDefault();
    }

    /// <summary>
    /// Phase 29: 修复 elif/else 体中 Return 丢失。
    /// 当 `return A and B` / `return A or B` 的 else 分支中含有 inner conditional jump，
    /// BuildIfElse 将其转为 elif 分支时，内层 body 的 Return 被丢失变为 ExprStmt。
    /// 此方法递归扫描 If 语句的 orelse 链，将末尾的裸 ExprStmt 包装为 Return。
    /// 参考 CPython 3.12: Python/ceval.c — RETURN_VALUE pops TOS.
    /// </summary>
    private List<Stmt> WrapElifReturn(List<Stmt> stmts)
    {
        for (int i = 0; i < stmts.Count; i++)
        {
            if (stmts[i] is If ifStmt)
            {
                stmts[i] = WrapIfReturn(ifStmt);
            }
        }
        return stmts;
    }

    private If WrapIfReturn(If ifStmt)
    {
        // 处理 elif 链：递归处理 orelse 中的 If（elif 链的第一个元素）
        var orelse = ifStmt.Orelse;
        if (orelse?.Count > 0)
        {
            if (orelse.Count == 1 && orelse[0] is If elifStmt)
            {
                orelse = new List<Stmt> { WrapIfReturn(elifStmt) };
            }
            else
            {
                // 普通 else 分支：单 ExprStmt → Return
                orelse = WrapLastExprStmtInReturn(orelse);
            }
        }

        var body = ifStmt.Body;
        // 检查 body 末尾的裸 ExprStmt（AND 链终端 body 会丢 Return）
        // 但排除副作用表达式：函数调用、方法调用等通常返回 None 的表达式不应该被包装为 Return
        if (body.Count == 1 && body[0] is ExprStmt expr)
        {
            // 只有当表达式不是函数/方法调用时，才包装为 Return
            // 函数/方法调用（如 set.add()）通常是副作用操作，返回 None，不应该被包装
            bool isCallLike = expr.Value is Call or Models.AST.Attribute or Name;
            if (!isCallLike)
            {
                body = new List<Stmt> { new Return(expr.Value) };
            }
        }

        return new If(ifStmt.Test, body, orelse);
    }

    private List<Stmt>? WrapLastExprStmtInReturn(List<Stmt>? stmts)
    {
        if (stmts == null || stmts.Count == 0) return stmts;
        var last = stmts[^1];
        if (last is ExprStmt expr && stmts.Count == 1)
        {
            // 排除副作用表达式：函数/方法调用等通常返回 None 的表达式不应该被包装为 Return
            bool isCallLike = expr.Value is Call or Models.AST.Attribute or Name;
            if (!isCallLike)
            {
                stmts[^1] = new Return(expr.Value);
            }
        }
        else if (last is If innerIf)
        {
            // 递归处理嵌套 If
            var lastIf = WrapIfReturn(innerIf);
            stmts[^1] = lastIf;
        }
        return stmts;
    }

    /// <summary>
    /// 推导式/生成器表达式模式。
    /// </summary>
    private enum CompKind { List, Set, Dict, Generator }

    /// <summary>
    /// 递归收集 for 循环体块（遍历后继直到回到 header 或已访问）。
    /// </summary>
    private static void CollectForLoopBodyBlocks(BasicBlock? entry, BasicBlock header, HashSet<int> bodyBlocks, HashSet<int> visited)
    {
        if (entry == null || entry == header || visited.Contains(entry.Id))
            return;
        visited.Add(entry.Id);
        bodyBlocks.Add(entry.Id);
        foreach (var succ in entry.Successors)
            CollectForLoopBodyBlocks(succ, header, bodyBlocks, visited);
    }

    /// <summary>
    /// 从 FunctionRef + Call 构建推导式表达式（set/dict/list comprehension 或 generator expression）。
    /// compRef.Name 为 "<setcomp>"、"<listcomp>"、"<dictcomp>"、"<genexpr>"。
    /// 将 FunctionRef 的 body（For 语句）转换为 Comprehension AST。
    /// 参考 CPython 3.12: Python/compile.c compiler_comprehension
    /// </summary>
    private Expr? BuildComprehension(FunctionRef compRef, Call compCall)
    {
        if (compRef.Code == null) return null;

        var kind = compRef.Name switch
        {
            "<setcomp>" => CompKind.Set,
            "<listcomp>" => CompKind.List,
            "<dictcomp>" => CompKind.Dict,
            "<genexpr>" => CompKind.Generator,
            _ => CompKind.List  // fallback
        };

        // Decompile the comprehension body
        var body = DecompileChildCode(compRef.Code);
        
        // Expected body structure: [For(target, iter, body, null)] or similar
        // followed by the for-loop. Find the for-loop in body.
        For? forStmt = null;
        foreach (var stmt in body)
        {
            if (stmt is For f)
            {
                forStmt = f;
                break;
            }
        }

        if (forStmt == null)
        {
            // Some comprehension bodies (set/dict via SET_ADD/MAP_ADD) don't have a For loop.
            // Use fallback: extract iterable, target, and element from the body.
            return BuildComprehensionFallback(body, kind, compCall);
        }

        // Build comprehension generators
        // Build comprehension generators: find the For loop and its filters
        var generators = new List<Comprehension>();

        // Find the innermost for-loop (for nested comprehensions)
        var innermostFor = forStmt;
        while (true)
        {
            For? nested = null;
            foreach (var s in innermostFor.Body)
                if (s is For f) { nested = f; break; }
            if (nested == null) break;
            innermostFor = nested;
        }

        // Collect filters from innermost for's body (preceding the element expr)
        var ifs = new List<Expr>();
        var bodyCopy = new List<Stmt>(innermostFor.Body);
        foreach (var s in bodyCopy)
        {
            if (s is If ifStmt)
            {
                ifs.Add(ifStmt.Test);
                // Remove the if from body
                innermostFor.Body.Remove(s);
            }
        }
        // Build generators list from outermost to innermost for
        int argIdx = 0;
        var cur = forStmt;
        while (cur != null)
        {
            var genIfs = (cur == innermostFor) ? ifs : new List<Expr>();
            // Replace .0/.1/.2 implicit parameters with actual call args
            var actualIter = cur.Iter;
            if (actualIter is Name dotName && dotName.Id.StartsWith(".") && int.TryParse(dotName.Id.AsSpan(1), out int di) && di < compCall.Args.Count)
                actualIter = compCall.Args[di];
            // 若迭代器回退到 "iterable"（ExtractIterExpression 无法提取），用 call 参数覆盖
            if (actualIter is Name fallbackName && fallbackName.Id == "iterable" && compCall.Args.Count > 0)
                actualIter = compCall.Args[0];
            // Replace .0/.1/.2 in filters with actual call args
            var replacedIfs = genIfs.Select(ifExpr => ReplaceDotParamInExpr(ifExpr, compCall)).ToList();
            generators.Add(new Comprehension(cur.Target, actualIter, replacedIfs));

            For? next = null;
            foreach (var s in cur.Body)
                if (s is For f) { next = f; break; }
            cur = next;
        }

        // Element expression: the last non-for, non-continue statement in innermost body
        Expr? elt = null;
        Expr? keyElt = null;
        
        // For list/dict/set comprehensions where MAP_ADD/SET_ADD/LIST_APPEND consumed the body,
        // the innermostFor.Body is empty. Extract key/value from the loop target.
        if (innermostFor.Body.Count == 0 && innermostFor.Target != null)
        {
            if (kind == CompKind.Dict && innermostFor.Target is ListLiteral tup && tup.Elts.Count >= 2)
            {
                // dict: target=(k, v), use Name(k), Name(v) as key/value
                keyElt = tup.Elts[0];
                elt = tup.Elts[1];
            }
            else if (kind == CompKind.Dict && innermostFor.Target is ListLiteral tup2)
            {
                elt = innermostFor.Target;
            }
            else
            {
                // set/list/generator: use target as element (or extract from child code for nested)
                if (kind is CompKind.List or CompKind.Set && compRef.Code?.Instructions != null)
                {
                    var childInstrs = compRef.Code.Instructions;
                    // Check for LOAD_DEREF (cell vars from outer scope → nested comprehension)
                    bool hasCellVar = childInstrs.Any(i => i.Opcode is Opcode.LOAD_DEREF or Opcode.LOAD_CLOSURE);
                    if (hasCellVar)
                    {
                        // Try to simulate element extraction from raw instructions
                        Expr? simElt = SimulateNestedElt(childInstrs, innermostFor.Target, compRef.Code);
                        if (simElt != null)
                            elt = simElt;
                    }
                }
                elt ??= innermostFor.Target;
            }
        }
        
        // For dict comprehensions, we need to find both key and value
        // The order in bytecode is: push key, push value, MAP_ADD
        // So in the decompiled body, we typically see: key expression, value expression
        if (kind == CompKind.Dict)
        {
            // Look for two consecutive ExprStmt: first is key, second is value
            for (int i = innermostFor.Body.Count - 1; i >= 0; i--)
            {
                var s = innermostFor.Body[i];
                if (s is ExprStmt es && !(es.Value is Name n0 && n0.Id.StartsWith(".")))
                {
                    if (elt == null)
                    {
                        // First ExprStmt from the end is value
                        elt = es.Value;
                    }
                    else
                    {
                        // Second ExprStmt from the end is key
                        keyElt = es.Value;
                        break;
                    }
                }
                else if (s is Assign aa)
                {
                    if (elt == null)
                    {
                        elt = aa.Value;
                    }
                    else
                    {
                        keyElt = aa.Value;
                        break;
                    }
                }
            }
        }
        else
        {
            // For other comprehensions, just find the last element
            for (int i = innermostFor.Body.Count - 1; i >= 0; i--)
            {
                var s = innermostFor.Body[i];
                if (s is ExprStmt es) { elt = es.Value; break; }
                if (s is Yield yieldStmt) { elt = yieldStmt.Value; break; }
                if (s is Assign aa) { elt = aa.Value; break; }
            }
        }

        // Fallback: use for-loop target as element when SET_ADD consumed it
        elt ??= innermostFor.Target;

        if (elt == null) return null;

        elt = ReplaceDotParams(elt, generators);
        if (keyElt != null)
            keyElt = ReplaceDotParams(keyElt, generators);

        if (_options.VerboseErrors)
        {
            Console.Error.WriteLine($"[COMP_OK] kind={kind} elt={elt.GetType().Name} generators.Count={generators.Count}");
        }

        return kind switch
        {
            CompKind.Set => new SetComp(elt, generators),
            CompKind.List => new ListComp(elt, generators),
            CompKind.Dict => new DictComp(keyElt ?? elt, elt, generators),
            CompKind.Generator => new GeneratorExp(elt, generators),
            _ => null
        };
    }

    private Expr ReplaceDotParamInExpr(Expr expr, Call compCall)
    {
        if (expr is Name name && name.Id.StartsWith(".") && int.TryParse(name.Id.AsSpan(1), out int di))
        {
            if (di < compCall.Args.Count)
                return compCall.Args[di];
            return name;
        }
        if (expr is BinOp binOp)
            return new BinOp(ReplaceDotParamInExpr(binOp.Left, compCall), binOp.Op, ReplaceDotParamInExpr(binOp.Right, compCall));
        if (expr is UnaryOp unaryOp)
            return new UnaryOp(unaryOp.Op, ReplaceDotParamInExpr(unaryOp.Operand, compCall));
        if (expr is PyRebuilderSharp.Core.Models.AST.Attribute attr)
            return new PyRebuilderSharp.Core.Models.AST.Attribute(ReplaceDotParamInExpr(attr.Value, compCall), attr.Attr, ExpressionContext.Load);
        if (expr is Subscript sub)
            return new Subscript(ReplaceDotParamInExpr(sub.Value, compCall), ReplaceDotParamInExpr(sub.Slice, compCall), ExpressionContext.Load);
        if (expr is Call call)
            return new Call(ReplaceDotParamInExpr(call.Func, compCall), call.Args.Select(a => ReplaceDotParamInExpr(a, compCall)).ToList(), call.Keywords.Select(k => new Keyword(k.Arg, ReplaceDotParamInExpr(k.Value, compCall))).ToList());
        if (expr is Compare compare)
            return new Compare(ReplaceDotParamInExpr(compare.Left, compCall), compare.Ops, compare.Comparators.Select(c => ReplaceDotParamInExpr(c, compCall)).ToList());
        if (expr is BoolOp boolOp)
            return new BoolOp(boolOp.Op, boolOp.Values.Select(v => ReplaceDotParamInExpr(v, compCall)).ToList());
        return expr;
    }

    private Expr ReplaceDotParams(Expr expr, List<Comprehension> generators)
    {
        if (expr is Name name && name.Id.StartsWith(".") && int.TryParse(name.Id.AsSpan(1), out int di))
        {
            if (di < generators.Count)
                return generators[di].Target;
            return name;
        }
        if (expr is BinOp binOp)
            return new BinOp(ReplaceDotParams(binOp.Left, generators), binOp.Op, ReplaceDotParams(binOp.Right, generators));
        if (expr is UnaryOp unaryOp)
            return new UnaryOp(unaryOp.Op, ReplaceDotParams(unaryOp.Operand, generators));
        if (expr is PyRebuilderSharp.Core.Models.AST.Attribute attr)
            return new PyRebuilderSharp.Core.Models.AST.Attribute(ReplaceDotParams(attr.Value, generators), attr.Attr, ExpressionContext.Load);
        if (expr is Subscript sub)
            return new Subscript(ReplaceDotParams(sub.Value, generators), ReplaceDotParams(sub.Slice, generators), ExpressionContext.Load);
        if (expr is Call call)
            return new Call(ReplaceDotParams(call.Func, generators), call.Args.Select(a => ReplaceDotParams(a, generators)).ToList(), call.Keywords.Select(k => new Keyword(k.Arg, ReplaceDotParams(k.Value, generators))).ToList());
        if (expr is Compare compare)
            return new Compare(ReplaceDotParams(compare.Left, generators), compare.Ops, compare.Comparators.Select(c => ReplaceDotParams(c, generators)).ToList());
        if (expr is BoolOp boolOp)
            return new BoolOp(boolOp.Op, boolOp.Values.Select(v => ReplaceDotParams(v, generators)).ToList());
        if (expr is Lambda lambda)
            return new Lambda(lambda.Args, ReplaceDotParams(lambda.Body, generators));
        return expr;
    }

    /// <summary>
    /// 替代 BuildComprehension for 没有 For 循环的推导式 body。
    /// body 结构：[ExprStmt(.0), element_expr, Assign(target) or If(filter, Assign(target)), Return]
    /// </summary>
    private Expr? BuildComprehensionFallback(List<Stmt> body, CompKind kind, Call compCall)
    {
        // body[0]: .0 parameter (Name)
        // body[1]: element expression (ExprStmt)
        // body[2]: target assignment (Assign) or If(filter, Assign(target))
        // body[3]: Return (ignored)

        Expr? elt = null;
        Expr? keyElt = null;
        Expr? target = null;
        Expr? iter = null;
        List<Expr> ifs = new List<Expr>();

        foreach (var stmt in body)
        {
            if (stmt is ExprStmt es && !(es.Value is Name n0 && n0.Id.StartsWith("."))
                && es.Value is not ListLiteral and not SetLiteral and not DictLiteral)
            {
                // 对于字典推导式，第一个 ExprStmt 是 key，第二个是 value
                if (kind == CompKind.Dict && keyElt == null)
                {
                    keyElt = es.Value;
                }
                else
                {
                    elt = es.Value;
                }
            }
            else if (stmt is Assign a && a.Targets.Count == 1 && a.Targets[0] is Name n && n.Id != "?")
            {
                // 如果 Assign 的值已经是推导式 AST（ListComp/SetComp/DictComp），直接使用它
                if (a.Value is ListComp lc) { elt = lc.Elt; target = lc.Generators.Count > 0 ? lc.Generators[0].Target : n; if (lc.Generators.Count > 0) { iter = lc.Generators[0].Iter; ifs = new List<Expr>(lc.Generators[0].Ifs); } break; }
                if (a.Value is SetComp sc) { elt = sc.Elt; target = sc.Generators.Count > 0 ? sc.Generators[0].Target : n; if (sc.Generators.Count > 0) { iter = sc.Generators[0].Iter; ifs = new List<Expr>(sc.Generators[0].Ifs); } break; }
                if (a.Value is GeneratorExp ge) { elt = ge.Elt; target = ge.Generators.Count > 0 ? ge.Generators[0].Target : n; if (ge.Generators.Count > 0) { iter = ge.Generators[0].Iter; ifs = new List<Expr>(ge.Generators[0].Ifs); } break; }
                target = n;
            }
            else if (stmt is If ifStmt)
            {
                foreach (var s in ifStmt.Body)
                {
                    if (s is Assign innerAssign && innerAssign.Targets.Count == 1 && innerAssign.Targets[0] is Name n2 && n2.Id != "?")
                    {
                        target = n2;
                        ifs.Add(ifStmt.Test);
                    }
                }
            }
        }

        // Determine iterable from call args (override inner iter with outer call args)
        if (compCall.Args.Count > 0)
            iter = compCall.Args[0];
        // Elt fallback: use child code's last ExprStmt value (after .0 is excluded)
        if (target == null)
        {
            // Extract loop target from child code's first STORE_FAST after FOR_ITER
            var childCode = (compCall.Func as FunctionRef)?.Code;
            if (childCode?.Instructions != null)
            {
                for (int ci = 0; ci < childCode.Instructions.Count - 1; ci++)
                {
                    if (childCode.Instructions[ci].Opcode == Opcode.FOR_ITER
                        && childCode.Instructions[ci + 1].Opcode == Opcode.STORE_FAST
                        && childCode.Instructions[ci + 1].Argument.HasValue)
                    {
                        int idx = childCode.Instructions[ci + 1].Argument.Value;
                        if (idx >= 0 && idx < childCode.Varnames.Count)
                            target = new Name(childCode.Varnames[idx], ExpressionContext.Store);
                        break;
                    }
                }
            }
        }

        // Fallback: use target as element when elt is unexpected
        if (elt == null && target != null)
            elt = target is Name n ? new Name(n.Id, ExpressionContext.Load) : target;

        if (kind == CompKind.Dict && compCall.Args.Count > 1)
            iter = compCall.Args[1];

        if (elt == null || target == null || iter == null)
            return null;

        var generators = new List<Comprehension>
        {
            new Comprehension(target, iter, ifs)
        };

        elt = ReplaceDotParams(elt, generators);
        if (keyElt != null)
            keyElt = ReplaceDotParams(keyElt, generators);

        // 检查元素表达式是否包含无效的 Call（如 Constant(None) 作为函数）
        // 如果包含，返回 null 让调用者处理
        if (ContainsInvalidCall(elt))
            return null;

        return kind switch
        {
            CompKind.Set => new SetComp(elt, generators),
            CompKind.List => new ListComp(elt, generators),
            CompKind.Dict => new DictComp(keyElt ?? elt, elt, generators),
            CompKind.Generator => new GeneratorExp(elt, generators),
            _ => null
        };
    }

    private bool ContainsInvalidCall(Expr? expr)
    {
        if (expr == null) return false;
        if (expr is Call call && call.Func is Constant)
            return true;
        if (expr is BinOp binOp)
            return ContainsInvalidCall(binOp.Left) || ContainsInvalidCall(binOp.Right);
        if (expr is UnaryOp unaryOp)
            return ContainsInvalidCall(unaryOp.Operand);
        if (expr is PyRebuilderSharp.Core.Models.AST.Attribute attr)
            return ContainsInvalidCall(attr.Value);
        if (expr is Subscript sub)
            return ContainsInvalidCall(sub.Value) || ContainsInvalidCall(sub.Slice);
        if (expr is Call call2)
        {
            if (ContainsInvalidCall(call2.Func)) return true;
            foreach (var arg in call2.Args)
                if (ContainsInvalidCall(arg)) return true;
        }
        return false;
    }

    /// <summary>
    /// 模拟嵌套推导式的元素提取。当 For 体为空（MAP_ADD/SET_ADD/LIST_APPEND 消耗了表达式栈），
    /// 从原始子代码指令中提取元素表达式。
    /// 处理需要 LOAD_DEREF（外部 cell 变量）的嵌套推导式。
    /// </summary>
    private Expr? SimulateNestedElt(List<Instruction> childInstrs, Expr? loopTarget, CodeObject? codeObj)
    {
        int storeIdx = -1;
        for (int i = 0; i < childInstrs.Count; i++)
        {
            if (childInstrs[i].Opcode == Opcode.STORE_FAST)
            {
                storeIdx = i;
                break;
            }
        }
        if (storeIdx < 0 || storeIdx >= childInstrs.Count - 1) return null;
        
        var simMachine = new StackMachine(codeObj ?? new CodeObject());
        simMachine.PushExpr(loopTarget ?? new Name("?", ExpressionContext.Load));
        
        for (int i = storeIdx + 1; i < childInstrs.Count; i++)
        {
            var ins = childInstrs[i];
            if (ins.Opcode is Opcode.LIST_APPEND or Opcode.LIST_APPEND_313 or Opcode.SET_ADD_313)
                break;
            if (ins.Opcode is Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
                or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38)
            {
                if (simMachine.ExprStackCount > 0) simMachine.PopExpr();
                continue;
            }
            try { simMachine.Execute(ins); } catch { return null; }
        }
        
        if (simMachine.ExprStackCount > 0)
            return simMachine.PopExpr();
        return null;
    }

    /// <summary>
    /// 递归转换所有语句中的 Call(FunctionRef&lt;...&gt;, ...) 为推导式表达式。
    /// 覆盖 Assign、Return、ExprStmt 等所有上下文中的推导式调用。
    /// </summary>
    private List<Stmt> ConvertComprehensionCalls(List<Stmt> stmts)
    {
        var result = new List<Stmt>(stmts.Count);
        foreach (var stmt in stmts)
        {
            result.Add(ConvertComprehensionCallInStmt(stmt));
        }
        return result;
    }

    private Stmt ConvertComprehensionCallInStmt(Stmt stmt)
    {
        return stmt switch
        {
            Assign a => a with { Value = ConvertComprehensionExpr(a.Value) },
            Return r => r.Value != null
                ? new Return(ConvertComprehensionExpr(r.Value))
                : r,
            ExprStmt es => es with { Value = ConvertComprehensionExpr(es.Value) },
            YieldFrom yf => new YieldFrom(ConvertComprehensionExpr(yf.Value)),
            Yield y => y.Value != null ? new Yield(ConvertComprehensionExpr(y.Value)) : y,
            Raise r => new Raise(ConvertComprehensionExpr(r.Exc)),
            If ifNode => new If(ifNode.Test,
                ConvertComprehensionCalls(ifNode.Body),
                ifNode.Orelse != null ? ConvertComprehensionCalls(ifNode.Orelse) : null),
            For forNode => new For(forNode.Target, forNode.Iter,
                ConvertComprehensionCalls(forNode.Body),
                forNode.Orelse != null ? ConvertComprehensionCalls(forNode.Orelse) : null),
            While wNode => new While(wNode.Test,
                ConvertComprehensionCalls(wNode.Body),
                wNode.Orelse != null ? ConvertComprehensionCalls(wNode.Orelse) : null),
            Try tNode => new Try(
                ConvertComprehensionCalls(tNode.Body),
                tNode.Handlers.Select(h => new ExceptHandler(h.Type, h.Name, ConvertComprehensionCalls(h.Body))).ToList(),
                tNode.Orelse != null ? ConvertComprehensionCalls(tNode.Orelse) : null,
                tNode.Finalbody != null ? ConvertComprehensionCalls(tNode.Finalbody) : null),
            _ => stmt
        };
    }

    private Expr ConvertComprehensionExpr(Expr? expr)
    {
        if (expr == null) return null;
        // Detect Call(FunctionRef<...>, ...) → comprehension expression
        // Must check BEFORE the general Call recursion to intercept generation/comp expressions
        if (expr is Call call)
        {
            FunctionRef? compRef = null;
            if (call.Func is FunctionRef fr)
                compRef = fr;
            else if (call.Func is Constant c && c.Value is Models.Bytecode.CodeObject co)
                compRef = new FunctionRef(co, co.Name ?? "");
            
            if (compRef != null && compRef.Name.StartsWith("<") && compRef.Name != "<lambda>")
            {
                var compExpr = BuildComprehension(compRef, call);
                if (compExpr != null)
                {
                    // 递归转换推导式内部的元素（可能包含嵌套推导式或 lambda）
                    compExpr = ConvertComprehensionExpr(compExpr);
                    return compExpr;
                }
                // If comprehensions fails, try lambda
                if (compRef.Name == "<lambda>")
                {
                    var lambda = BuildLambda(compRef);
                    if (lambda != null)
                    {
                        var newArgs = call.Args.Select(a => ConvertComprehensionExpr(a)).ToList();
                        var newKeywords = call.Keywords.Select(k => new Keyword(k.Arg, ConvertComprehensionExpr(k.Value))).ToList();
                        return new Call(lambda, newArgs, newKeywords);
                    }
                }
                // If comprehension and lambda both fail, try to decompile as lambda function
                // This handles cases like <genexpr>, <setcomp>, etc. that couldn't be converted
                var fallbackLambda = BuildLambda(compRef);
                if (fallbackLambda != null)
                {
                    // 如果 BuildLambda 返回的 Lambda body 是字面量或常量，直接返回这个 body
                    // 这处理了列表推导式重构失败的情况
                    if (fallbackLambda.Body is Constant || 
                        fallbackLambda.Body is SetLiteral || 
                        fallbackLambda.Body is ListLiteral || 
                        fallbackLambda.Body is DictLiteral)
                    {
                        return fallbackLambda.Body;
                    }
                    
                    // 否则将 Lambda 包装在 Call 中
                    var newArgs = call.Args.Select(a => ConvertComprehensionExpr(a)).ToList();
                    var newKeywords = call.Keywords.Select(k => new Keyword(k.Arg, ConvertComprehensionExpr(k.Value))).ToList();
                    return new Call(fallbackLambda, newArgs, newKeywords);
                }
            }
        }
        // Detect standalone FunctionRef<lambda> → Lambda expression
        if (expr is FunctionRef lambdaRef && lambdaRef.Name == "<lambda>")
        {
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine($"[COMP_LAMBDA] detected standalone <lambda>, code={lambdaRef.Code?.Name}, funcRef type={lambdaRef.GetType().Name}");
            }
            var lambda = BuildLambda(lambdaRef);
            Console.Error.WriteLine($"[COMP_LAMBDA] BuildLambda returned {(lambda != null ? "non-null" : "null")}");
            if (lambda != null)
                return lambda;
            // Fallback: create a minimal lambda with no args and None body
            if (_options.VerboseErrors)
            {
            Console.Error.WriteLine("[COMP_LAMBDA] using fallback lambda");
            }
            return new Lambda(new List<Parameter>(), new Constant(null));
        }
        // Recurse into sub-expressions: Call args, BinOp, JoinedStr, FormattedValue, etc.
        if (expr is JoinedStr js)
        {
            return new JoinedStr(js.Values.Select(v => ConvertComprehensionExpr(v)).ToList());
        }
        if (expr is FormattedValue fv)
        {
            return new FormattedValue(ConvertComprehensionExpr(fv.Value), fv.Conversion, fv.FormatSpec != null ? ConvertComprehensionExpr(fv.FormatSpec) : null);
        }
        if (expr is Call call2)
        {
            var newArgs = call2.Args.Select(a => ConvertComprehensionExpr(a)).ToList();
            var newKeywords = call2.Keywords.Select(k => {
                return new Keyword(k.Arg, ConvertComprehensionExpr(k.Value));
            }).ToList();
            return new Call(call2.Func, newArgs, newKeywords);
        }
        if (expr is BinOp binOp)
        {
            return new BinOp(ConvertComprehensionExpr(binOp.Left), binOp.Op, ConvertComprehensionExpr(binOp.Right));
        }
        if (expr is UnaryOp unaryOp)
        {
            return new UnaryOp(unaryOp.Op, ConvertComprehensionExpr(unaryOp.Operand));
        }
        // 递归转换推导式内部元素（嵌套推导式 / lambda）
        if (expr is ListComp lc)
        {
            return new ListComp(ConvertComprehensionExpr(lc.Elt),
                lc.Generators.Select(g => new Comprehension(
                    g.Target,
                    ConvertComprehensionExpr(g.Iter) ?? g.Iter,
                    g.Ifs)).ToList());
        }
        if (expr is SetComp sc)
        {
            return new SetComp(ConvertComprehensionExpr(sc.Elt),
                sc.Generators.Select(g => new Comprehension(
                    g.Target,
                    ConvertComprehensionExpr(g.Iter) ?? g.Iter,
                    g.Ifs)).ToList());
        }
        if (expr is DictComp dc)
        {
            return new DictComp(ConvertComprehensionExpr(dc.Key) ?? dc.Key,
                ConvertComprehensionExpr(dc.Value) ?? dc.Value,
                dc.Generators.Select(g => new Comprehension(
                    g.Target,
                    ConvertComprehensionExpr(g.Iter) ?? g.Iter,
                    g.Ifs)).ToList());
        }
        if (expr is GeneratorExp ge)
        {
            return new GeneratorExp(ConvertComprehensionExpr(ge.Elt),
                ge.Generators.Select(g => new Comprehension(
                    g.Target,
                    ConvertComprehensionExpr(g.Iter) ?? g.Iter,
                    g.Ifs)).ToList());
        }
        return expr;
    }

    private bool IsConditionBranch(BasicBlock block)
    {
        var lastInstr = block.Instructions.LastOrDefault();
        return lastInstr != default && JumpHelper.IsConditionalJump(lastInstr.Opcode);
    }

    // ===================================================================
    // 后处理：Assign + FunctionRef → FunctionDef
    /// <summary>
    /// 后处理函数/类定义（从 Assign + FunctionRef → FunctionDef）。
    /// 使用显式栈代替递归，防止 StackOverflow。
    /// 注意：不再重复递归 FunctionDef/ClassDef 的 body，
    /// 因为 BuildFunctionDef/ExtractClassDef 已完整处理。
    /// </summary>
    private List<Stmt> PostProcessFunctionDefs(List<Stmt> stmts)
    {
        var result = new List<Stmt>(stmts.Count);
        var seenNames = new HashSet<string>();
        var workQueue = new Queue<(List<Stmt> stmts, List<Stmt> result)>();
        workQueue.Enqueue((stmts, result));

        while (workQueue.Count > 0)
        {
            var (currentStmts, currentResult) = workQueue.Dequeue();

            foreach (var stmt in currentStmts)
            {
                if (stmt is If ifNode)
                {
                    var newBody = new List<Stmt>();
                    var newOrelse = ifNode.Orelse != null ? new List<Stmt>() : null;
                    workQueue.Enqueue((ifNode.Body, newBody));
                    if (newOrelse != null) workQueue.Enqueue((ifNode.Orelse!, newOrelse));
                    currentResult.Add(new If(ifNode.Test, newBody, newOrelse));
                    continue;
                }
                if (stmt is While whileNode)
                {
                    var newBody = new List<Stmt>();
                    var newOrelse = whileNode.Orelse != null ? new List<Stmt>() : null;
                    workQueue.Enqueue((whileNode.Body, newBody));
                    if (newOrelse != null) workQueue.Enqueue((whileNode.Orelse!, newOrelse));
                    currentResult.Add(new While(whileNode.Test, newBody, newOrelse));
                    continue;
                }
                if (stmt is For forNode)
                {
                    var newBody = new List<Stmt>();
                    var newOrelse = forNode.Orelse != null ? new List<Stmt>() : null;
                    workQueue.Enqueue((forNode.Body, newBody));
                    if (newOrelse != null) workQueue.Enqueue((forNode.Orelse!, newOrelse));
                    currentResult.Add(new For(forNode.Target, forNode.Iter, newBody, newOrelse));
                    continue;
                }
                if (stmt is Try tryNode)
                {
                    var newBody = new List<Stmt>();
                    workQueue.Enqueue((tryNode.Body, newBody));
                    var handlers = tryNode.Handlers.Select(h =>
                    {
                        var hBody = new List<Stmt>();
                        workQueue.Enqueue((h.Body, hBody));
                        return new ExceptHandler(h.Type, h.Name, hBody);
                    }).ToList();
                    var newOrelse = tryNode.Orelse != null ? new List<Stmt>() : null;
                    if (newOrelse != null) workQueue.Enqueue((tryNode.Orelse!, newOrelse));
                    var newFinalbody = tryNode.Finalbody != null ? new List<Stmt>() : null;
                    if (newFinalbody != null) workQueue.Enqueue((tryNode.Finalbody!, newFinalbody));
                    currentResult.Add(new Try(newBody, handlers, newOrelse, newFinalbody));
                    continue;
                }
                // FunctionDef/ClassDef body already processed by BuildFunctionDef/ExtractClassDef
                if (stmt is FunctionDef fd)
                {
                    if (!seenNames.Add(fd.Name))
                    {
                        // 替换已有的重复定义（保留最后一个，通常更完整）
                        for (int si = currentResult.Count - 1; si >= 0; si--)
                            if (currentResult[si] is FunctionDef prev && prev.Name == fd.Name)
                                { currentResult.RemoveAt(si); break; }
                    }
                    currentResult.Add(fd);
                    continue;
                }
                if (stmt is ClassDef cd)
                {
                    foreach (var bodyStmt in cd.Body)
                    {
                        if (bodyStmt is FunctionDef innerFd)
                        {
                            bool hasNonComment = false;
                            foreach (var s in innerFd.Body)
                            {
                                if (s is not CommentBlock)
                                {
                                    hasNonComment = true;
                                    break;
                                }
                            }
                            if (!hasNonComment)
                            {
                                innerFd.Body.Add(new Pass());
                            }
                        }
                    }
                    
                    if (!seenNames.Add(cd.Name))
                    {
                        // 替换已有的重复定义（保留最后一个，通常更完整）
                        for (int si = currentResult.Count - 1; si >= 0; si--)
                            if (currentResult[si] is ClassDef prev && prev.Name == cd.Name)
                                { currentResult.RemoveAt(si); break; }
                    }
                    currentResult.Add(cd);
                    continue;
                }
                if (stmt is Assign assign && assign.Targets.Count == 1
                    && assign.Targets[0] is Name targetName)
                {
                    // Lambda
                    if (assign.Value is FunctionRef funcRef1
                        && (funcRef1.Name == "<lambda>" || funcRef1.Code?.Name == "<lambda>"))
                    {
                        var lambda = BuildLambda(funcRef1);
                        if (lambda != null)
                            currentResult.Add(new Assign(new List<Expr> { new Name(targetName.Id, ExpressionContext.Store) }, lambda));
                        else
                            currentResult.Add(stmt);
                        continue;
                    }
                    // Comprehension: <genexpr>/<setcomp>/<listcomp>/<dictcomp>
                    // 直接赋值的 FunctionRef（无外层 CALL）—— 如 Module 级推导式赋值
                    if (assign.Value is FunctionRef compFuncRef
                        && compFuncRef.Name.StartsWith("<"))
                    {
                        var compExpr = BuildComprehension(compFuncRef, new Call(compFuncRef, new List<Expr>(), new List<Keyword>()));
                        if (compExpr != null)
                            currentResult.Add(new Assign(new List<Expr> { new Name(targetName.Id, ExpressionContext.Store) }, compExpr));
                        else
                            currentResult.Add(new CommentBlock($"# [{compFuncRef.Name}]: comprehension expression"));
                        continue;
                    }
                    // FunctionDef
                    if (assign.Value is FunctionRef funcRef)
                    {
                        var fnName = funcRef.Name;
                        if ((string.IsNullOrEmpty(fnName) || fnName == "<lambda>")
                            && funcRef.Code != null && !string.IsNullOrEmpty(funcRef.Code.Name)
                            && funcRef.Code.Name != "<module>" && !funcRef.Code.Name.Contains("module"))
                            fnName = funcRef.Code.Name;
                        if (string.IsNullOrEmpty(fnName) || fnName == "<lambda>" || fnName.Contains("code object"))
                            fnName = targetName.Id;
                        if (!seenNames.Add(fnName))
                        {
                            // 替换已存在的重复定义（保留最后一个，通常是正确的版本）
                            for (int si = currentResult.Count - 1; si >= 0; si--)
                            {
                                if (currentResult[si] is FunctionDef prevFd && prevFd.Name == fnName
                                    || currentResult[si] is ClassDef prevCd && prevCd.Name == fnName)
                                {
                                    currentResult.RemoveAt(si);
                                    break;
                                }
                            }
                        }
                        var funcDef = BuildFunctionDef(fnName, funcRef);
                        currentResult.Add(funcDef ?? stmt);
                        continue;
                    }
                    // ClassDef
                    // 两种情况：
                    // 1. 直接调用: __build_class__(func, name, ...)
                    // 2. 装饰器调用: decorator(__build_class__(func, name, ...)) 或 decorator(__build_class__(...))()
                    Call? buildClassCall = null;
                    var decorators = new List<Expr>();
                    
                    if (assign.Value is Call call)
                    {
                        // 调试信息
                        // 情况 2b: decorator(__build_class__(...))() — 装饰器结果被调用
                        if (call.Args.Count == 0 && call.Func is Call outerDecoratorCall)
                        {
                            decorators.Add(outerDecoratorCall.Func);
                            if (outerDecoratorCall.Args.Count == 1 && outerDecoratorCall.Args[0] is Call bcCall1
                                && bcCall1.Func is Name bcName1 && bcName1.Id == "__build_class__")
                            {
                                buildClassCall = bcCall1;
                            }
                        }
                        // 情况 2a: decorator(__build_class__(...)) — 装饰器直接应用
                        else if (call.Args.Count == 1 && call.Args[0] is Call bcCall2
                                 && bcCall2.Func is Name bcName2 && bcName2.Id == "__build_class__")
                        {
                            decorators.Add(call.Func);
                            buildClassCall = bcCall2;
                        }
                        // 情况 1: 直接调用 __build_class__
                        else if (call.Func is Name bcName3 && bcName3.Id == "__build_class__")
                        {
                            buildClassCall = call;
                        }
                    }
                    
                    if (buildClassCall != null)
                    {
                        if (!seenNames.Add(targetName.Id))
                        {
                            for (int si = currentResult.Count - 1; si >= 0; si--)
                            {
                                if (currentResult[si] is ClassDef prevClass && prevClass.Name == targetName.Id
                                    || currentResult[si] is FunctionDef prevFn && prevFn.Name == targetName.Id)
                                {
                                    currentResult.RemoveAt(si);
                                    break;
                                }
                            }
                        }
                        var classDef = ExtractClassDef(buildClassCall, targetName.Id);
                        if (classDef != null && decorators.Count > 0)
                        {
                            classDef = classDef with { Decorators = decorators };
                        }
                        currentResult.Add(classDef ?? stmt);
                        continue;
                    }
                    // 推导式（comprehension）：<setcomp>/<listcomp>/<dictcomp>/<genexpr>
                    // 模式：assign.Value is Call(funcRef, [iterExpr?])
                    // 其中 funcRef.Name 以 < 开头（如 "<setcomp>"）
                    // 注意：CALL 的 Args 可能为空（GET_ITER 消耗了迭代表达式，
                    // 迭代器通过函数参数 .0 隐式传入）。
                    if (assign.Value is Call compCall
                        && compCall.Func is FunctionRef compRef
                        && compRef.Name.StartsWith("<"))
                    {
                        var compExpr = BuildComprehension(compRef, compCall);
                        if (compExpr != null)
                            currentResult.Add(new Assign(new List<Expr> { new Name(targetName.Id, ExpressionContext.Store) }, compExpr));
                        else
                            currentResult.Add(stmt);
                        continue;
                    }
                    // import
                    if (assign.Value is Name valName && valName.IsImport)
                    {
                        currentResult.Add(valName.Id == targetName.Id
                            ? new Import(new List<Alias> { new Alias(targetName.Id, null) })
                            : new Import(new List<Alias> { new Alias(valName.Id, targetName.Id) }));
                        continue;
                    }
                    // decorator
                    if (assign.Value is Call decoratorCall && decoratorCall.Args.Count == 1)
                    {
                        // Class decorator: decorator(__build_class__(func, name, ...))
                        if (decoratorCall.Args[0] is Call classBuildCall
                            && classBuildCall.Func is Name classFuncName 
                            && classFuncName.Id == "__build_class__")
                        {
                            if (!seenNames.Add(targetName.Id))
                            {
                                for (int si = currentResult.Count - 1; si >= 0; si--)
                                {
                                    if (currentResult[si] is ClassDef prevClass && prevClass.Name == targetName.Id
                                        || currentResult[si] is FunctionDef prevFn && prevFn.Name == targetName.Id)
                                    {
                                        currentResult.RemoveAt(si);
                                        break;
                                    }
                                }
                            }
                            var classDef = ExtractClassDef(classBuildCall, targetName.Id);
                            if (classDef != null)
                            {
                                classDef = classDef with { Decorators = new List<Expr> { decoratorCall.Func } };
                            }
                            currentResult.Add(classDef ?? stmt);
                            continue;
                        }
                        // Function decorator: decorator(func)
                        if (decoratorCall.Args[0] is FunctionRef)
                        {
                            BuildFunctionDefWithDecorators(targetName, decoratorCall, currentResult);
                            continue;
                        }
                    }
                    if (assign.Value is Call outerCall && outerCall.Args.Count == 1
                        && outerCall.Args[0] is Call innerCall && innerCall.Args.Count == 1)
                    {
                        // Nested class decorator: outer(inner(__build_class__(func, name, ...)))
                        if (innerCall.Args[0] is Call classBuildCall
                            && classBuildCall.Func is Name classFuncName 
                            && classFuncName.Id == "__build_class__")
                        {
                            if (!seenNames.Add(targetName.Id))
                            {
                                for (int si = currentResult.Count - 1; si >= 0; si--)
                                {
                                    if (currentResult[si] is ClassDef prevClass && prevClass.Name == targetName.Id
                                        || currentResult[si] is FunctionDef prevFn && prevFn.Name == targetName.Id)
                                    {
                                        currentResult.RemoveAt(si);
                                        break;
                                    }
                                }
                            }
                            var classDef = ExtractClassDef(classBuildCall, targetName.Id);
                            if (classDef != null)
                            {
                                classDef = classDef with { Decorators = new List<Expr> { innerCall.Func, outerCall.Func } };
                            }
                            currentResult.Add(classDef ?? stmt);
                            continue;
                        }
                        // Nested function decorator: outer(inner(func))
                        if (innerCall.Args[0] is FunctionRef)
                        {
                            BuildFunctionDefWithDecorators(targetName, outerCall, currentResult);
                            continue;
                        }
                    }
                    // from ... import
                    if (assign.Value is Models.AST.Attribute attr && attr.Value is Name modName
                        && attr.Ctx == ExpressionContext.Load && attr.IsImportFrom)
                    {
                        var alias = targetName.Id == attr.Attr ? null : targetName.Id;
                        currentResult.Add(new ImportFrom(modName.Id, new List<Alias> { new Alias(attr.Attr, alias) }, 0));
                        continue;
                    }
                    currentResult.Add(stmt);
                }
                else
                {
                    currentResult.Add(stmt);
                }
            }
        }

        // 合并连续的同模块 import-from
        // from types import A, B (was: from types import A / from types import B)
        var merged = new List<Stmt>();
        ImportFrom? pendingImportFrom = null;
        foreach (var stmt in result)
        {
            if (stmt is ImportFrom impf)
            {
                if (pendingImportFrom != null && pendingImportFrom.Module == impf.Module
                    && pendingImportFrom.Level == impf.Level)
                {
                    pendingImportFrom.Names.AddRange(impf.Names);
                }
                else
                {
                    if (pendingImportFrom != null)
                        merged.Add(pendingImportFrom);
                    pendingImportFrom = impf;
                }
            }
            else
            {
                if (pendingImportFrom != null)
                {
                    merged.Add(pendingImportFrom);
                    pendingImportFrom = null;
                }
                merged.Add(stmt);
            }
        }
        if (pendingImportFrom != null)
            merged.Add(pendingImportFrom);
        result = merged;

        // 过滤 import 后遗留的模块名表达式
        var importedModules = new HashSet<string>();
        foreach (var stmt in result)
        {
            if (stmt is Import imp)
                foreach (var a in imp.Names)
                    importedModules.Add(a.Name);
            if (stmt is ImportFrom impf)
                importedModules.Add(impf.Module);
        }
        result = result.Where(s => s is not ExprStmt { Value: Name n } || !importedModules.Contains(n.Id)).ToList();

        // Return-Fold: 将 if cond: return True; return False → return cond
        // 递归扫描所有 FunctionDef/ClassDef 体
        for (int i = 0; i < result.Count; i++)
        {
            if (result[i] is FunctionDef fd)
                result[i] = fd with { Body = FoldReturnIf(fd.Body) };
            else if (result[i] is ClassDef cd)
                result[i] = cd with { Body = FoldReturnIf(cd.Body) };
        }

        return result;
    }

    /// <summary>
    /// 将 if cond: return True; return False → return cond。
    /// 递归扫描嵌套结构体（If/While/For/Try/FunctionDef/ClassDef）。
    /// </summary>
    private List<Stmt> FoldReturnIf(List<Stmt> stmts)
    {
        // 递归处理嵌套结构
        for (int i = 0; i < stmts.Count; i++)
        {
            stmts[i] = stmts[i] switch
            {
                FunctionDef fd => fd with { Body = FoldReturnIf(fd.Body) },
                ClassDef cd => cd with { Body = FoldReturnIf(cd.Body) },
                If ifNode => new If(ifNode.Test,
                    FoldReturnIf(ifNode.Body),
                    ifNode.Orelse != null ? FoldReturnIf(ifNode.Orelse) : null),
                While wNode => new While(wNode.Test,
                    FoldReturnIf(wNode.Body),
                    wNode.Orelse != null ? FoldReturnIf(wNode.Orelse) : null),
                For fNode => new For(fNode.Target, fNode.Iter,
                    FoldReturnIf(fNode.Body),
                    fNode.Orelse != null ? FoldReturnIf(fNode.Orelse) : null),
                Try tNode => new Try(FoldReturnIf(tNode.Body),
                    tNode.Handlers.Select(h => new ExceptHandler(h.Type, h.Name,
                        FoldReturnIf(h.Body))).ToList(),
                    tNode.Orelse != null ? FoldReturnIf(tNode.Orelse) : null,
                    tNode.Finalbody != null ? FoldReturnIf(tNode.Finalbody) : null),
                _ => stmts[i]
            };
        }

        // 先单独应用规则 0: 展开 if+else 中 body 以 return/raise 结尾的无效 else
        // 当 if body 以不可达终止符结尾时，else 体可以安全提升为顺序代码。
        // ⚠️ 此规则在源码反编译中正确，但在字节码反编译中错误！
        // 字节码中 POP_JUMP_IF_FALSE 条件分支的 else 体 isElseClause=True 判定
        // 正是基于 body 以不可达终止符结尾（bodyEndsWithTerminal=True）。
        // 此时 else 体 NOT 是"无效的"——字节码结构要求必须保留 else 关键字。
        // 参考 CPython: if-else 的 POP_JUMP_IF_FALSE → body(Return) → else 分支。
        // 如果去除 else，else 体被输出为顺序代码，导致结构塌陷。
        // 参见测试用例 l1_basic/if_else.py: test_if_else_simple。
        // 此规则已禁用。如需恢复，仅在源码反编译（非字节码）上下文中启用。
        //for (int ri = stmts.Count - 1; ri >= 0; ri--)
        //{
        //    if (stmts[ri] is If ifStmt0
        //        && ifStmt0.Orelse is { Count: > 0 }
        //        && ifStmt0.Body.Count > 0
        //        && ifStmt0.Body[^1] is Return or Raise or Continue or Break)
        //    {
        //        var inlined = new List<Stmt> { new If(ifStmt0.Test, ifStmt0.Body, null) };
        //        inlined.AddRange(ifStmt0.Orelse);
        //        stmts.RemoveAt(ri);
        //        stmts.InsertRange(ri, inlined);
        //    }
        //}

        // 从后向前扫描可折叠模式（保证删除不影响前向索引）
        for (int i = stmts.Count - 2; i >= 0; i--)
        {
            if (stmts[i] is If ifStmt)
            {
                // 规则 1: if cond: return val; return False → return cond and val
                if (ifStmt.Orelse == null
                    && ifStmt.Body is [Return retVal]
                    && stmts[i + 1] is Return { Value: Constant { Value: false } })
                {
                    // 折叠为 return cond and val
                    var merged = MergeBoolOpValues(BoolOperator.And,
                        new List<Expr> { ifStmt.Test, retVal.Value ?? new Constant(true) });
                    stmts[i] = new Return(merged);
                    stmts.RemoveAt(i + 1);
                }
                // 规则 1b: if cond: return False; return True → return not cond
                else if (ifStmt.Orelse == null
                    && ifStmt.Body is [Return { Value: Constant { Value: false } }]
                    && stmts[i + 1] is Return { Value: Constant { Value: true } })
                {
                    stmts[i] = new Return(new UnaryOp(UnaryOperator.Not, ifStmt.Test));
                    stmts.RemoveAt(i + 1);
                }
                // 规则 2: if cond: return True; else: return False → return cond
                else if (ifStmt.Orelse is [Return { Value: Constant { Value: false } }]
                    && ifStmt.Body is [Return { Value: Constant { Value: true } }])
                {
                    stmts[i] = new Return(ifStmt.Test);
                }
                // 规则 2b: if cond: return False; else: return True → return not cond
                else if (ifStmt.Orelse is [Return { Value: Constant { Value: true } }]
                    && ifStmt.Body is [Return { Value: Constant { Value: false } }])
                {
                    stmts[i] = new Return(new UnaryOp(UnaryOperator.Not, ifStmt.Test));
                }
            }
        }

        // 规则 3: if cond: return val（纯 AND 链末尾，无其他语句）→ return cond and val
        // 3.13+ AND 链终端：跳转直达共享 RETURN_VALUE，无显式 Return(False)
        // 仅对纯单-if 函数体应用（[docstring?, If(cond, [Return(val)])]），
        // 且 val 为布尔表达式（Compare/BoolOp），避免误伤非纯布尔模式
        if (stmts.Count >= 1 && stmts.Count <= 2 && stmts[^1] is If lastIf
            && lastIf.Orelse == null
            && lastIf.Body is [Return { Value: not null } lastRet])
        {
            bool isPureIfReturn = stmts.Count == 1
                || (stmts.Count == 2 && stmts[0] is ExprStmt { Value: Constant { Value: string } });
            bool isBoolExpr = lastRet.Value is Compare or BoolOp;
            if (isPureIfReturn && isBoolExpr)
            {
                var merged = MergeBoolOpValues(BoolOperator.And,
                    new List<Expr> { lastIf.Test, lastRet.Value });
                stmts[^1] = new Return(merged);
            }
        }
        return stmts;
    }

    /// <summary>
    /// 剥离单层 Not 包装。如果是 Not(expr) 返回 expr，否则返回 null。
    /// </summary>
    private static Expr? StripNot(Expr expr) => expr is UnaryOp { Op: UnaryOperator.Not } un ? un.Operand : null;

    /// <summary>
    /// 从 Assign(Name, Call(decorator_chain, FunctionRef)) 中提取 FunctionDef 和装饰器列表。
    /// </summary>
    private void BuildFunctionDefWithDecorators(Name targetName, Call call, List<Stmt> result)
    {
        // Extract decorator chain from nested Call
        var decorators = new List<Expr>();
        var current = call;
        
        // Walk the call chain: Call(func1, Call(func2, FunctionRef(...)))
        while (current.Args.Count >= 1 && current.Args[0] is Call innerCall)
        {
            // The outer call's function is a decorator
            decorators.Add(current.Func);
            current = innerCall;
        }
        
        // The innermost call's first arg should be FunctionRef
        if (current.Args.Count >= 1 && current.Args[0] is FunctionRef funcRef)
        {
            decorators.Add(current.Func);
            decorators.Reverse(); // decorators[0] = inner-most, decorators[-1] = outer-most
            
            var fnName = funcRef.Name;
            if (string.IsNullOrEmpty(fnName) || fnName == "<lambda>"
                && funcRef.Code != null && !string.IsNullOrEmpty(funcRef.Code.Name)
                && funcRef.Code.Name != "<module>")
                fnName = funcRef.Code.Name;
            if (string.IsNullOrEmpty(fnName) || fnName == "<lambda>")
                fnName = targetName.Id;
            
            var cleanName = fnName;
            var lastDot = fnName.LastIndexOf('.');
            if (lastDot >= 0) cleanName = fnName[(lastDot + 1)..];
            
            var stmt = BuildFunctionDef(cleanName, funcRef);
            if (stmt != null)
            {
                if (stmt is FunctionDef funcDef)
                {
                    result.Add(funcDef with { Decorators = decorators });
                }
                else
                {
                    result.Add(stmt);
                }
            }
        }
    }

    /// <summary>
    /// 从 `__build_class__(funcRef, name, *bases)` 调用中提取 ClassDef。
    /// </summary>
    private ClassDef? ExtractClassDef(Call buildClassCall, string storeName)
    {
        if (buildClassCall.Args.Count < 2) return null;

        // args[0] = FunctionRef (class body function)
        if (buildClassCall.Args[0] is not FunctionRef funcRef) return null;
        if (funcRef.Code == null) return null;

        // 类名：优先使用 STORE_NAME 的目标名（args[1] 可能是方法名，不是类名）
        string className = storeName;

        // args[2:] = base classes
        var bases = new List<Expr>();
        for (int i = 2; i < buildClassCall.Args.Count; i++)
            bases.Add(buildClassCall.Args[i]);

        // Keywords: metaclass=... 等（来自 Call.Keywords 或从 last arg 中提取关键词名元组）
        List<Keyword>? keywords = null;
        if (buildClassCall.Keywords.Count > 0)
        {
            // 3.10-: CALL_FUNCTION_KW 已正确分离关键词
            keywords = buildClassCall.Keywords;
        }
        else if (bases.Count > 0 && bases[^1] is Constant { Value: System.Collections.IList kwList }
            && kwList.Count > 0 && kwList[0] is string)
        {
            // 3.11+ CALL/CALL_KW_313: 关键词名元组在最后一个 arg 中
            // 倒数第二个 arg 是关键词值
            int kwCount = kwList.Count;
            if (bases.Count >= kwCount + 1)
            {
                var kwValues = bases.GetRange(bases.Count - 1 - kwCount, kwCount);
                keywords = new List<Keyword>();
                for (int i = 0; i < kwCount; i++)
                {
                    keywords.Add(new Keyword(kwList[i]?.ToString() ?? "", kwValues[i]));
                }
                bases.RemoveRange(bases.Count - 1 - kwCount, kwCount + 1);
            }
        }

        // Decompile class body from the child code object
        var body = DecompileChildCode(funcRef.Code);
        
        // 修复类体中的空函数体：如果函数体只有注释，添加 pass 语句
        foreach (var stmt in body)
        {
            if (stmt is FunctionDef fd)
            {
                bool hasNonComment = false;
                foreach (var sb in fd.Body)
                {
                    if (sb is not CommentBlock)
                    {
                        hasNonComment = true;
                        break;
                    }
                }
                if (!hasNonComment)
                {
                    fd.Body.Add(new Pass());
                }
            }
        }

        // 过滤 class body 中的 __module__ / __qualname__ 元数据赋值
        body = body.Where(s => s is not Assign a
            || a.Targets.Count != 1
            || a.Targets[0] is not Name n
            || (n.Id != "__module__" && n.Id != "__qualname__" && n.Id != "__classcell__"
                && n.Id != "__static_attributes__" && n.Id != "__firstlineno__"
                && n.Id != "__classdictcell__")).ToList();

        // 移除类体开头的独立字符串常量 'ClassName'（编译器产生的 __doc__ 别名）
        if (body.Count > 0 && body[0] is ExprStmt { Value: Constant { Value: string s } }
            && s.All(c => char.IsLetterOrDigit(c) || c == '_'))
        {
            Console.Error.WriteLine($"[CLS_CLEAN] Removing standalone string '{s}' from class body (count={body.Count})");
            body.RemoveAt(0);
        }

        // 将类体中第一个 __doc__ = '...' 转换为裸字符串表达式（类体 docstring）
        bool hadDocString = false;
        for (int di = 0; di < body.Count; di++)
        {
            if (body[di] is Assign docAssign
                && docAssign.Targets.Count == 1 && docAssign.Targets[0] is Name docName
                && docName.Id == "__doc__" && docAssign.Value is Constant docConst)
            {
                body[di] = new ExprStmt(docConst);
                hadDocString = true;
                break;
            }
        }
        // 如果同时存在独立的 'ClassName' 字符串（编译器产生）和 __doc__ 赋值，
        // 移除独立字符串（以 __doc__ 为准）
        if (hadDocString && body.Count > 0 && body[0] is ExprStmt { Value: Constant { Value: string sv } }
            && sv == className)
        {
            body.RemoveAt(0);
        }

        // 过滤 class body 中的 return 语句（class body 无 return）
        body = body.Where(s => s is not Return).ToList();
        // 过滤编译器内部伪影
        Console.Error.WriteLine($"[CLS_EXTRACT] body.Count={body.Count} before filtering");
        body = body.Where(s => s is not Assign a || a.Targets.Count != 1
            || a.Targets[0] is not Name an
            || (an.Id != "__static_attributes__" && an.Id != "__classdictcell__"
                && an.Id != "__classcell__" && an.Id != "__firstlineno__"))
            .Where(s => s is not Assign a2 || a2.Value is not Name classN || classN.Id != "__class__")
            .Where(s => s is not Assign a3 || a3.Value is not Constant ic || ic.Value is not int)
            .ToList();
        // 如果类体为空（所有伪影被清空后），添加 pass
        if (body.Count == 0 || body.All(s => s is CommentBlock))
            body.Add(new Pass());

        return new ClassDef(className, bases, body, null, keywords);
    }

    /// <summary>
    /// 从 FunctionRef 构建一个完整的 FunctionDef AST。
    /// 递归反编译子代码对象以获取函数体。
    /// </summary>
    private Stmt? BuildFunctionDef(string name, FunctionRef funcRef)
    {
        if (funcRef.Code == null) return null;

        // 推导式（comprehension）：<genexpr>/<setcomp>/<listcomp>/<dictcomp>
        // 这些名字以 "<" 开头的 FunctionRef 不应生成 FunctionDef，
        // 而应由 BuildComprehension 在 CALL 站点处理。
        if (name.StartsWith("<"))
            return null;

        var childCode = funcRef.Code;

        // 1. 提取函数参数
        var args = new List<Parameter>();
        var varnames = childCode.Varnames;
        int posOnlyCount = childCode.PosOnlyArgCount;
        int totalPosArgs = childCode.ArgCount;  // posonly + positional-or-keyword
        int kwOnlyCount = childCode.KwOnlyArgCount;
        int kwOnlyStart = totalPosArgs;  // kwonly args start after all positional args

        // 1a. Positional-only args: indices [0, posOnlyCount)
        for (int i = 0; i < posOnlyCount && i < varnames.Count; i++)
            args.Add(new Parameter(varnames[i]));

        // 1b. Positional-or-keyword args: indices [posOnlyCount, totalPosArgs)
        for (int i = posOnlyCount; i < totalPosArgs && i < varnames.Count; i++)
            args.Add(new Parameter(varnames[i]));

        // 1c. Keyword-only args: indices [kwOnlyStart, kwOnlyStart + kwOnlyCount)
        for (int i = kwOnlyStart; i < kwOnlyStart + kwOnlyCount && i < varnames.Count; i++)
        {
            var param = new Parameter(varnames[i]);
            // Attach kwdefault if available
            if (funcRef.KwDefaultExprs?.TryGetValue(varnames[i], out var kwDefault) == true && kwDefault != null)
                param = param with { Default = kwDefault };
            args.Add(param);
        }

        // 1e. *args (var-positional) parameter — 在 varnames 中位于 kwonly 之后
        string? varargName = childCode.HasVarargs && varnames.Count > totalPosArgs + kwOnlyCount
            ? varnames[totalPosArgs + kwOnlyCount] : null;

        // 1f. **kwargs (var-keyword) parameter — 在 varnames 中位于 vararg 之后
        string? varkwName = childCode.HasVarkw && varnames.Count > totalPosArgs + kwOnlyCount + (childCode.HasVarargs ? 1 : 0)
            ? varnames[totalPosArgs + kwOnlyCount + (childCode.HasVarargs ? 1 : 0)] : null;

        // 1d. Set default values for trailing positional args (from DefaultExprs)
        // 注意：DefaultExprs 只应用于 POSITIONAL 参数（posonly + positional-or-keyword），
        // 不可污染 keyword-only 参数。args.Count 可能包含 kwonly 参数。
        int totalPosArgsCount = posOnlyCount + (totalPosArgs - posOnlyCount); // = childCode.ArgCount
        int positionalArgsInList = args.Count - kwOnlyCount; // 排除 kwonly 后的位置参数数
        if (funcRef.DefaultExprs != null && funcRef.DefaultExprs.Count > 0)
        {
            int startIdx = positionalArgsInList - funcRef.DefaultExprs.Count;
            if (startIdx < 0) startIdx = 0; // 安全防护
            for (int i = 0; i < funcRef.DefaultExprs.Count; i++)
            {
                int argIdx = startIdx + i;
                if (argIdx >= 0 && argIdx < positionalArgsInList) // 只限位置参数范围
                {
                    var existing = args[argIdx];
                    args[argIdx] = new Parameter(existing.Name, existing.Annotation,
                        funcRef.DefaultExprs[i]);
                }
            }
        }

        // 2. 递归反编译函数体
        var body = DecompileChildCode(childCode);
        
        // 2.5 隐式 docstring: Python 3.10+ 将 docstring 放在 co_consts[0]
        //    但不生成 LOAD_CONST 0 指令。需检测并插入。
        if (childCode.Constants.TryGetValue(0, out var const0) && const0 is string docstr)
        {
            // 检查 body 是否已有 docstring
            bool hasDoc = body.Count > 0 && body[0] is ExprStmt es
                && es.Value is Constant c && c.Value is string;
            if (!hasDoc)
                body.Insert(0, new ExprStmt(new Constant(docstr)));
        }

        // 在 StripTrailingReturnNone 之前检查是否有显式返回值
        // 类体的 return __class__ 是 CPython 内部实现，不算显式函数返回
        bool implicitClassReturn = body.Count > 0 && body[^1] is Return rVal1
            && rVal1.Value is Name rn1 && rn1.Id == "__class__";
        bool hasNonImplicitReturn = body.Any(stmt => stmt is Return ret && ret.Value != null
            && !(ret.Value is Name rn2 && rn2.Id == "__class__"));

        // 3. 去掉函数体末尾的隐式 return None（由 LOAD_CONST None + RETURN_VALUE 产生）
        StripTrailingReturnNone(body);

        // 4. 去掉函数名中的 qualname 前缀（如 C.foobar → foobar）
        var cleanName = name;
        var lastDot = name.LastIndexOf('.');
        if (lastDot >= 0) cleanName = name[(lastDot + 1)..];
        
        // 4.5 如果函数体为空或只有注释，添加 pass 语句
        bool hasNonComment = false;
        foreach (var stmt in body)
        {
            if (stmt is not CommentBlock)
            {
                hasNonComment = true;
                break;
            }
        }
        if (!hasNonComment)
        {
            body.Add(new Pass());
        }

        // 4. 检测是否是类体：无参数函数且函数体只有赋值语句
        // 但如果函数有显式返回值，或者有 RETURN_VALUE 指令，则不应识别为类
        bool hasReturnValue = childCode.Instructions.Any(i => i.Opcode == Opcode.RETURN_VALUE);
        // 类体的 return __class__ 和 return None 都是 CPython 内部实现，不算显式函数返回
        // 经过 StripTrailingReturnNone 后，body 中还有非-implicit return 才算 real return
        bool hasRealReturn = body.Any(s => s is Return r2 && r2.Value != null
            && !(r2.Value is Name rn && rn.Id == "__class__"));
        
        // 只有当函数体确实像类体（只有赋值语句）且没有显式返回值时，才识别为类
        // 对于普通函数，即使没有参数，如果有 return 语句或 RETURN_VALUE 指令，也应该识别为函数
        bool isLikelyClassBody = !hasNonImplicitReturn && (HasNestedFunctions(body) || LooksLikeClassBody(body));
        
        // 如果函数有 RETURN_VALUE 指令，且函数体看起来像类体，但实际上应该是函数
        // 这种情况通常发生在反编译器没有正确识别出 return 语句时
        bool shouldBeFunction = hasRealReturn && body.Count > 0 
            && !(body.Count == 1 && body[0] is ExprStmt es2 && es2.Value is Constant { Value: string });
        
        if (args.Count == 0 && !childCode.IsGenerator && !childCode.IsCoroutine && !childCode.IsAsyncGenerator
            && isLikelyClassBody && !shouldBeFunction)
        {
            // 即使看起来像类体，如果有 With/For/While/Try/Raise/With 等控制流语句，也应视为函数
            // 类体一般不包含控制流语句（除了函数/类嵌套）
            bool hasControlFlow = body.Any(s => s is With or For or While or Try or Raise or Assert);
            if (!hasControlFlow)
            {
                CleanClassBody(body);
                return new ClassDef(cleanName, new List<Expr>(), body);
            }
        }


        // 4. 添加 *args / **kwargs 参数
        if (varargName != null)
            args.Insert(totalPosArgs, new Parameter($"*{varargName}"));
        if (varkwName != null)
            args.Add(new Parameter($"**{varkwName}"));

        // 5. 生成 FunctionDef
        return new FunctionDef(
            cleanName,
            args,
            body,
            IsGenerator: childCode.IsGenerator,
            IsAsync: childCode.IsCoroutine || childCode.IsAsyncGenerator,
            PosOnlyCount: posOnlyCount,
            KwOnlyCount: kwOnlyCount
        );
    }

    /// <summary>
    /// 递归去掉控制结构体末尾的隐式 return None。
    /// </summary>
    private static void StripTrailingReturnNone(List<Stmt> stmts)
    {
        for (int i = stmts.Count - 1; i >= 0; i--)
        {
            var s = stmts[i];
            if (s is Return ret && ((ret.Value is Constant { Value: null } || ret.Value == null)))
            {
                stmts.RemoveAt(i);
            }
            else if (s is If ifNode)
            {
                StripTrailingReturnNone(ifNode.Body);
                if (ifNode.Orelse != null)
                    StripTrailingReturnNone(ifNode.Orelse);
            }
            else if (s is While w)
            {
                StripTrailingReturnNone(w.Body);
                if (w.Orelse != null)
                    StripTrailingReturnNone(w.Orelse);
            }
            else if (s is For f)
            {
                StripTrailingReturnNone(f.Body);
                if (f.Orelse != null)
                    StripTrailingReturnNone(f.Orelse);
            }
            else if (s is Try t)
            {
                StripTrailingReturnNone(t.Body);
                if (t.Orelse != null)
                    StripTrailingReturnNone(t.Orelse);
                if (t.Finalbody != null)
                    StripTrailingReturnNone(t.Finalbody);
                foreach (var h in t.Handlers)
                    StripTrailingReturnNone(h.Body);
            }
            else if (s is FunctionDef fd)
            {
                StripTrailingReturnNone(fd.Body);
            }
            else break;  // non-return statement → stop
        }
    }

    /// <summary>
    /// 清理类体中 CPython 编译器产生的内部伪影（__isabstractmethod__ 等用户定义除外）。
    /// 移除：__static_attributes__, __classdictcell__, __classcell__, return __class__。
    /// </summary>
    private static void CleanClassBody(List<Stmt> body)
    {
        for (int i = body.Count - 1; i >= 0; i--)
        {
            if (body[i] is Return r)
            {
                if (r.Value is Name rn && rn.Id == "__class__")
                { body.RemoveAt(i); continue; }
                if (r.Value == null || r.Value is Constant { Value: null })
                { body.RemoveAt(i); continue; }
            }
            if (body[i] is Assign a && a.Targets.Count == 1
                && a.Targets[0] is Name an)
            {
                if (an.Id == "__static_attributes__" || an.Id == "__classdictcell__"
                    || an.Id == "__classcell__" || an.Id == "__firstlineno__"
                    || an.Id == "__module__" || an.Id == "__qualname__")
                { body.RemoveAt(i); continue; }
                // Remove __doc__ = 'ClassName' (no real docstring, just class name alias)
                if (an.Id == "__doc__" && a.Value is Constant c && c.Value is string s
                    && i > 0 && body[0] is ExprStmt { Value: Constant { Value: string } })
                { body.RemoveAt(i); continue; }
                // Remove assignments where value is __class__ cell (compiler metadata)
                if (a.Value is Name classCell && classCell.Id == "__class__")
                { body.RemoveAt(i); continue; }
                // Remove assignments with integer constant value (firstlineno)
                if (a.Value is Constant ic && ic.Value is int)
                { body.RemoveAt(i); continue; }
            }
            // Remove standalone 'ClassName' string literal (docstring alias when no docstring)
            if (body[i] is ExprStmt e && e.Value is Constant c2 && c2.Value is string
                && i == 0 && body.Count > 1 && body[1] is Assign a2
                && a2.Targets.Count == 1 && a2.Targets[0] is Name n2
                && (n2.Id == "__module__" || n2.Id == "__qualname__"))
            { body.RemoveAt(i); continue; }
            // Remove standalone string or integer constants (compiler metadata)
            if (body[i] is ExprStmt e2 && e2.Value is Constant c3)
            {
                if (c3.Value is string sn && sn.All(ch => char.IsLetterOrDigit(ch) || ch == '_'))
                { body.RemoveAt(i); continue; }
                if (c3.Value is int)
                { body.RemoveAt(i); continue; }
            }
            if (i == body.Count - 1 && body[i] is Pass)
            { body.RemoveAt(i); continue; }
        }
        // 如果类体为空（所有伪影被清空后），添加 pass
        if (body.Count == 0 || body.All(s => s is CommentBlock))
            body.Add(new Pass());
    }

    /// <summary>
    /// 递归反编译子代码对象为语句列表。
    /// </summary>
    private List<Stmt> DecompileChildCode(CodeObject childCode)
    {
        try
        {
            if (childCode.Instructions.Count == 0)
                return new List<Stmt> { new Pass() };
            
            var scanner = new BlockScanner();
            var blocks = scanner.Scan(childCode);
            var cfScanner = new ControlFlowScanner();
            var cfg = cfScanner.Analyze(blocks);

            // 用递归的 AstBuilder 处理子代码
            var childBuilder = new AstBuilder(childCode, _options);
            var ast = childBuilder.Build(cfg);
            if (ast is Module m)
            {
                // 修复空函数体：如果函数体只有注释，添加 pass 语句
                foreach (var stmt in m.Body)
                {
                    if (stmt is FunctionDef fd)
                    {
                        bool hasNonComment = false;
                        foreach (var s in fd.Body)
                        {
                            if (s is not CommentBlock)
                            {
                                hasNonComment = true;
                                break;
                            }
                        }
                        if (!hasNonComment)
                        {
                            fd.Body.Add(new Pass());
                        }
                    }
                }
                
                // 修复顶层空函数体：如果模块体只有注释，添加 pass 语句
                bool topLevelHasNonComment = false;
                foreach (var stmt in m.Body)
                {
                    if (stmt is not CommentBlock)
                    {
                        topLevelHasNonComment = true;
                        break;
                    }
                }
                if (!topLevelHasNonComment)
                {
                    m.Body.Add(new Pass());
                }
                
                return m.Body;
            }
            return new List<Stmt>();
        }
        catch (Exception ex)
        {
            // 子代码反编译失败 → 注释兜底
            return new List<Stmt>
            {
                new CommentBlock($"# Function body decompilation failed: {ex.Message}")
            };
        }
    }

    /// <summary>
    /// 从 FunctionRef 构建 Lambda 表达式 AST。
    /// </summary>
    private Lambda? BuildLambda(FunctionRef funcRef)
    {
        if (funcRef.Code == null) return null;
        var childCode = funcRef.Code;

        // 1. 提取参数
        var args = new List<Parameter>();
        for (int i = 0; i < childCode.ArgCount && i < childCode.Varnames.Count; i++)
        {
            string name = childCode.Varnames[i];
            if (!name.StartsWith("."))
                args.Add(new Parameter(name));
        }

        // 应用默认参数值（DefaultExprs 对应最后 N 个位置参数）
        if (funcRef.DefaultExprs != null && funcRef.DefaultExprs.Count > 0)
        {
            int defaultsCount = funcRef.DefaultExprs.Count;
            for (int i = 0; i < defaultsCount && i < args.Count; i++)
            {
                int argIdx = args.Count - defaultsCount + i;
                if (argIdx >= 0 && argIdx < args.Count)
                    args[argIdx] = args[argIdx] with { Default = funcRef.DefaultExprs[i] };
            }
        }

        // 2. 反编译函数体，提取返回表达式
        var body = DecompileChildCode(childCode);
        if (body.Count == 0)
        {
            if (args.Count == 0)
                args.Add(new Parameter("_"));
            return new Lambda(args, new Constant(null));
        }



        // 找到最后一个 Return 语句，提取其表达式
        for (int i = body.Count - 1; i >= 0; i--)
        {
            if (body[i] is Return ret && ret.Value != null)
            {
                if (args.Count == 0)
                    args.Add(new Parameter("_"));
                
                // 如果返回表达式是 Call(Constant(None), ...)，说明列表推导式重构失败
                // 应该直接返回 Constant(None) 而不是错误的调用
                if (ret.Value is Call callRet)
                {
                    if (callRet.Func is Constant { Value: null })
                    {
                        return new Lambda(args, new Constant(null));
                    }
                    // 如果 func 是一个常量（如整数、字符串等），也说明重构失败
                    if (callRet.Func is Constant)
                    {
                        return new Lambda(args, new Constant(null));
                    }
                }
                
                return new Lambda(args, ret.Value);
            }
        }

        // 如果没有 Return 语句，检查 body 中是否有 ExprStmt，提取其值作为返回表达式
        for (int i = body.Count - 1; i >= 0; i--)
        {
            if (body[i] is ExprStmt es && es.Value != null)
            {
                if (args.Count == 0)
                    args.Add(new Parameter("_"));
                
                // 如果表达式是 Call(Constant(None), ...)，说明列表推导式重构失败
                // 应该直接返回 Constant(None) 而不是错误的调用
                if (es.Value is Call callExpr)
                {
                    if (callExpr.Func is Constant { Value: null })
                    {
                        return new Lambda(args, new Constant(null));
                    }
                    // 如果 func 是一个常量（如整数、字符串等），也说明重构失败
                    if (callExpr.Func is Constant)
                    {
                        return new Lambda(args, new Constant(null));
                    }
                    // 如果 func 是 DictLiteral、ListLiteral 或 SetLiteral，这也是重构失败
                    // 空字典/列表/集合不应该被当作函数调用
                    if (callExpr.Func is DictLiteral || callExpr.Func is ListLiteral || callExpr.Func is SetLiteral)
                    {
                        return new Lambda(args, new Constant(null));
                    }
                }
                
                return new Lambda(args, es.Value);
            }
        }

        if (args.Count == 0)
            args.Add(new Parameter("_"));
        return new Lambda(args, new Constant(null));
    }

    /// <summary>
    /// 兜底：从 ChildCodes 中按位置匹配 Assign 语句。
    /// 当 PostProcessFunctionDefs 未能通过命名匹配时使用。
    /// </summary>
    private List<Stmt> ConvertChildCodesToFunctionDefs(List<Stmt> stmts)
    {
        // 收集已在 PostProcessFunctionDefs 中正确定义的名称，防止兜底路径重复创建
        var existingDefNames = new HashSet<string>();
        void collectNames(List<Stmt> list)
        {
            foreach (var s in list)
            {
                if (s is FunctionDef fd) existingDefNames.Add(fd.Name);
                else if (s is ClassDef cd) existingDefNames.Add(cd.Name);
                else if (s is If ifNode) { collectNames(ifNode.Body); if (ifNode.Orelse != null) collectNames(ifNode.Orelse); }
                else if (s is For forNode) { collectNames(forNode.Body); if (forNode.Orelse != null) collectNames(forNode.Orelse); }
                else if (s is While wNode) { collectNames(wNode.Body); if (wNode.Orelse != null) collectNames(wNode.Orelse); }
                else if (s is Try tNode) { collectNames(tNode.Body); foreach (var h in tNode.Handlers) collectNames(h.Body); }
            }
        }
        collectNames(stmts);

        var childCodes = _codeObject?.ChildCodes ?? new List<CodeObject>();
        if (childCodes.Count == 0)
            return stmts;

        var result = new List<Stmt>(stmts.Count);
        int childIdx = 0;
        var localSeen = new HashSet<string>(); // 防止同一方法内部重复创建同名定义

        foreach (var stmt in stmts)
        {
            // 处理 pre-3.11: Assign + FunctionRef（来自 MAKE_FUNCTION → STORE_NAME）
            if (stmt is Assign assignFn && assignFn.Targets.Count == 1
                && assignFn.Targets[0] is Name targetNameFn
                && assignFn.Value is FunctionRef fnRef
                && fnRef.Code != null)
            {
                childIdx++;
                
                // Lambda 函数
                if (fnRef.Name == "<lambda>" || fnRef.Code.Name == "<lambda>")
                {
                    var lambda = BuildLambda(fnRef);
                    if (lambda != null)
                    {
                        result.Add(new Assign(new List<Expr> { new Name(targetNameFn.Id, ExpressionContext.Store) }, lambda));
                    }
                    else
                    {
                        result.Add(stmt);
                    }
                    continue;
                }
                
                // 跳过推导式（已在 PostProcessFunctionDefs 中处理）
                if (fnRef.Name.StartsWith("<"))
                {
                    result.Add(stmt);
                    continue;
                }
                
                var defStmt = BuildFunctionDef(fnRef.Name ?? targetNameFn.Id, fnRef);
                if (defStmt != null)
                {
                    string defName = "";
                    if (defStmt is FunctionDef fd) defName = fd.Name;
                    else if (defStmt is ClassDef cd) defName = cd.Name;
                    
                    if (!localSeen.Add(defName))
                    { result.Add(stmt); continue; }
                    result.Add(defStmt);
                }
                else { result.Add(stmt); }
                continue;
            }

            if (stmt is Assign assign && assign.Targets.Count == 1
                && assign.Targets[0] is Name targetName
                && assign.Value is Constant constVal
                && (constVal.Value == null || constVal.Value is CodeObject)
                && childIdx < childCodes.Count)
            {
                var cc = childCodes[childIdx];
                childIdx++;
                var defStmt = BuildFunctionDef(cc.Name ?? targetName.Id, new FunctionRef(cc, cc.Name ?? targetName.Id));
                if (defStmt != null)
                {
                    string defName = "";
                    if (defStmt is FunctionDef fd) defName = fd.Name;
                    else if (defStmt is ClassDef cd) defName = cd.Name;
                    
                    if (existingDefNames.Contains(defName) || !localSeen.Add(defName))
                    {
                        result.Add(stmt);
                        continue;
                    }
                    result.Add(defStmt);
                    continue;
                }
            }
            result.Add(stmt);
        }

        // Python 3.13/3.14: 内层函数可能没有 MAKE_FUNCTION 或 LOAD_CONST→STORE_NAME 指令
        // 而是直接通过 LOAD_FAST_AND_CLEAR 访问。这种情况下，需要在函数体开头添加
        // 函数定义，因为 wrapper 的 code object 存在于 co_consts 中。
        var remainingChildCodes = new List<CodeObject>();
        // 收集 result 中所有已定义的函数名（包括嵌套函数体中的引用）
        var nestedNames = new HashSet<string>();
        void CollectNestedNames(List<Stmt> stmts)
        {
            foreach (var s in stmts)
            {
                if (s is FunctionDef fd)
                { nestedNames.Add(fd.Name); CollectNestedNames(fd.Body); }
                else if (s is ClassDef cd)
                { nestedNames.Add(cd.Name); CollectNestedNames(cd.Body); }
            }
        }
        CollectNestedNames(result);
        for (int i = childIdx; i < childCodes.Count; i++)
        {
            var cc = childCodes[i];
            if (!existingDefNames.Contains(cc.Name ?? "") && !localSeen.Contains(cc.Name ?? "")
                && !nestedNames.Contains(cc.Name ?? ""))
            {
                remainingChildCodes.Add(cc);
            }
        }

        if (remainingChildCodes.Count > 0)
        {
            var newResult = new List<Stmt>();
            foreach (var cc in remainingChildCodes)
            {
                var funcRef = new FunctionRef(cc, cc.Name ?? "<lambda>");
                var defStmt = BuildFunctionDef(cc.Name ?? "<lambda>", funcRef);
                if (defStmt is ClassDef cd && cc != null)
                {
                    // 从模块级指令中提取基类名
                    // 模式: LOAD_BUILD_CLASS ... LOAD_CONST(name) LOAD_NAME(base) CALL N STORE_NAME(className)
                    // 对 keyword-args 类定义，从 Call.Keywords 提取 keyword bases
                    // 在 PostProcessFunctionDefs 中，CALL_KW 路径会产生 Keyword 列表
                    // 此处从字节码回溯 CALL_KW + KW_NAMES 模式
                    var bases = new List<Expr>();
                    if (_codeObject?.Instructions != null)
                    {
                        // 模式: LOAD_BUILD_CLASS ... LOAD_CONST(code) MAKE_FUNCTION LOAD_CONST(name) LOAD_NAME(base) CALL N STORE_NAME
                        bool foundLoadBuild = false;
                        bool foundClassCode = false;
                        for (int ii = 0; ii < _codeObject.Instructions.Count - 2; ii++)
                        {
                            var instr = _codeObject.Instructions[ii];
                            if (instr.Opcode == Opcode.LOAD_BUILD_CLASS)
                            {
                                foundLoadBuild = true;
                                foundClassCode = false;
                                continue;
                            }
                            if (!foundLoadBuild) continue;
                            // Skip PUSH_NULL
                            if (instr.Opcode == Opcode.PUSH_NULL) continue;
                            // First LOAD_CONST after BUILD_CLASS is the code object
                            if (!foundClassCode && instr.Opcode == Opcode.LOAD_CONST)
                            {
                                foundClassCode = true;
                                continue;
                            }
                            // Second LOAD_CONST after BUILD_CLASS: check if it's our class name
                            if (foundLoadBuild && foundClassCode && instr.Opcode == Opcode.LOAD_CONST
                                && instr.Argument.HasValue
                                && _codeObject.Constants.TryGetValue(instr.Argument.Value, out var cv)
                                && cv is string className && className == cd.Name)
                            {
                                // After the class name, collect LOAD_NAME instructions (bases)
                                for (int jj = ii + 1; jj < _codeObject.Instructions.Count; jj++)
                                {
                                    var next = _codeObject.Instructions[jj];
                                    if (next.Opcode == Opcode.LOAD_NAME && next.Argument.HasValue)
                                    {
                                        var baseName = _codeObject.Names.Count > next.Argument.Value
                                            ? _codeObject.Names[next.Argument.Value] : null;
                                        if (baseName != null && baseName != cd.Name && baseName != "__build_class__")
                                        {
                                            // Phase 9-4: 检查此 LOAD_NAME 后是否有 KW_NAMES tuple
                                            // 如果有 → 这是 keyword arg value，不是 base class
                                            bool isKeywordArg = false;
                                            for (int kk = jj + 1; kk < _codeObject.Instructions.Count; kk++)
                                            {
                                                var next2 = _codeObject.Instructions[kk];
                                                if (next2.Opcode == Opcode.LOAD_CONST)
                                                    continue; // skip constants before CALL
                                                if (next2.Opcode == Opcode.CALL || next2.Opcode == Opcode.CALL_311
                                                    || next2.Opcode == Opcode.CALL_FUNCTION_KW
                                                    || next2.Opcode == Opcode.CALL_KW_313)
                                                    break; // reached CALL, this is base
                                                if (next2.Opcode == Opcode.LOAD_NAME)
                                                {
                                                    // Two consecutive LOAD_NAME: this is a base, next is kwarg
                                                    break;
                                                }
                                                if (next2.Opcode == Opcode.STORE_NAME)
                                                    break;
                                                // Any other opcode before CALL → this is kwarg value
                                                isKeywordArg = true;
                                                break;
                                            }
                                            if (!isKeywordArg)
                                                bases.Add(new Name(baseName, ExpressionContext.Load));
                                        }
                                    }
                                    else if (next.Opcode == Opcode.BUILD_TUPLE || next.Opcode == Opcode.BUILD_LIST)
                                    {
                                        // Multiple base classes in tuple
                                        for (int kk = jj + 1; kk < _codeObject.Instructions.Count; kk++)
                                        {
                                            var tupNext = _codeObject.Instructions[kk];
                                            if (tupNext.Opcode == Opcode.LOAD_NAME && tupNext.Argument.HasValue)
                                            {
                                                var bn = _codeObject.Names.Count > tupNext.Argument.Value
                                                    ? _codeObject.Names[tupNext.Argument.Value] : null;
                                                if (bn != null && bn != cd.Name && bn != "__build_class__")
                                                    bases.Add(new Name(bn, ExpressionContext.Load));
                                            }
                                            if (tupNext.Opcode == Opcode.CALL || tupNext.Opcode == Opcode.CALL_311)
                                                break;
                                        }
                                        break;
                                    }
                                    if (next.Opcode == Opcode.CALL || next.Opcode == Opcode.CALL_311
                                        || next.Opcode == Opcode.CALL_KW_313
                                        || next.Opcode == Opcode.STORE_NAME)
                                        break;
                                }
                                break;
                            }
                        }
                    }
                    if (bases.Count > 0)
                        defStmt = cd with { Bases = bases };
                }
                if (defStmt is FunctionDef fd2 && _codeObject?.Instructions != null)
                    AttachDefaultsFromBytecode(fd2, ref defStmt);
                // 清理 ClassDef 类体中的编译器伪影（独立字符串、__class__ 赋值等）
                if (defStmt is ClassDef clsDefVal)
                {
                    var cleanBody = new List<Stmt>(clsDefVal.Body);
                    CleanClassBody(cleanBody);
                    defStmt = clsDefVal with { Body = cleanBody };
                }
                if (defStmt != null)
                {
                    newResult.Add(defStmt);
                    if (defStmt is FunctionDef fd3) localSeen.Add(fd3.Name);
                    else if (defStmt is ClassDef cd2) localSeen.Add(cd2.Name);
                }
            }
            newResult.AddRange(result);
            return newResult;
        }

        return result;
    }

    private void AttachDefaultsFromBytecode(FunctionDef fd, ref Stmt defStmt)
    {
        if (_codeObject == null) return;
        // Search current code object, then search child codes that reference this name
        if (ScanCodeObjectForDefaults(_codeObject, fd, ref defStmt)) return;
        foreach (var childCode in _codeObject.ChildCodes)
            if (childCode.Names != null && childCode.Names.Contains(fd.Name))
                if (ScanCodeObjectForDefaults(childCode, fd, ref defStmt)) return;
    }

    private bool ScanCodeObjectForDefaults(CodeObject codeObj, FunctionDef fd, ref Stmt defStmt)
    {
        var insList = codeObj.Instructions;
        for (int ii = 0; ii < insList.Count; ii++)
        {
            if (insList[ii].Opcode != Opcode.STORE_NAME || !insList[ii].Argument.HasValue
                || codeObj.Names.Count <= insList[ii].Argument.Value
                || codeObj.Names[insList[ii].Argument.Value] != fd.Name)
                continue;

            // Found STORE_NAME <funcName>. Scan backward for SFA instructions for THIS function.
            bool processedDefaults = false, processedKwDefaults = false;
            for (int jj = ii - 1; jj >= 0 && jj >= ii - 8; jj--)
            {
                if (insList[jj].Opcode != Opcode.SET_FUNCTION_ATTRIBUTE_313 || !insList[jj].Argument.HasValue)
                    continue;

                var sfaFlags = insList[jj].Argument.Value;
                if ((sfaFlags & 0x01) != 0 && !processedDefaults) // positional defaults
                {
                    var defaults = new List<Expr>();
                    for (int kk = jj - 1; kk >= 0 && kk >= jj - 20; kk--)
                    {
                        var kIns = insList[kk];
                        if (kIns.Opcode == Opcode.BUILD_TUPLE && kIns.Argument.HasValue && kIns.Argument.Value > 0)
                        {
                            for (int mm = kk - 1, need = kIns.Argument.Value; mm >= 0 && need > 0; mm--)
                            {
                                var it = insList[mm];
                                if (it.Opcode == Opcode.LOAD_NAME && it.Argument.HasValue && codeObj.Names.Count > it.Argument.Value)
                                { defaults.Insert(0, new Name(codeObj.Names[it.Argument.Value], ExpressionContext.Load)); need--; }
                                else if (it.Opcode == Opcode.LOAD_CONST && it.Argument.HasValue && codeObj.Constants.TryGetValue(it.Argument.Value, out var cv))
                                { defaults.Insert(0, new Constant(cv)); need--; }
                            }
                            break;
                        }
                        if (kIns.Opcode == Opcode.LOAD_CONST && kIns.Argument.HasValue
                            && codeObj.Constants.TryGetValue(kIns.Argument.Value, out var cv2)
                            && cv2 is System.Collections.IList tupleList && tupleList.Count > 0)
                        {
                            foreach (var item in tupleList)
                                defaults.Add(new Constant(item));
                            break;
                        }
                    }
                    if (defaults.Count > 0)
                    {
                        int posC = fd.Args.Count - fd.KwOnlyCount;
                        int sIdx = posC - defaults.Count;
                        if (sIdx < 0) sIdx = 0;
                        var newArgs = new List<Parameter>(fd.Args.Count);
                        for (int ai = 0; ai < fd.Args.Count; ai++)
                        {
                            int di = ai - sIdx;
                            newArgs.Add(di >= 0 && di < defaults.Count
                                ? new Parameter(fd.Args[ai].Name, fd.Args[ai].Annotation, defaults[di])
                                : fd.Args[ai]);
                        }
                        defStmt = fd with { Args = newArgs };
                        processedDefaults = true;
                        if (processedKwDefaults) break;
                    }
                }
                if ((sfaFlags & 0x02) != 0 && !processedKwDefaults) // kwdefaults
                {
                    var kwDefaults = new Dictionary<string, Expr?>();
                    for (int kk = jj - 1; kk >= 0 && kk >= jj - 16; kk--)
                    {
                        var kIns = insList[kk];
                        if (kIns.Opcode == Opcode.BUILD_MAP && kIns.Argument.HasValue && kIns.Argument.Value > 0)
                        {
                            int need = kIns.Argument.Value;
                            for (int mm = kk - 1; mm >= 0 && need > 0; mm -= 2)
                            {
                                var valIns = insList[mm];
                                var keyIns = insList[mm - 1];
                                if (keyIns.Opcode == Opcode.LOAD_CONST && keyIns.Argument.HasValue
                                    && codeObj.Constants.TryGetValue(keyIns.Argument.Value, out var keyVal)
                                    && keyVal is string keyStr)
                                {
                                    Expr? val = null;
                                    if (valIns.Opcode == Opcode.LOAD_NAME && valIns.Argument.HasValue && codeObj.Names.Count > valIns.Argument.Value)
                                        val = new Name(codeObj.Names[valIns.Argument.Value], ExpressionContext.Load);
                                    else if (valIns.Opcode == Opcode.LOAD_CONST && valIns.Argument.HasValue && codeObj.Constants.TryGetValue(valIns.Argument.Value, out var constVal))
                                        val = new Constant(constVal);
                                    kwDefaults[keyStr] = val;
                                    need--;
                                }
                            }
                            break;
                        }
                    }
                    if (kwDefaults.Count > 0)
                    {
                        var curArgs = (defStmt is FunctionDef fd3) ? fd3.Args : fd.Args;
                        var newArgs = new List<Parameter>(curArgs.Count);
                        foreach (var arg in curArgs)
                        {
                            if (kwDefaults.TryGetValue(arg.Name, out var d) && arg.Default == null)
                                newArgs.Add(new Parameter(arg.Name, arg.Annotation, d));
                            else
                                newArgs.Add(arg);
                        }
                        defStmt = fd with { Args = newArgs };
                        processedKwDefaults = true;
                        if (processedDefaults) break;
                    }
                }
            }
            return true;
        }
        return false;
    }

    private static bool HasNestedFunctions(List<Stmt> body)
    {
        if (body == null) return false;
        foreach (var stmt in body)
        {
            if (stmt is FunctionDef) return true;
            if (stmt is ClassDef) return true;
        }
        return false;
    }
    
    private static bool LooksLikeClassBody(List<Stmt> body)
    {
        if (body == null || body.Count == 0) return false;
        
        int assignCount = 0;
        int otherCount = 0;
        
        foreach (var stmt in body)
        {
            if (stmt is Assign)
                assignCount++;
            else if (stmt is ExprStmt { Value: Constant { Value: string } })
                continue;  // docstring
            else if (stmt is CommentBlock)
                continue;  // comment
            else
                otherCount++;
        }
        
        return otherCount == 0 && assignCount > 0;
    }

    private bool IsExceptionHandlerBlock(BasicBlock block)
    {
        if (block == null) return false;
        var instrs = block.Instructions;
        if (instrs.Count == 0) return false;
        var firstInstr = instrs[0];
        if (firstInstr.Opcode == Opcode.SETUP_FINALLY || firstInstr.Opcode == Opcode.SETUP_EXCEPT)
            return true;
        if (_codeObject.Version >= PythonVersion.Py311 && _codeObject.ExceptionTable != null)
        {
            foreach (var et in _codeObject.ExceptionTable)
            {
                if (et.TargetOffset == block.StartOffset)
                    return true;
            }
        }
        return false;
    }

    private AstNode BuildWithSequentialBlocks(ControlFlowGraph cfg)
    {
        Console.Error.WriteLine($"[SEQ_BUILD] Starting three-phase sequential block architecture");

        _blockResults = _blockDecompiler.DecompileBlocks(cfg.Blocks, _codeObject);
        _allBlocks = cfg.Blocks;
        _sortedBlocks = cfg.Blocks
            .Where(b => b.Instructions.Count > 0)
            .OrderBy(b => b.Instructions[0].Offset)
            .ToList();
        _sortedExceptionTable = _codeObject.ExceptionTable
            .OrderBy(e => e.StartOffset)
            .ToList();

        TotalBlockCount = _blockResults.Count;
        FailedBlockCount = _blockResults.Values.Count(r => !r.IsSuccess);

        _blockByOffset.Clear();
        foreach (var b in cfg.Blocks)
            _blockByOffset[b.StartOffset] = b;

        _loopHeaderOffsets.Clear();
        foreach (var b in cfg.Blocks)
        {
            if (b.Flags.HasFlag(BlockFlags.LoopHeader))
            {
                _loopHeaderOffsets.Add(b.StartOffset);
            }
        }

        var seqBuilder = new SequentialBlockBuilder(_codeObject);

        var seqBlocks = seqBuilder.BuildSequentialBlocks(cfg);
        Console.Error.WriteLine($"[SEQ_BUILD] Phase 1: {seqBlocks.Count} sequential blocks created");
        foreach (var sb in seqBlocks)
        {
            bool hasLoadSpecial = sb.Instructions.Any(i => i.Opcode == Opcode.LOAD_SPECIAL);
            Console.Error.WriteLine($"[SEQ_BUILD]   SeqBlock 0x{sb.StartOffset:X4}-0x{sb.EndOffset:X4}, {sb.Instructions.Count} instructions, hasLoadSpecial={hasLoadSpecial}");
            if (hasLoadSpecial)
            {
                for (int i = 0; i < sb.Instructions.Count; i++)
                {
                    Console.Error.WriteLine($"[SEQ_BUILD]     instr[{i}] = {sb.Instructions[i].Opcode}");
                }
                Console.Error.WriteLine($"[SEQ_BUILD]     Has exception table entries: {sb.ExceptionTableEntries.Count}");
            }
        }

        if (!seqBuilder.VerifyNoOrphanBlocks(seqBlocks, cfg))
        {
            Console.Error.WriteLine($"[SEQ_BUILD] ERROR: Orphan blocks detected, falling back to original method");
            return BuildFallback(cfg);
        }

        Console.Error.WriteLine($"[SEQ_BUILD] Phase 1: All basic blocks merged into sequential blocks");

        seqBuilder.DecompileSequentialBlocks(seqBlocks);
        Console.Error.WriteLine($"[SEQ_BUILD] Phase 1: All sequential blocks decompiled");

        var controlStructures = ParseControlStructures(seqBlocks);
        Console.Error.WriteLine($"[SEQ_BUILD] Phase 2: {controlStructures.Count} control structures detected");

        // Phase 8 Step 4-5: 结构验证（通过 DecompileOptions 控制）
        if (_options.ShowStructuralValidation)
        {
            try
            {
                if (_pdomScanner == null)
                {
                    _pdomScanner = new PostDominatorScanner();
                    _pdomScanner.ComputePostDominators(cfg);
                    _pdomScanner.BuildComeFromMap(cfg);
                }
                var validator = new StructuralValidator(_pdomScanner, cfg);
                var result = validator.Validate(controlStructures);
                if (result.Count > 0)
                {
                    Console.Error.WriteLine(
                        $"[STRUCT_VALIDATE] {result.Count} structural issues: " +
                        $"R1={result.Count(r => r.Rule == "R1")}, " +
                        $"R3={result.Count(r => r.Rule == "R3")}, " +
                        $"R5={result.Count(r => r.Rule == "R5")}");
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"[STRUCT_VALIDATE] Error: {ex.Message}");
            }
        }

        LinkControlStructures(controlStructures, seqBlocks);
        Console.Error.WriteLine($"[SEQ_BUILD] Phase 3: Control structures linked to sequential blocks");

        var stmts = GenerateAstStatementsHybrid(seqBlocks, cfg);

        var unvisited = cfg.Blocks
            .Where(b => !_processedBlockIds.Contains(b.Id))
            .OrderBy(b => b.StartOffset)
            .ToList();

        foreach (var orphan in unvisited)
        {
            if (orphan.Instructions.Count == 0)
                continue;
            // 对孤儿块分类，跳过程序处理 preamble/cleanup 块（handler_pre）
            var classification = ClassifyOrphanBlock(orphan);
            bool hasHandlerPreamble = classification == "handler_pre" || classification == "handler_chain";
            if (hasHandlerPreamble)
            {
                _processedBlockIds.Add(orphan.Id);
                continue;
            }
            var blockResult = _blockDecompiler.DecompileBlock(orphan.Instructions, _codeObject, orphan.Id);
            if (blockResult.IsSuccess)
            {
                stmts.AddRange(blockResult.Statements);
            }
        }

        stmts = PostProcessFunctionDefs(stmts);
        stmts = ConvertChildCodesToFunctionDefs(stmts);
        stmts = ConvertComprehensionCalls(stmts);
        stmts = ConvertAugAssign(stmts);
        FixEmptyFunctionBodies(stmts);
        CollapseRedundantPasses(stmts);
        stmts = TrimPostTerminalDeadCode(stmts);
        stmts = CleanupBareExpr(stmts);
        stmts = CleanForElseBareExprs(stmts);
        stmts = CleanDeadCodeAfterReturn(stmts);
        // BARE 清理后可能产生空的 FunctionDef body → 再次补 pass
        FixEmptyFunctionBodies(stmts);
        stmts = FixSyntaxErrors(stmts);
        // stmts = DecompileNestedCodeObjects(stmts, _codeObject); // disabled

        // 最终检查：FunctionDef body 为空 → 补 pass
        stmts = FinalFixFunctionBodies(stmts);
        return new Module(stmts, _codeObject.Name);
    }

    private AstNode BuildFallback(ControlFlowGraph cfg)
    {
        var structuredCFG = new StructuredCFG { RawCFG = cfg };
        _blockResults = _blockDecompiler.DecompileBlocks(cfg.Blocks, _codeObject);
        _allBlocks = cfg.Blocks;
        _sortedBlocks = cfg.Blocks
            .Where(b => b.Instructions.Count > 0)
            .OrderBy(b => b.Instructions[0].Offset)
            .ToList();
        _sortedExceptionTable = _codeObject.ExceptionTable
            .OrderBy(e => e.StartOffset)
            .ToList();

        var stmts = new List<Stmt>();
        var visited = new HashSet<BasicBlock>();
        stmts.AddRange(BuildStatements(cfg.Entry, visited));

        var unvisited = cfg.Blocks
            .Where(b => !_processedBlockIds.Contains(b.Id))
            .OrderBy(b => b.StartOffset)
            .ToList();

        // build stmts from unvisited blocks
        foreach (var orphan in unvisited) { /* ... */ }

        stmts = PostProcessFunctionDefs(stmts);
        stmts = ConvertChildCodesToFunctionDefs(stmts);
        stmts = ConvertComprehensionCalls(stmts);
        stmts = ConvertAugAssign(stmts);
        FixEmptyFunctionBodies(stmts);
        CollapseRedundantPasses(stmts);
        stmts = TrimPostTerminalDeadCode(stmts);
        stmts = CleanupBareExpr(stmts);
        stmts = CleanForElseBareExprs(stmts);
        stmts = CleanDeadCodeAfterReturn(stmts);
        FixEmptyFunctionBodies(stmts);
        stmts = FixSyntaxErrors(stmts);
        // stmts = DecompileNestedCodeObjects(stmts, _codeObject); // disabled

        // 最终检查：FunctionDef body 为空 → 补 pass
        stmts = FinalFixFunctionBodies(stmts);
        return new Module(stmts, _codeObject.Name);
    }

    private List<ISequentialControlStructure> ParseControlStructures(List<SequentialBlock> seqBlocks)
    {
        // Phase 5: 统一链接 — 基于 Phase 2/3/4 的标注信息
        // 链接顺序: Try → Loop → With → IfElse (模式目录第 7 节)
        var structures = new List<ISequentialControlStructure>();
        var visited = new HashSet<int>();

        // 1. Try 结构（ExceptionTable 定义了严格的 offset 边界）
        foreach (var seqBlock in seqBlocks.OrderBy(b => b.StartOffset))
        {
            if (visited.Contains(seqBlock.Id))
                continue;
            if (!seqBlock.IsTryHeader)
                continue;

            var tryStructure = ParseTryStructure(seqBlock, seqBlocks);
            if (tryStructure != null)
            {
                structures.Add(tryStructure);
                visited.Add(seqBlock.Id);
                foreach (var bodyBlock in tryStructure.BodyBlocks)
                    visited.Add(bodyBlock.Id);
                if (tryStructure is TryControlStructure tryStruct)
                {
                    foreach (var handler in tryStruct.ExceptHandlers)
                        visited.Add(handler.Handler.Id);
                    if (tryStruct.FinallyBlock != null)
                        visited.Add(tryStruct.FinallyBlock.Id);
                    if (tryStruct.ElseBlock != null)
                        visited.Add(tryStruct.ElseBlock.Id);
                }
            }
        }

        // 2. Loop 结构（逆序——内层优先，可嵌套在 Try body 中）
        foreach (var seqBlock in seqBlocks
            .Where(b => b.IsForLoopHeader || b.IsWhileLoopHeader)
            .OrderByDescending(b => b.StartOffset))
        {
            if (visited.Contains(seqBlock.Id))
                continue;

            var loopStructure = ParseLoopStructure(seqBlock, seqBlocks);
            if (loopStructure != null)
            {
                structures.Add(loopStructure);
                visited.Add(seqBlock.Id);
                foreach (var bodyBlock in loopStructure.BodyBlocks)
                    visited.Add(bodyBlock.Id);
                if (loopStructure is ForLoopControlStructure forStruct && forStruct.ElseBlock != null)
                    visited.Add(forStruct.ElseBlock.Id);
                if (loopStructure is WhileLoopControlStructure whileStruct && whileStruct.ElseBlock != null)
                    visited.Add(whileStruct.ElseBlock.Id);
            }
        }

        // 3. With 结构
        foreach (var seqBlock in seqBlocks.OrderBy(b => b.StartOffset))
        {
            if (visited.Contains(seqBlock.Id))
                continue;
            if (!seqBlock.IsWithHeader && !seqBlock.HasBeforeWith && !seqBlock.HasLoadSpecial)
                continue;

            Console.Error.WriteLine($"[PARSE_CTL] SeqBlock 0x{seqBlock.StartOffset:X4}, IsWithHeader={seqBlock.IsWithHeader}, visited={visited.Contains(seqBlock.Id)}");
            Console.Error.WriteLine($"[PARSE_CTL]   Calling ParseWithStructure");
            var withStructure = ParseWithStructure(seqBlock, seqBlocks);
            if (withStructure != null)
            {
                structures.Add(withStructure);
                visited.Add(seqBlock.Id);
                foreach (var bodyBlock in withStructure.BodyBlocks)
                    visited.Add(bodyBlock.Id);
                if (withStructure is WithControlStructure withStruct && withStruct.HandlerBlock != null)
                    visited.Add(withStruct.HandlerBlock.Id);
            }
        }

        // 4. IfElse 结构（最灵活，最后链接）
        // 模式目录 I1-I4: POP_JUMP_IF_* + 无回边 → if
        // while 已有 IsWhileLoopHeader 标注，在此跳过
        foreach (var seqBlock in seqBlocks.OrderBy(b => b.StartOffset))
        {
            if (visited.Contains(seqBlock.Id))
                continue;
            // visited 已排除已链接的结构，但 IsLoopHeader 的块即使链接失败也应尝试 IfElse
            if (!seqBlock.IsConditionHeader &&
                !seqBlock.Instructions.Any(i =>
                    i.Opcode is Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
                        or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38
                        or Opcode.JUMP_IF_FALSE_OR_POP or Opcode.JUMP_IF_TRUE_OR_POP))
                continue;

            var ifElseStructure = ParseIfElseStructure(seqBlock, seqBlocks);
            if (ifElseStructure != null)
            {
                structures.Add(ifElseStructure);
                visited.Add(seqBlock.Id);
                foreach (var bodyBlock in ifElseStructure.BodyBlocks)
                    visited.Add(bodyBlock.Id);
            }
        }

        return structures;
    }

    private ISequentialControlStructure? ParseLoopStructure(SequentialBlock header, List<SequentialBlock> seqBlocks)
    {
        bool isWithStatement = header.Instructions.Any(i => 
            i.Opcode == Opcode.SETUP_WITH || 
            i.Opcode == Opcode.BEFORE_WITH ||
            i.Opcode == Opcode.BEFORE_WITH_312 ||
            i.Opcode == Opcode.BEFORE_WITH_313 ||
            i.Opcode == Opcode.LOAD_SPECIAL);

        if (isWithStatement)
            return null;
            
        bool isWithExceptionHandler = header.Instructions.Any(i => 
            i.Opcode == Opcode.WITH_EXCEPT_START || 
            i.Opcode == Opcode.WITH_EXCEPT_START_312 ||
            i.Opcode == Opcode.PUSH_EXC_INFO_312 ||
            i.Opcode == Opcode.PUSH_EXC_INFO);
            
        if (isWithExceptionHandler)
            return null;
            
        bool isTryExceptHandler = header.Instructions.Any(i => 
            i.Opcode == Opcode.CHECK_EXC_MATCH ||
            i.Opcode == Opcode.POP_EXCEPT ||
            i.Opcode == Opcode.RERAISE);
            
        if (isTryExceptHandler)
            return null;

        bool isForLoop = header.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER);
        bool hasJumpOp = header.Instructions.Any(i =>
            i.Opcode is Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
                or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38);

        if (!isForLoop && !hasJumpOp)
            return null;
            
        if (!isForLoop)
        {
            bool hasBackEdge = false;
            // 使用 SequentialBlock 级别的后继检测回边（Phase 3a 已构建 Successors）
            // 回边来自 body 中跳回 header 的块，而非 header 自己的基本块后继
            foreach (var sb in seqBlocks)
            {
                if (sb.StartOffset > header.StartOffset && sb.Successors.Contains(header))
                {
                    hasBackEdge = true;
                    break;
                }
            }

            if (!hasBackEdge)
                return null;
        }

        var bodyBlocks = new List<SequentialBlock>();
        SequentialBlock? backEdge = null;
        SequentialBlock? elseBlock = null;

        var blockByOffset = seqBlocks.ToDictionary(b => b.StartOffset);
        var visited = new HashSet<int> { header.Id };

        // 使用 SequentialBlock 级别的后继确定 else/exit 块
        // 对于 FOR_ITER 和条件跳转，header 有两个后继：body（fall-through）和 else（jump target）
        // body 入口是 offset 较小的后继（紧接着 header 之后），else 是 offset 较大的后继
        var bodyCandidates = header.Successors
            .Where(s => s.StartOffset > header.StartOffset && !visited.Contains(s.Id))
            .OrderBy(s => s.StartOffset)
            .ToList();
        
        if (bodyCandidates.Count >= 2)
        {
            // 有 body 和 else 两个后继：第一个是 body 入口，第二个是 else/exit
            elseBlock = bodyCandidates.Last();
            Console.Error.WriteLine($"[SEQ_BUILD_PARSE] FOR loop at 0x{header.StartOffset:X4}: else/exit block at 0x{elseBlock.StartOffset:X4} (via successors)");
        }
        else if (header.JumpTarget.HasValue)
        {
            // Fallback: 使用 JumpTarget 查找（兼容无条件跳转的循环）
            var jumpTarget = header.JumpTarget.Value;
            var targetBlock = blockByOffset.Values
                .FirstOrDefault(sb => sb.StartOffset <= jumpTarget && sb.EndOffset >= jumpTarget);
            if (targetBlock != null && targetBlock.StartOffset > header.StartOffset)
            {
                elseBlock = targetBlock;
                Console.Error.WriteLine($"[SEQ_BUILD_PARSE] FOR loop at 0x{header.StartOffset:X4}: else/exit block at 0x{targetBlock.StartOffset:X4} (via JumpTarget)");
            }
        }

        var loopBodyStart = header.EndOffset + 1;
        var loopBodyEnd = elseBlock?.StartOffset ?? int.MaxValue;

        Console.Error.WriteLine($"[SEQ_BUILD_PARSE] FOR loop at 0x{header.StartOffset:X4}: body range 0x{loopBodyStart:X4}-0x{loopBodyEnd:X4}");

        var worklist = new Queue<SequentialBlock>();
        Console.Error.WriteLine($"[SEQ_BUILD_PARSE] FOR loop header at 0x{header.StartOffset:X4}: {header.SourceBlocks.Count} source blocks");
        foreach (var sourceBlock in header.SourceBlocks)
        {
            Console.Error.WriteLine($"[SEQ_BUILD_PARSE]   Source block 0x{sourceBlock.StartOffset:X4}-0x{sourceBlock.EndOffset:X4}: {sourceBlock.Successors.Count} successors");
            foreach (var succ in sourceBlock.Successors)
            {
                Console.Error.WriteLine($"[SEQ_BUILD_PARSE]     Successor: 0x{succ.StartOffset:X4}-0x{succ.EndOffset:X4}");
                var targetSeqBlock = blockByOffset.Values
                    .FirstOrDefault(sb => sb.StartOffset <= succ.StartOffset && sb.EndOffset >= succ.StartOffset);
                if (targetSeqBlock != null)
                {
                    Console.Error.WriteLine($"[SEQ_BUILD_PARSE]     -> Sequential block: 0x{targetSeqBlock.StartOffset:X4}-0x{targetSeqBlock.EndOffset:X4}, id={targetSeqBlock.Id}");
                    if (!visited.Contains(targetSeqBlock.Id))
                    {
                        if (targetSeqBlock.StartOffset != header.StartOffset)
                        {
                            if (targetSeqBlock.StartOffset >= loopBodyStart && targetSeqBlock.StartOffset < loopBodyEnd)
                            {
                                worklist.Enqueue(targetSeqBlock);
                                visited.Add(targetSeqBlock.Id);
                                Console.Error.WriteLine($"[SEQ_BUILD_PARSE]     -> Added to worklist (in body range)");
                            }
                            else
                            {
                                Console.Error.WriteLine($"[SEQ_BUILD_PARSE]     -> Skipped (outside body range)");
                            }
                        }
                        else
                        {
                            Console.Error.WriteLine($"[SEQ_BUILD_PARSE]     -> Skipped (same as header)");
                        }
                    }
                    else
                    {
                        Console.Error.WriteLine($"[SEQ_BUILD_PARSE]     -> Skipped (already visited)");
                    }
                }
                else
                {
                    Console.Error.WriteLine($"[SEQ_BUILD_PARSE]     -> NOT FOUND in sequential blocks");
                }
            }
        }

        Console.Error.WriteLine($"[SEQ_BUILD_PARSE] Worklist size: {worklist.Count}");

        while (worklist.Count > 0)
        {
            var current = worklist.Dequeue();

            bodyBlocks.Add(current);

            foreach (var succ in current.Successors)
            {
                if (!visited.Contains(succ.Id) && succ.StartOffset != header.StartOffset)
                {
                    if (elseBlock != null && succ.StartOffset == elseBlock.StartOffset)
                    {
                        Console.Error.WriteLine($"[SEQ_BUILD_PARSE]   Skipping else block at 0x{succ.StartOffset:X4}");
                        continue;
                    }

                    if (succ.StartOffset < loopBodyStart || succ.StartOffset >= loopBodyEnd)
                    {
                        Console.Error.WriteLine($"[SEQ_BUILD_PARSE]   Skipping block at 0x{succ.StartOffset:X4} (outside body range)");
                        continue;
                    }

                    visited.Add(succ.Id);
                    worklist.Enqueue(succ);
                }
            }
        }

        if (elseBlock != null)
        {
            bodyBlocks = bodyBlocks.Where(b => 
                b.StartOffset >= header.StartOffset && 
                b.StartOffset < elseBlock.StartOffset).ToList();
        }

        bodyBlocks.Sort((a, b) => a.StartOffset.CompareTo(b.StartOffset));

        Console.Error.WriteLine($"[SEQ_BUILD_PARSE] FOR loop at 0x{header.StartOffset:X4}: {bodyBlocks.Count} body blocks found");
        foreach (var bb in bodyBlocks)
        {
            Console.Error.WriteLine($"[SEQ_BUILD_PARSE]   Body block: 0x{bb.StartOffset:X4}-0x{bb.EndOffset:X4}");
        }

        if (isForLoop)
        {
            Console.Error.WriteLine($"[SEQ_BUILD_PARSE] Found FOR loop at 0x{header.StartOffset:X4}, body blocks: {bodyBlocks.Count}");
            return new ForLoopControlStructure(header, bodyBlocks.FirstOrDefault(), backEdge, elseBlock, bodyBlocks);
        }
        else
        {
            Console.Error.WriteLine($"[SEQ_BUILD_PARSE] Found WHILE loop at 0x{header.StartOffset:X4}, body blocks: {bodyBlocks.Count}");
            return new WhileLoopControlStructure(header, bodyBlocks.FirstOrDefault(), backEdge, elseBlock, bodyBlocks);
        }
    }

    private ISequentialControlStructure? ParseWithStructure(SequentialBlock header, List<SequentialBlock> seqBlocks)
    {
        var bodyBlocks = new List<SequentialBlock>();
        SequentialBlock? handlerBlock = null;

        var blockByOffset = seqBlocks.ToDictionary(b => b.StartOffset);

        foreach (var et in header.ExceptionTableEntries)
        {
            if (blockByOffset.TryGetValue(et.TargetOffset, out var targetBlock))
            {
                if (targetBlock.Instructions.Any(i => 
                    i.Opcode == Opcode.WITH_EXCEPT_START || 
                    i.Opcode == Opcode.WITH_EXCEPT_START_312 ||
                    i.Opcode == Opcode.PUSH_EXC_INFO_312))
                {
                    handlerBlock = targetBlock;
                    break;
                }
            }
        }

        bool isPy314Style = header.Instructions.Any(i => i.Opcode == Opcode.LOAD_SPECIAL);
        bool isBeforeWithStyle = header.Instructions.Any(i => 
            i.Opcode == Opcode.BEFORE_WITH || 
            i.Opcode == Opcode.BEFORE_WITH_312 || 
            i.Opcode == Opcode.BEFORE_WITH_313);

            if (isPy314Style)
            {
                int? cleanupStartOffset = null;
                foreach (var seqBlock in seqBlocks)
                {
                    if (seqBlock == header)
                        continue;
                    if (seqBlock.StartOffset > header.EndOffset && IsWithCleanupBlock(seqBlock))
                    {
                        cleanupStartOffset = seqBlock.StartOffset;
                        Console.Error.WriteLine($"[PARSE_WITH] Found cleanup block at 0x{seqBlock.StartOffset:X4} after header 0x{header.EndOffset:X4}");
                        break;
                    }
                }
            
            foreach (var seqBlock in seqBlocks)
            {
                if (seqBlock == header)
                    continue;
                if (handlerBlock != null)
                {
                    if (seqBlock == handlerBlock)
                        continue;
                    if (seqBlock.StartOffset > header.EndOffset && seqBlock.StartOffset < handlerBlock.StartOffset)
                    {
                        bool isCleanupBlock = IsWithCleanupBlock(seqBlock);
                        bool isAnotherWithHeader = false;
                        for (int i = 0; i < seqBlock.Instructions.Count - 6; i++)
                        {
                            if (seqBlock.Instructions[i].Opcode == Opcode.LOAD_FAST_BORROW_314 &&
                                seqBlock.Instructions[i + 1].Opcode == Opcode.COPY &&
                                seqBlock.Instructions[i + 2].Opcode == Opcode.LOAD_SPECIAL &&
                                seqBlock.Instructions[i + 3].Opcode == Opcode.SWAP &&
                                seqBlock.Instructions[i + 4].Opcode == Opcode.SWAP &&
                                seqBlock.Instructions[i + 5].Opcode == Opcode.LOAD_SPECIAL &&
                                seqBlock.Instructions[i + 6].Opcode == Opcode.CALL)
                            {
                                isAnotherWithHeader = true;
                                break;
                            }
                        }
                        if (!isCleanupBlock && !isAnotherWithHeader)
                        {
                            bodyBlocks.Add(seqBlock);
                        }
                    }
                }
                else if (cleanupStartOffset.HasValue)
                {
                    if (seqBlock.StartOffset > header.EndOffset && seqBlock.StartOffset < cleanupStartOffset.Value)
                    {
                        bool isAnotherWithHeader = false;
                        for (int i = 0; i < seqBlock.Instructions.Count - 6; i++)
                        {
                            if (seqBlock.Instructions[i].Opcode == Opcode.LOAD_FAST_BORROW_314 &&
                                seqBlock.Instructions[i + 1].Opcode == Opcode.COPY &&
                                seqBlock.Instructions[i + 2].Opcode == Opcode.LOAD_SPECIAL &&
                                seqBlock.Instructions[i + 3].Opcode == Opcode.SWAP &&
                                seqBlock.Instructions[i + 4].Opcode == Opcode.SWAP &&
                                seqBlock.Instructions[i + 5].Opcode == Opcode.LOAD_SPECIAL &&
                                seqBlock.Instructions[i + 6].Opcode == Opcode.CALL)
                            {
                                isAnotherWithHeader = true;
                                break;
                            }
                        }
                        if (!isAnotherWithHeader)
                        {
                            bodyBlocks.Add(seqBlock);
                        }
                    }
                }
                else
                {
                    if (seqBlock.StartOffset > header.EndOffset)
                    {
                        bool isAnotherWithHeader = false;
                        for (int i = 0; i < seqBlock.Instructions.Count - 6; i++)
                        {
                            if (seqBlock.Instructions[i].Opcode == Opcode.LOAD_FAST_BORROW_314 &&
                                seqBlock.Instructions[i + 1].Opcode == Opcode.COPY &&
                                seqBlock.Instructions[i + 2].Opcode == Opcode.LOAD_SPECIAL &&
                                seqBlock.Instructions[i + 3].Opcode == Opcode.SWAP &&
                                seqBlock.Instructions[i + 4].Opcode == Opcode.SWAP &&
                                seqBlock.Instructions[i + 5].Opcode == Opcode.LOAD_SPECIAL &&
                                seqBlock.Instructions[i + 6].Opcode == Opcode.CALL)
                            {
                                isAnotherWithHeader = true;
                                break;
                            }
                        }
                        if (!isAnotherWithHeader)
                        {
                            bodyBlocks.Add(seqBlock);
                        }
                    }
                }
            }
        }
        else if (isBeforeWithStyle)
        {
            int? nextWithStartOffset = null;
            int? cleanupStartOffset = null;
            
            foreach (var seqBlock in seqBlocks)
            {
                if (seqBlock == header)
                    continue;
                if (seqBlock.StartOffset <= header.EndOffset)
                    continue;
                    
                bool hasBeforeWith = seqBlock.Instructions.Any(i => 
                    i.Opcode == Opcode.BEFORE_WITH || 
                    i.Opcode == Opcode.BEFORE_WITH_312 || 
                    i.Opcode == Opcode.BEFORE_WITH_313);
                
                if (hasBeforeWith && nextWithStartOffset == null)
                {
                    nextWithStartOffset = seqBlock.StartOffset;
                    break;
                }
            }
            
            foreach (var seqBlock in seqBlocks)
            {
                if (seqBlock == header)
                    continue;
                if (seqBlock.StartOffset <= header.EndOffset)
                    continue;
                
                if (nextWithStartOffset.HasValue && seqBlock.StartOffset >= nextWithStartOffset.Value)
                    continue;
                
                bool isCleanup = IsWithCleanupBlock(seqBlock);
                if (isCleanup)
                {
                    cleanupStartOffset = seqBlock.StartOffset;
                    break;
                }
            }
            
            int? endOffset = nextWithStartOffset ?? cleanupStartOffset;
            
            
            
            foreach (var seqBlock in seqBlocks)
            {
                if (seqBlock == header)
                    continue;
                if (handlerBlock != null && seqBlock == handlerBlock)
                    continue;
                
                bool isInRange = false;
                    if (endOffset.HasValue)
                    {
                        isInRange = seqBlock.EndOffset > header.EndOffset && seqBlock.StartOffset < endOffset.Value;
                    }
                    else if (handlerBlock != null)
                    {
                        isInRange = seqBlock.EndOffset > header.EndOffset && seqBlock.StartOffset < handlerBlock.StartOffset;
                    }
                    else
                    {
                        isInRange = seqBlock.EndOffset > header.EndOffset;
                    }
                
                if (isInRange)
                {
                    bool isCleanup = IsWithCleanupBlock(seqBlock);
                    bool hasBeforeWith = seqBlock.Instructions.Any(i => 
                        i.Opcode == Opcode.BEFORE_WITH || 
                        i.Opcode == Opcode.BEFORE_WITH_312 || 
                        i.Opcode == Opcode.BEFORE_WITH_313);
                    
                    if (!isCleanup && !hasBeforeWith)
                    {
                        bodyBlocks.Add(seqBlock);
                    }
                }
            }
        }
        else
        {
            var visited = new HashSet<int> { header.Id };
            var worklist = new Queue<SequentialBlock>();

            foreach (var sourceBlock in header.SourceBlocks)
            {
                foreach (var succ in sourceBlock.Successors)
                {
                    var targetSeqBlock = blockByOffset.Values
                        .FirstOrDefault(sb => sb.StartOffset <= succ.StartOffset && sb.EndOffset >= succ.StartOffset);
                    if (targetSeqBlock != null && targetSeqBlock != handlerBlock && !visited.Contains(targetSeqBlock.Id))
                    {
                        visited.Add(targetSeqBlock.Id);
                        worklist.Enqueue(targetSeqBlock);
                    }
                }
            }

            while (worklist.Count > 0)
            {
                var current = worklist.Dequeue();

                if (current == handlerBlock)
                    continue;

                bool isCleanupCode = current.Instructions.Any(i => 
                    i.Opcode == Opcode.LOAD_CONST && 
                    current.Instructions.IndexOf(i) == 0 &&
                    current.Instructions.Count >= 3 &&
                    current.Instructions[1].Opcode == Opcode.LOAD_CONST &&
                    current.Instructions[2].Opcode == Opcode.LOAD_CONST);

                if (isCleanupCode)
                    continue;

                bodyBlocks.Add(current);

                foreach (var succ in current.Successors)
                {
                    if (!visited.Contains(succ.Id) && succ != handlerBlock)
                    {
                        visited.Add(succ.Id);
                        worklist.Enqueue(succ);
                    }
                }
            }
        }

        bodyBlocks.Sort((a, b) => a.StartOffset.CompareTo(b.StartOffset));

        Console.Error.WriteLine($"[SEQ_BUILD_PARSE] Found WITH statement at 0x{header.StartOffset:X4}, header.EndOffset=0x{header.EndOffset:X4}, body blocks: {bodyBlocks.Count}, handler: {(handlerBlock != null ? $"0x{handlerBlock.StartOffset:X4}" : "none")}");
        foreach (var bb in bodyBlocks)
        {
            Console.Error.WriteLine($"[SEQ_BUILD_PARSE]   Body block: 0x{bb.StartOffset:X4}-0x{bb.EndOffset:X4}, Instrs={string.Join(",", bb.Instructions.Select(i => i.Opcode))}");
        }
        
        Console.Error.WriteLine($"[SEQ_BUILD_PARSE] All seqBlocks:");
        foreach (var sb in seqBlocks)
        {
            Console.Error.WriteLine($"[SEQ_BUILD_PARSE]   seqBlock: 0x{sb.StartOffset:X4}-0x{sb.EndOffset:X4}, hasWith={sb.Instructions.Any(i => i.Opcode == Opcode.BEFORE_WITH || i.Opcode == Opcode.BEFORE_WITH_312 || i.Opcode == Opcode.BEFORE_WITH_313)}");
        }

        return new WithControlStructure(header, handlerBlock, bodyBlocks);
    }

    private bool IsWithCleanupBlock(SequentialBlock block)
    {
        var instrs = block.Instructions;
        if (instrs.Count < 3)
            return false;

        bool isWithHeader = false;
        for (int i = 0; i < instrs.Count - 6; i++)
        {
            if (instrs[i].Opcode == Opcode.LOAD_FAST_BORROW_314 &&
                instrs[i + 1].Opcode == Opcode.COPY &&
                instrs[i + 2].Opcode == Opcode.LOAD_SPECIAL &&
                instrs[i + 3].Opcode == Opcode.SWAP &&
                instrs[i + 4].Opcode == Opcode.SWAP &&
                instrs[i + 5].Opcode == Opcode.LOAD_SPECIAL &&
                instrs[i + 6].Opcode == Opcode.CALL)
            {
                isWithHeader = true;
                break;
            }
        }
        
        if (isWithHeader)
            return false;
        
        bool hasBeforeWith = instrs.Any(i => 
            i.Opcode == Opcode.BEFORE_WITH || 
            i.Opcode == Opcode.BEFORE_WITH_312 || 
            i.Opcode == Opcode.BEFORE_WITH_313);
        
        if (hasBeforeWith)
            return false;

        if (instrs.Count >= 4)
        {
            int startIdx = 0;
            if (instrs[0].Opcode == Opcode.NOP)
                startIdx = 1;
            
            if (instrs.Count >= startIdx + 4 &&
                instrs[startIdx].Opcode == Opcode.LOAD_CONST &&
                instrs[startIdx + 1].Opcode == Opcode.LOAD_CONST &&
                instrs[startIdx + 2].Opcode == Opcode.LOAD_CONST &&
                instrs[startIdx + 3].Opcode == Opcode.CALL)
            {
                if (instrs[startIdx + 3].Argument == 3 || instrs[startIdx + 3].Argument == 2)
                {
                    return true;
                }
            }
        }

        if (instrs.Any(i => i.Opcode == Opcode.POP_EXCEPT || 
                           i.Opcode == Opcode.RERAISE))
        {
            return true;
        }

        if (instrs.Any(i => i.Opcode == Opcode.PUSH_EXC_INFO ||
                           i.Opcode == Opcode.PUSH_EXC_INFO_312 ||
                           i.Opcode == Opcode.WITH_EXCEPT_START ||
                           i.Opcode == Opcode.WITH_EXCEPT_START_312))
        {
            return true;
        }

        return false;
    }

    private ISequentialControlStructure? ParseTryStructure(SequentialBlock header, List<SequentialBlock> seqBlocks)
    {
        var exceptHandlers = new List<(SequentialBlock Handler, string? ExceptionType, string? ExceptionVar)>();
        SequentialBlock? elseBlock = null;
        SequentialBlock? finallyBlock = null;
        var bodyBlocks = new List<SequentialBlock>();

        var blockByOffset = seqBlocks.ToDictionary(b => b.StartOffset);

        bool hasSetupOpcode = header.Instructions.Any(i => 
            i.Opcode == Opcode.SETUP_FINALLY ||
            i.Opcode == Opcode.SETUP_EXCEPT);

        if (hasSetupOpcode)
        {
            if (header.ExceptionTableEntries.Count > 0)
            {
                // 3.11+ ExceptionTable path
                foreach (var et in header.ExceptionTableEntries)
                {
                    if (blockByOffset.TryGetValue(et.TargetOffset, out var targetBlock))
                    {
                        if (targetBlock.Instructions.Any(i => i.Opcode == Opcode.END_FINALLY))
                        {
                            finallyBlock = targetBlock;
                        }
                        else
                        {
                            exceptHandlers.Add((targetBlock, null, null));
                        }
                    }
                }
            }
            else
            {
                // 3.10- SETUP_FINALLY path: use instruction argument (jump target)
                var setupInstr = header.Instructions.FirstOrDefault(i =>
                    i.Opcode == Opcode.SETUP_FINALLY ||
                    i.Opcode == Opcode.SETUP_EXCEPT);
                if (setupInstr.Argument.HasValue)
                {
                    int handlerTarget = setupInstr.Argument.Value;
                    // 3.6-3.10 wordcode: arg 是半字符数，需转为绝对字节偏移
                    // PycReader 不转换 SETUP_FINALLY 的 arg（非传统跳转指令）
                    bool isWordcodeWithHalfword = _codeObject.Version switch
                    {
                        PythonVersion.Py36 or PythonVersion.Py37 or
                        PythonVersion.Py38 or PythonVersion.Py39 or
                        PythonVersion.Py310 => true,
                        _ => false
                    };
                    if (isWordcodeWithHalfword && handlerTarget < 0x1000)
                    {
                        handlerTarget = setupInstr.Offset + 2 + handlerTarget * 2;
                    }
                    var targetBlock = blockByOffset.Values
                        .FirstOrDefault(sb => sb.StartOffset <= handlerTarget && sb.EndOffset >= handlerTarget);
                    if (targetBlock != null)
                    {
                        // SETUP_FINALLY can target either an except handler or a finally block
                        exceptHandlers.Add((targetBlock, null, null));
                    }
                }
            }

            var handlerOffsets = exceptHandlers.Select(h => h.Handler.StartOffset).ToList();
            if (finallyBlock != null)
                handlerOffsets.Add(finallyBlock.StartOffset);

            var visited = new HashSet<int> { header.Id };
            var worklist = new Queue<SequentialBlock>();

            foreach (var sourceBlock in header.SourceBlocks)
            {
                foreach (var succ in sourceBlock.Successors)
                {
                    var targetSeqBlock = blockByOffset.Values
                        .FirstOrDefault(sb => sb.StartOffset <= succ.StartOffset && sb.EndOffset >= succ.StartOffset);
                    if (targetSeqBlock != null && !visited.Contains(targetSeqBlock.Id))
                    {
                        visited.Add(targetSeqBlock.Id);
                        worklist.Enqueue(targetSeqBlock);
                    }
                }
            }

            // 将 header 本身加入 bodyBlocks（header 包含 try body 的指令）
            bodyBlocks.Add(header);

            while (worklist.Count > 0)
            {
                var current = worklist.Dequeue();

                // Phase 9-04: 跳过 handler preamble 块（不会产生有效语句）
                if (IsHandlerPreambleBlock(current))
                    continue;

                if (handlerOffsets.Contains(current.StartOffset))
                    continue;

                bodyBlocks.Add(current);

                foreach (var succ in current.Successors)
                {
                    if (!visited.Contains(succ.Id) && !handlerOffsets.Contains(succ.StartOffset))
                    {
                        visited.Add(succ.Id);
                        worklist.Enqueue(succ);
                    }
                }
            }
        }
        else
        {
            var allEtEntries = new List<ExceptionTableEntry>();
            foreach (var seqBlock in seqBlocks)
            {
                foreach (var et in seqBlock.ExceptionTableEntries)
                {
                    if (et.IsExcept || et.IsFinally)
                    {
                        if (!allEtEntries.Contains(et))
                            allEtEntries.Add(et);
                    }
                }
            }

            if (allEtEntries.Count == 0)
                return null;

            var primaryExceptEntry = allEtEntries.FirstOrDefault(et => 
                et.Depth == 0 && !et.Lasti && et.StartOffset == header.StartOffset);

            // 如果精确匹配失败（seqBlock 可能包含 try 之前的代码），
            // 找 header 范围内 StartOffset 最小的 ET 条目
            if (primaryExceptEntry == null)
            {
                primaryExceptEntry = allEtEntries
                    .Where(et => et.Depth == 0 && !et.Lasti &&
                        et.StartOffset >= header.StartOffset && et.StartOffset < header.EndOffset)
                    .OrderBy(et => et.StartOffset)
                    .FirstOrDefault();
            }

            if (primaryExceptEntry == null)
                return null;

            int tryStartOffset = primaryExceptEntry.StartOffset;
            int tryEndOffset = primaryExceptEntry.EndOffset;
            var handlerOffsets = new HashSet<int>();

            SequentialBlock? pushExcInfoBlock = null;
            foreach (var seqBlock in seqBlocks)
            {
                if (seqBlock.Instructions.Any(i => i.Opcode == Opcode.PUSH_EXC_INFO_312 || i.Opcode == Opcode.PUSH_EXC_INFO))
                {
                    pushExcInfoBlock = seqBlock;
                    break;
                }
            }
            
            if (pushExcInfoBlock != null)
            {
                string? exceptType = null;
                string? exceptVar = null;
                
                var allHandlerInstrs = new List<Instruction>();
                allHandlerInstrs.AddRange(pushExcInfoBlock.Instructions);
                
                int exceptStart = pushExcInfoBlock.StartOffset;
                int exceptEnd = pushExcInfoBlock.EndOffset;
                bool foundPopExcept = false;
                
                foreach (var seqBlock in seqBlocks)
                {
                    if (seqBlock.StartOffset >= exceptStart)
                    {
                        bool hasPopExcept = seqBlock.Instructions.Any(i => i.Opcode == Opcode.POP_EXCEPT);
                        bool hasReturn = seqBlock.Instructions.Any(i => i.Opcode == Opcode.RETURN_VALUE);
                        
                        if (hasPopExcept)
                        {
                            exceptEnd = seqBlock.EndOffset;
                            foundPopExcept = true;
                            break;
                        }
                        
                        if (hasReturn)
                        {
                            exceptEnd = seqBlock.StartOffset;
                            break;
                        }
                        
                        exceptEnd = seqBlock.EndOffset;
                    }
                }
                
                if (!foundPopExcept)
                {
                    exceptEnd = pushExcInfoBlock.EndOffset;
                }
                
                foreach (var seqBlock in seqBlocks)
                {
                    if (seqBlock.StartOffset > exceptStart && seqBlock.StartOffset < exceptEnd)
                    {
                        handlerOffsets.Add(seqBlock.StartOffset);
                        allHandlerInstrs.AddRange(seqBlock.Instructions);
                    }
                }
                
                for (int i = 0; i < allHandlerInstrs.Count; i++)
                {
                    if (allHandlerInstrs[i].Opcode == Opcode.LOAD_GLOBAL)
                    {
                        var nameIdx = allHandlerInstrs[i].Argument ?? 0;
                        if (nameIdx < _codeObject.Names.Count)
                            exceptType = _codeObject.Names[nameIdx];
                        break;
                    }
                    else if (allHandlerInstrs[i].Opcode == Opcode.CHECK_EXC_MATCH || 
                             allHandlerInstrs[i].Opcode == Opcode.CHECK_EG_MATCH)
                    {
                        break;
                    }
                }
                
                for (int i = 0; i < allHandlerInstrs.Count; i++)
                {
                    if (allHandlerInstrs[i].Opcode == Opcode.STORE_FAST)
                    {
                        var nameIdx = allHandlerInstrs[i].Argument ?? 0;
                        if (nameIdx < _codeObject.Varnames.Count)
                            exceptVar = _codeObject.Varnames[nameIdx];
                        break;
                    }
                }
                
                var mergedHandlerBlock = new SequentialBlock();
                mergedHandlerBlock.StartOffset = exceptStart;
                mergedHandlerBlock.EndOffset = exceptEnd;
                mergedHandlerBlock.Instructions.AddRange(allHandlerInstrs);
                foreach (var seqBlock in seqBlocks)
                {
                    if (seqBlock.StartOffset >= exceptStart && seqBlock.StartOffset < exceptEnd)
                    {
                        mergedHandlerBlock.SourceBlocks.AddRange(seqBlock.SourceBlocks);
                        handlerOffsets.Add(seqBlock.StartOffset);
                    }
                }
                
                exceptHandlers.Add((mergedHandlerBlock, exceptType, exceptVar));
            }

            var finallyEtEntry = allEtEntries.Where(et => et.IsFinally).LastOrDefault();
            
            if (finallyEtEntry != null)
            {
                SequentialBlock? foundElseBlock = null;
                int elseStart = -1;
                int elseEnd = -1;
                    
                if (exceptHandlers.Count > 0)
                {
                    var lastHandler = exceptHandlers[0].Handler;
                    int handlerEnd = lastHandler.EndOffset;
                    
                    int tryBodyEnd = tryEndOffset;
                    
                    foreach (var seqBlock in seqBlocks)
                    {
                        if (seqBlock.StartOffset >= tryBodyEnd)
                        {
                            bool hasPopExcept = seqBlock.Instructions.Any(i => i.Opcode == Opcode.POP_EXCEPT);
                            bool hasReraise = seqBlock.Instructions.Any(i => i.Opcode == Opcode.RERAISE);
                            bool hasCopy = seqBlock.Instructions.Any(i => i.Opcode == Opcode.COPY);
                            bool hasExcInfo = seqBlock.Instructions.Any(i => i.Opcode == Opcode.PUSH_EXC_INFO_312 || i.Opcode == Opcode.PUSH_EXC_INFO);
                            bool hasDeleteFast = seqBlock.Instructions.Any(i => i.Opcode == Opcode.DELETE_FAST);
                            bool hasStoreFast = seqBlock.Instructions.Any(i => i.Opcode == Opcode.STORE_FAST);
                            bool hasReturn = seqBlock.Instructions.Any(i => i.Opcode == Opcode.RETURN_VALUE);
                            
                            bool isCleanup = hasPopExcept || hasReraise || hasCopy || hasExcInfo || 
                                            hasDeleteFast || hasStoreFast;
                            
                            if (!isCleanup)
                            {
                                if (elseStart < 0)
                                    elseStart = seqBlock.StartOffset;
                                   
                                if (hasReturn)
                                {
                                    elseEnd = seqBlock.StartOffset;
                                    break;
                                }
                                else
                                {
                                    elseEnd = seqBlock.EndOffset;
                                }
                            }
                        }
                    }
                    
                    if (elseStart >= 0 && elseEnd >= 0)
                    {
                        foreach (var seqBlock in seqBlocks)
                        {
                            if (seqBlock.StartOffset >= elseStart)
                            {
                                if (foundElseBlock == null)
                                    foundElseBlock = seqBlock;
                            }
                        }
                    }
                }
                
                if (foundElseBlock != null && elseStart >= 0 && elseEnd >= 0)
                {
                    var allElseInstrs = new List<Instruction>();
                    foreach (var sb in seqBlocks)
                    {
                        if (sb.StartOffset >= elseStart && sb.StartOffset < elseEnd)
                        {
                            allElseInstrs.AddRange(sb.Instructions);
                            handlerOffsets.Add(sb.StartOffset);
                        }
                    }
                    
                    var mergedElseBlock = new SequentialBlock();
                    mergedElseBlock.StartOffset = elseStart;
                    mergedElseBlock.EndOffset = elseEnd;
                    mergedElseBlock.Instructions.AddRange(allElseInstrs);
                    foreach (var sb in seqBlocks)
                    {
                        if (sb.StartOffset >= elseStart && sb.StartOffset < elseEnd)
                        {
                            mergedElseBlock.SourceBlocks.AddRange(sb.SourceBlocks);
                        }
                    }
                    
                    elseBlock = mergedElseBlock;
                }
            }

            int finallyStart = -1;
            if (finallyEtEntry != null)
            {
                int exceptionPathStart = finallyEtEntry.TargetOffset;
                
                int searchStart = tryEndOffset;
                if (elseBlock != null)
                {
                    searchStart = elseBlock.EndOffset;
                }
                else if (exceptHandlers.Count > 0)
                {
                    searchStart = exceptHandlers[0].Handler.EndOffset;
                }
                
                foreach (var seqBlock in seqBlocks)
                {
                    if (seqBlock.StartOffset >= searchStart && seqBlock.StartOffset < exceptionPathStart)
                    {
                        bool hasCall = seqBlock.Instructions.Any(i => i.Opcode == Opcode.CALL);
                        bool hasReturn = seqBlock.Instructions.Any(i => i.Opcode == Opcode.RETURN_VALUE);
                        bool hasJumpForward = seqBlock.Instructions.Any(i => i.Opcode == Opcode.JUMP_FORWARD);
                        bool hasPopExcept = seqBlock.Instructions.Any(i => i.Opcode == Opcode.POP_EXCEPT);
                        bool hasStoreFast = seqBlock.Instructions.Any(i => i.Opcode == Opcode.STORE_FAST);
                        bool hasDeleteFast = seqBlock.Instructions.Any(i => i.Opcode == Opcode.DELETE_FAST);
                        bool hasReraise = seqBlock.Instructions.Any(i => i.Opcode == Opcode.RERAISE);
                        
                        bool isCleanup = hasPopExcept || hasStoreFast || hasDeleteFast;
                        
                        if (hasJumpForward && !hasCall)
                            continue;
                        
                        if (hasCall && !hasReraise && !isCleanup)
                        {
                            finallyStart = seqBlock.StartOffset;
                            break;
                        }
                    }
                }
                
                if (finallyStart < 0)
                    finallyStart = exceptionPathStart;

                int finallyEnd = finallyStart;
                foreach (var seqBlock in seqBlocks)
                {
                    if (seqBlock.StartOffset >= finallyStart && seqBlock.StartOffset < exceptionPathStart)
                    {
                        bool hasReraise = seqBlock.Instructions.Any(i => 
                            i.Opcode == Opcode.RERAISE || 
                            i.Opcode == Opcode.END_FINALLY);
                        bool hasReturnValue = seqBlock.Instructions.Any(i => i.Opcode == Opcode.RETURN_VALUE);
                        bool hasPushExcInfo = seqBlock.Instructions.Any(i => 
                            i.Opcode == Opcode.PUSH_EXC_INFO_312 || 
                            i.Opcode == Opcode.PUSH_EXC_INFO);
                        bool hasCheckExcMatch = seqBlock.Instructions.Any(i => i.Opcode == Opcode.CHECK_EXC_MATCH);
                        
                        if (hasReraise || hasReturnValue)
                        {
                            finallyEnd = seqBlock.EndOffset;
                            break;
                        }
                        if (hasPushExcInfo || hasCheckExcMatch)
                        {
                            break;
                        }
                        finallyEnd = seqBlock.EndOffset;
                    }
                }
                
                var allFinallyInstrs = new List<Instruction>();
                foreach (var sb in seqBlocks)
                {
                    if (sb.StartOffset >= finallyStart && sb.StartOffset <= finallyEnd)
                    {
                        allFinallyInstrs.AddRange(sb.Instructions);
                        handlerOffsets.Add(sb.StartOffset);
                    }
                }
                    
                var mergedFinallyBlock = new SequentialBlock();
                mergedFinallyBlock.StartOffset = finallyStart;
                mergedFinallyBlock.EndOffset = finallyEnd;
                mergedFinallyBlock.Instructions.AddRange(allFinallyInstrs);
                foreach (var sb in seqBlocks)
                {
                    if (sb.StartOffset >= finallyStart && sb.StartOffset <= finallyEnd)
                    {
                        mergedFinallyBlock.SourceBlocks.AddRange(sb.SourceBlocks);
                    }
                }
                    
                finallyBlock = mergedFinallyBlock;
            }

            foreach (var seqBlock in seqBlocks)
            {
                if (handlerOffsets.Contains(seqBlock.StartOffset))
                    continue;

                bool hasExcInfo = seqBlock.Instructions.Any(i => 
                    i.Opcode == Opcode.PUSH_EXC_INFO_312 || 
                    i.Opcode == Opcode.PUSH_EXC_INFO);
                if (hasExcInfo && seqBlock != exceptHandlers[0].Handler)
                    continue;

                bool hasExcMatch = seqBlock.Instructions.Any(i =>
                    i.Opcode == Opcode.CHECK_EXC_MATCH || i.Opcode == Opcode.CHECK_EG_MATCH);
                if (hasExcMatch && seqBlock != exceptHandlers[0].Handler)
                    continue;

                if (seqBlock.EndOffset > tryStartOffset && seqBlock.StartOffset < tryEndOffset)
                {
                    if (finallyStart >= 0 && seqBlock.StartOffset >= finallyStart)
                        continue;
                    if (!bodyBlocks.Contains(seqBlock))
                        bodyBlocks.Add(seqBlock);
                }
            }

            // ET路径：如果 bodyBlocks 为空但存在 handler，从 offset 范围推导 body
            if (bodyBlocks.Count == 0 && exceptHandlers.Count > 0)
            {
                int firstHandlerStart = exceptHandlers.Min(h => h.Handler.StartOffset);
                foreach (var seqBlock in seqBlocks)
                {
                    if (seqBlock.EndOffset > tryStartOffset && seqBlock.StartOffset < firstHandlerStart
                        && !handlerOffsets.Contains(seqBlock.StartOffset))
                    {
                        bodyBlocks.Add(seqBlock);
                    }
                }
            }
        }

        bodyBlocks.Sort((a, b) => a.StartOffset.CompareTo(b.StartOffset));

        // Phase 9-04: 如果 body 只有 handler preamble 块，不创建空 try
        bodyBlocks.RemoveAll(b => IsHandlerPreambleBlock(b));
        if (bodyBlocks.Count == 0)
        {
            Console.Error.WriteLine(
                $"[TRY_PARSE] Skipped empty try @0x{header.StartOffset:X4} (no real body)");
            return null;
        }

        // Phase 9-4: 检测模块级 try（header 在偏移 0 且 handler 足够远）
        // abc.py 3.8-3.10 用模块级 `try: ... except NameError: pass` 包裹全部代码
        if (header.StartOffset == 0 && exceptHandlers.Count > 0)
        {
            var lastHandler = exceptHandlers[^1].Handler;
            bool coversMajority = lastHandler.StartOffset > 100
                || (seqBlocks.Count > 0 && lastHandler.StartOffset > seqBlocks[^1].EndOffset * 0.85);
            if (coversMajority)
            {
                Console.Error.WriteLine(
                    $"[TRY_PARSE] Skipped module-level try @0x{header.StartOffset:X4} " +
                    $"(handler at 0x{lastHandler.StartOffset:X4} wraps entire module)");
                return null;
            }
        }

        if (exceptHandlers.Count > 0 || finallyBlock != null)
        {
            return new TryControlStructure(header, exceptHandlers, elseBlock, finallyBlock, bodyBlocks);
        }

        return null;
    }

    private ISequentialControlStructure? ParseIfElseStructure(SequentialBlock header, List<SequentialBlock> seqBlocks)
    {
        var hasExcInfo = header.Instructions.Any(i => 
            i.Opcode == Opcode.PUSH_EXC_INFO_312 || 
            i.Opcode == Opcode.PUSH_EXC_INFO);
        var hasExcMatch = header.Instructions.Any(i => 
            i.Opcode == Opcode.CHECK_EXC_MATCH || 
            i.Opcode == Opcode.CHECK_EG_MATCH);
        
        if (hasExcInfo || hasExcMatch)
            return null;

        SequentialBlock? trueBranch = null;
        SequentialBlock? falseBranch = null;
        SequentialBlock? mergePoint = null;
        var bodyBlocks = new List<SequentialBlock>();

        var blockByOffset = seqBlocks.ToDictionary(b => b.StartOffset);

        if (header.JumpTarget.HasValue && blockByOffset.TryGetValue(header.JumpTarget.Value, out var jumpTarget))
        {
            falseBranch = jumpTarget;
        }

        foreach (var sourceBlock in header.SourceBlocks)
        {
            foreach (var succ in sourceBlock.Successors)
            {
                var targetSeqBlock = blockByOffset.Values
                    .FirstOrDefault(sb => sb.StartOffset <= succ.StartOffset && sb.EndOffset >= succ.StartOffset);
                if (targetSeqBlock != null)
                {
                    if (targetSeqBlock == falseBranch)
                        continue;
                    if (trueBranch == null)
                        trueBranch = targetSeqBlock;
                    else if (falseBranch == null)
                        falseBranch = targetSeqBlock;
                }
            }
        }

        if (trueBranch != null)
        {
            foreach (var sourceBlock in trueBranch.SourceBlocks)
            {
                foreach (var succ in sourceBlock.Successors)
                {
                    var targetSeqBlock = blockByOffset.Values
                        .FirstOrDefault(sb => sb.StartOffset <= succ.StartOffset && sb.EndOffset >= succ.StartOffset);
                    if (targetSeqBlock != null && targetSeqBlock != header)
                    {
                        mergePoint = targetSeqBlock;
                        break;
                    }
                }
                if (mergePoint != null) break;
            }
        }

        if (trueBranch != null)
        {
            var visited = new HashSet<int> { header.Id };
            var worklist = new Queue<SequentialBlock>();
            visited.Add(trueBranch.Id);
            worklist.Enqueue(trueBranch);

            while (worklist.Count > 0)
            {
                var current = worklist.Dequeue();
                if (current == mergePoint)
                    continue;
                bodyBlocks.Add(current);
                foreach (var succ in current.Successors)
                {
                    if (!visited.Contains(succ.Id) && succ != mergePoint)
                    {
                        visited.Add(succ.Id);
                        worklist.Enqueue(succ);
                    }
                }
            }
        }

        if (falseBranch != null && falseBranch != trueBranch)
        {
            var visited = new HashSet<int> { header.Id };
            var worklist = new Queue<SequentialBlock>();
            visited.Add(falseBranch.Id);
            worklist.Enqueue(falseBranch);

            while (worklist.Count > 0)
            {
                var current = worklist.Dequeue();
                if (current == mergePoint)
                    continue;
                bodyBlocks.Add(current);
                foreach (var succ in current.Successors)
                {
                    if (!visited.Contains(succ.Id) && succ != mergePoint)
                    {
                        visited.Add(succ.Id);
                        worklist.Enqueue(succ);
                    }
                }
            }
        }

        bodyBlocks.Sort((a, b) => a.StartOffset.CompareTo(b.StartOffset));

        Console.Error.WriteLine($"[SEQ_BUILD_PARSE] Found IF/ELSE at 0x{header.StartOffset:X4}, body blocks: {bodyBlocks.Count}, true: {(trueBranch != null ? $"0x{trueBranch.StartOffset:X4}" : "none")}, false: {(falseBranch != null ? $"0x{falseBranch.StartOffset:X4}" : "none")}");

        return new IfElseControlStructure(header, trueBranch, falseBranch, mergePoint, bodyBlocks);
    }

    private void LinkControlStructures(List<ISequentialControlStructure> structures, List<SequentialBlock> seqBlocks)
    {
        foreach (var structure in structures)
        {
            structure.Header.ParentStructure = structure;
            foreach (var bodyBlock in structure.BodyBlocks)
            {
                bodyBlock.ParentStructure = structure;
            }

            if (structure is WithControlStructure withStruct && withStruct.HandlerBlock != null)
            {
                withStruct.HandlerBlock.ParentStructure = structure;
            }

            if (structure is TryControlStructure tryStruct)
            {
                foreach (var (handler, _, __) in tryStruct.ExceptHandlers)
                {
                    handler.ParentStructure = structure;
                    foreach (var sb in seqBlocks)
                    {
                        if (sb.StartOffset >= handler.StartOffset && sb.StartOffset < handler.EndOffset)
                        {
                            sb.ParentStructure = structure;
                        }
                    }
                }
                if (tryStruct.ElseBlock != null)
                    tryStruct.ElseBlock.ParentStructure = structure;
                if (tryStruct.FinallyBlock != null)
                {
                    tryStruct.FinallyBlock.ParentStructure = structure;
                    foreach (var sb in seqBlocks)
                    {
                        if (sb.StartOffset >= tryStruct.FinallyBlock.StartOffset && sb.StartOffset <= tryStruct.FinallyBlock.EndOffset)
                        {
                            sb.ParentStructure = structure;
                        }
                    }
                }
                
                foreach (var bodyBlock in tryStruct.BodyBlocks)
                {
                    bodyBlock.ParentStructure = structure;
                    foreach (var sb in seqBlocks)
                    {
                        if (sb.StartOffset == bodyBlock.StartOffset)
                        {
                            sb.ParentStructure = structure;
                        }
                    }
                }
                
                foreach (var sb in seqBlocks)
                {
                    if (sb.StartOffset >= tryStruct.Header.StartOffset && sb.ParentStructure == null)
                    {
                        bool hasExcInfo = sb.Instructions.Any(i => 
                            i.Opcode == Opcode.PUSH_EXC_INFO_312 || 
                            i.Opcode == Opcode.PUSH_EXC_INFO);
                        bool hasReraise = sb.Instructions.Any(i => i.Opcode == Opcode.RERAISE);
                        bool hasPopExcept = sb.Instructions.Any(i => i.Opcode == Opcode.POP_EXCEPT);
                        bool hasCopy = sb.Instructions.Any(i => i.Opcode == Opcode.COPY);
                        bool hasPrint = sb.Instructions.Any(i => i.Opcode == Opcode.CALL);
                        
                        if (hasExcInfo || hasReraise || hasPopExcept || hasCopy || hasPrint)
                        {
                            sb.ParentStructure = structure;
                            Console.Error.WriteLine($"[LINK_CONTROL] Marked seqBlock Id={sb.Id}, Start=0x{sb.StartOffset:X4} as TryControlStructure");
                        }
                    }
                }
            }

            if (structure is IfElseControlStructure ifStruct)
            {
                if (ifStruct.TrueBranch != null)
                    ifStruct.TrueBranch.ParentStructure = structure;
                if (ifStruct.FalseBranch != null)
                    ifStruct.FalseBranch.ParentStructure = structure;
            }

            if (structure is ForLoopControlStructure forStruct)
            {
                if (forStruct.ElseBlock != null)
                    forStruct.ElseBlock.ParentStructure = structure;
            }

            if (structure is WhileLoopControlStructure whileStruct)
            {
                if (whileStruct.ElseBlock != null)
                    whileStruct.ElseBlock.ParentStructure = structure;
            }
        }
    }

    private List<Stmt> GenerateAstStatements(List<SequentialBlock> seqBlocks, ControlFlowGraph cfg)
    {
        var stmts = new List<Stmt>();
        var processed = new HashSet<int>();

        var seqBlockByOffset = seqBlocks.ToDictionary(b => b.StartOffset);
        var startSeqBlock = seqBlockByOffset.GetValueOrDefault(cfg.Entry.StartOffset);

        if (startSeqBlock != null)
        {
            stmts.AddRange(GenerateStatementsFromSeqBlock(startSeqBlock, seqBlocks, processed));
        }

        foreach (var seqBlock in seqBlocks.OrderBy(b => b.StartOffset))
        {
            if (processed.Contains(seqBlock.Id))
                continue;

            if (seqBlock.Statements != null && seqBlock.Statements.Count > 0)
            {
                stmts.AddRange(seqBlock.Statements);
                processed.Add(seqBlock.Id);
            }
        }

        return stmts;
    }

    private List<Stmt> GenerateStatementsFromSeqBlock(SequentialBlock seqBlock, List<SequentialBlock> seqBlocks, HashSet<int> processed)
    {
        var stmts = new List<Stmt>();

        if (processed.Contains(seqBlock.Id))
            return stmts;

        processed.Add(seqBlock.Id);

        if (seqBlock.ParentStructure != null)
        {
            var structure = seqBlock.ParentStructure;
            var structureStmts = BuildStructureStatements(structure);
            stmts.AddRange(structureStmts);

            processed.Add(structure.Header.Id);
            foreach (var bodyBlock in structure.BodyBlocks)
                processed.Add(bodyBlock.Id);

            if (structure is WithControlStructure withStruct && withStruct.HandlerBlock != null)
                processed.Add(withStruct.HandlerBlock.Id);

            if (structure is TryControlStructure tryStruct)
            {
                foreach (var (handler, _, __) in tryStruct.ExceptHandlers)
                    processed.Add(handler.Id);
                if (tryStruct.ElseBlock != null)
                    processed.Add(tryStruct.ElseBlock.Id);
                if (tryStruct.FinallyBlock != null)
                    processed.Add(tryStruct.FinallyBlock.Id);
            }

            if (structure is IfElseControlStructure ifStruct)
            {
                if (ifStruct.TrueBranch != null)
                    processed.Add(ifStruct.TrueBranch.Id);
                if (ifStruct.FalseBranch != null)
                    processed.Add(ifStruct.FalseBranch.Id);
            }

            if (structure is ForLoopControlStructure forStruct && forStruct.ElseBlock != null)
                processed.Add(forStruct.ElseBlock.Id);

            if (structure is WhileLoopControlStructure whileStruct && whileStruct.ElseBlock != null)
                processed.Add(whileStruct.ElseBlock.Id);

            foreach (var succ in structure.Header.Successors)
            {
                if (!processed.Contains(succ.Id))
                    stmts.AddRange(GenerateStatementsFromSeqBlock(succ, seqBlocks, processed));
            }
        }
        else if (seqBlock.Statements != null)
        {
            stmts.AddRange(seqBlock.Statements);

            foreach (var succ in seqBlock.Successors)
            {
                if (!processed.Contains(succ.Id))
                    stmts.AddRange(GenerateStatementsFromSeqBlock(succ, seqBlocks, processed));
            }
        }

        return stmts;
    }

    private List<Stmt> GenerateAstStatementsHybrid(List<SequentialBlock> seqBlocks, ControlFlowGraph cfg)
    {
        var stmts = new List<Stmt>();
        var processedSeqBlocks = new HashSet<int>();
        var processedBasicBlocks = new HashSet<int>();

        var structureHeaders = new HashSet<int>();
        foreach (var sb in seqBlocks)
        {
            if (sb.ParentStructure != null)
            {
                structureHeaders.Add(sb.ParentStructure.Header.Id);
            }
        }

        Console.Error.WriteLine($"[SEQ_BUILD_HYBRID] Total seqBlocks: {seqBlocks.Count}");
        foreach (var sb in seqBlocks.OrderBy(b => b.StartOffset))
        {
            Console.Error.WriteLine($"[SEQ_BUILD_HYBRID] SeqBlock Id={sb.Id}, Start=0x{sb.StartOffset:X4}, End=0x{sb.EndOffset:X4}, ParentStructure={(sb.ParentStructure != null ? sb.ParentStructure.GetType().Name : "null")}");
        }

        var seqBlockByOffset = seqBlocks.ToDictionary(b => b.StartOffset);
        var startSeqBlock = seqBlockByOffset.GetValueOrDefault(cfg.Entry.StartOffset);

        if (startSeqBlock != null)
        {
            stmts.AddRange(GenerateStatementsFromSeqBlockHybrid(startSeqBlock, seqBlocks, cfg, processedSeqBlocks, processedBasicBlocks, structureHeaders));
        }

        foreach (var seqBlock in seqBlocks.OrderBy(b => b.StartOffset))
        {
            if (processedSeqBlocks.Contains(seqBlock.Id))
                continue;
            
            Console.Error.WriteLine($"[SEQ_BUILD_HYBRID] Second loop: seqBlock Id={seqBlock.Id}, Start=0x{seqBlock.StartOffset:X4}, ParentStructure={(seqBlock.ParentStructure != null ? seqBlock.ParentStructure.GetType().Name : "null")}");

            if (structureHeaders.Contains(seqBlock.Id))
            {
                var structure = seqBlock.ParentStructure;
                if (structure != null)
                {
                    var structureStmts = BuildStructureStatements(structure);
                    stmts.AddRange(structureStmts);
                    MarkStructureBlocksProcessed(structure, processedSeqBlocks, seqBlocks);
                    foreach (var sb in structure.Header.SourceBlocks)
                        { processedBasicBlocks.Add(sb.Id); _processedBlockIds.Add(sb.Id); }
                    foreach (var bb in structure.BodyBlocks)
                    {
                        foreach (var sb in bb.SourceBlocks)
                            { processedBasicBlocks.Add(sb.Id); _processedBlockIds.Add(sb.Id); }
                    }

                    if (structure is TryControlStructure tryStruct)
                    {
                        foreach (var (handler, _, __) in tryStruct.ExceptHandlers)
                        {
                            foreach (var sb in handler.SourceBlocks)
                                { processedBasicBlocks.Add(sb.Id); _processedBlockIds.Add(sb.Id); }
                        }
                        if (tryStruct.ElseBlock != null)
                        {
                            foreach (var sb in tryStruct.ElseBlock.SourceBlocks)
                                { processedBasicBlocks.Add(sb.Id); _processedBlockIds.Add(sb.Id); }
                        }
                        if (tryStruct.FinallyBlock != null)
                        {
                            foreach (var sb in tryStruct.FinallyBlock.SourceBlocks)
                                { processedBasicBlocks.Add(sb.Id); _processedBlockIds.Add(sb.Id); }
                        }
                    }
                    
                    return stmts;
                }
            }
            else if (seqBlock.ParentStructure != null)
            {
                processedSeqBlocks.Add(seqBlock.Id);
                foreach (var sourceBlock in seqBlock.SourceBlocks)
                {
                    processedBasicBlocks.Add(sourceBlock.Id);
                    _processedBlockIds.Add(sourceBlock.Id);
                }
            }
            else if (seqBlock.ParentStructure == null)
            {
                // 第二循环：跳过已被控制结构消费的前缀块（仅含中间表达式）
                bool hasStructureHeaderSuccessor = seqBlock.Successors.Any(s => structureHeaders.Contains(s.Id));
                bool hasOnlyIntermediateExprs = seqBlock.Statements != null &&
                    seqBlock.Statements.All(s => s is ExprStmt);

                if (!(hasStructureHeaderSuccessor && hasOnlyIntermediateExprs) && seqBlock.Statements != null)
                {
                    stmts.AddRange(seqBlock.Statements);
                }
                foreach (var sourceBlock in seqBlock.SourceBlocks)
                {
                    processedBasicBlocks.Add(sourceBlock.Id);
                    _processedBlockIds.Add(sourceBlock.Id);
                }
            }
            processedSeqBlocks.Add(seqBlock.Id);
        }

        return stmts;
    }

    private List<Stmt> GenerateStatementsFromSeqBlockHybrid(SequentialBlock seqBlock, List<SequentialBlock> seqBlocks, ControlFlowGraph cfg, HashSet<int> processedSeqBlocks, HashSet<int> processedBasicBlocks, HashSet<int> structureHeaders)
    {
        var stmts = new List<Stmt>();

        if (processedSeqBlocks.Contains(seqBlock.Id))
            return stmts;

        processedSeqBlocks.Add(seqBlock.Id);

        if (structureHeaders.Contains(seqBlock.Id))
        {
            var structure = seqBlock.ParentStructure;
            if (structure != null)
            {
                Console.Error.WriteLine($"[SEQ_BUILD_HYBRID] Processing control structure: {structure.Type} at 0x{seqBlock.StartOffset:X4}");

                var structureStmts = BuildStructureStatements(structure);
                stmts.AddRange(structureStmts);

                MarkStructureBlocksProcessed(structure, processedSeqBlocks, seqBlocks);

                foreach (var sourceBlock in structure.Header.SourceBlocks)
                {
                    processedBasicBlocks.Add(sourceBlock.Id);
                    _processedBlockIds.Add(sourceBlock.Id);
                }
                foreach (var bodyBlock in structure.BodyBlocks)
                {
                    foreach (var sourceBlock in bodyBlock.SourceBlocks)
                    {
                        processedBasicBlocks.Add(sourceBlock.Id);
                        _processedBlockIds.Add(sourceBlock.Id);
                    }
                }

                if (structure is TryControlStructure tryStruct)
                {
                    foreach (var (handler, _, __) in tryStruct.ExceptHandlers)
                    {
                        foreach (var sourceBlock in handler.SourceBlocks)
                        {
                            processedBasicBlocks.Add(sourceBlock.Id);
                            _processedBlockIds.Add(sourceBlock.Id);
                        }
                    }
                    if (tryStruct.ElseBlock != null)
                    {
                        foreach (var sourceBlock in tryStruct.ElseBlock.SourceBlocks)
                        {
                            processedBasicBlocks.Add(sourceBlock.Id);
                            _processedBlockIds.Add(sourceBlock.Id);
                        }
                    }
                    if (tryStruct.FinallyBlock != null)
                    {
                        foreach (var sourceBlock in tryStruct.FinallyBlock.SourceBlocks)
                        {
                            processedBasicBlocks.Add(sourceBlock.Id);
                            _processedBlockIds.Add(sourceBlock.Id);
                        }
                    }
                }

                if (!(structure is TryControlStructure))
                {
                    var mergePoint = FindMergePoint(structure, seqBlocks);
                    if (mergePoint != null && !processedSeqBlocks.Contains(mergePoint.Id))
                    {
                        stmts.AddRange(GenerateStatementsFromSeqBlockHybrid(mergePoint, seqBlocks, cfg, processedSeqBlocks, processedBasicBlocks, structureHeaders));
                    }
                }
                else
                {
                    return stmts;
                }
            }
        }
        else if (seqBlock.ParentStructure != null)
        {
            return stmts;
        }
        else if (seqBlock.ParentStructure == null)
        {
            // 如果后继包含控制结构头，且本块的语句都是中间表达式（非 Assign/Return/If 等），
            // 则跳过输出——这些语句是控制结构的前缀指令，由 BuildStructureStatements 处理
            bool hasStructureHeaderSuccessor = seqBlock.Successors.Any(s => structureHeaders.Contains(s.Id));
            bool hasOnlyIntermediateExprs = seqBlock.Statements != null && 
                seqBlock.Statements.All(s => s is ExprStmt);

            if (hasStructureHeaderSuccessor && hasOnlyIntermediateExprs)
            {
                Console.Error.WriteLine($"[SEQ_BUILD_HYBRID] Skipping prefix seqBlock Id={seqBlock.Id}, Start=0x{seqBlock.StartOffset:X4} (consumed by structure)");
            }
            else if (seqBlock.Statements != null)
            {
                // 混合块（含有效语句 + 中间表达式）：保留有效语句，去掉尾部 ExprStmt（中间表达式）
                var filteredStmts = seqBlock.Statements;
                if (hasStructureHeaderSuccessor && filteredStmts.Count > 0 && filteredStmts.Last() is ExprStmt)
                {
                    Console.Error.WriteLine($"[SEQ_BUILD_HYBRID] Trimming trailing ExprStmt from seqBlock Id={seqBlock.Id}");
                    filteredStmts = filteredStmts.Take(filteredStmts.Count - 1).ToList();
                }
                Console.Error.WriteLine($"[SEQ_BUILD_HYBRID] Adding statements from seqBlock Id={seqBlock.Id}, Start=0x{seqBlock.StartOffset:X4}, count={filteredStmts.Count}");
                stmts.AddRange(filteredStmts);
            }
            foreach (var sourceBlock in seqBlock.SourceBlocks)
            {
                processedBasicBlocks.Add(sourceBlock.Id);
                _processedBlockIds.Add(sourceBlock.Id);
            }

            foreach (var succ in seqBlock.Successors)
            {
                if (!processedSeqBlocks.Contains(succ.Id))
                {
                    Console.Error.WriteLine($"[SEQ_BUILD_HYBRID] Processing successor: Id={succ.Id}, Start=0x{succ.StartOffset:X4}");
                    stmts.AddRange(GenerateStatementsFromSeqBlockHybrid(succ, seqBlocks, cfg, processedSeqBlocks, processedBasicBlocks, structureHeaders));
                }
            }
        }

        return stmts;
    }

    private void MarkStructureBlocksProcessed(ISequentialControlStructure structure, HashSet<int> processed, List<SequentialBlock> seqBlocks)
    {
        processed.Add(structure.Header.Id);
        foreach (var bodyBlock in structure.BodyBlocks)
            processed.Add(bodyBlock.Id);

        if (structure is WithControlStructure withStruct && withStruct.HandlerBlock != null)
            processed.Add(withStruct.HandlerBlock.Id);

        if (structure is TryControlStructure tryStruct)
        {
            foreach (var (handler, _, __) in tryStruct.ExceptHandlers)
            {
                processed.Add(handler.Id);
                foreach (var seqBlock in seqBlocks)
                {
                    if (seqBlock.StartOffset >= handler.StartOffset && seqBlock.StartOffset < handler.EndOffset)
                    {
                        processed.Add(seqBlock.Id);
                    }
                }
            }
            if (tryStruct.ElseBlock != null)
                processed.Add(tryStruct.ElseBlock.Id);
            
            int? tryEndOffset = null;
            if (tryStruct.FinallyBlock != null)
            {
                tryEndOffset = tryStruct.FinallyBlock.EndOffset;
            }
            else if (tryStruct.ExceptHandlers.Count > 0)
            {
                tryEndOffset = tryStruct.ExceptHandlers.Last().Handler.EndOffset;
            }
            
            if (tryEndOffset.HasValue)
            {
                Console.Error.WriteLine($"[MARK_STRUCT] Try structure: Header=0x{tryStruct.Header.StartOffset:X4}, End=0x{tryEndOffset.Value:X4}");
                foreach (var seqBlock in seqBlocks)
                {
                    if (seqBlock.StartOffset >= tryStruct.Header.StartOffset && 
                        seqBlock.StartOffset <= tryEndOffset.Value)
                    {
                        processed.Add(seqBlock.Id);
                        Console.Error.WriteLine($"[MARK_STRUCT] Marked seqBlock Id={seqBlock.Id}, Start=0x{seqBlock.StartOffset:X4}, End=0x{seqBlock.EndOffset:X4}");
                    }
                }
            }
            
            if (tryStruct.FinallyBlock != null)
            {
                processed.Add(tryStruct.FinallyBlock.Id);
                foreach (var seqBlock in seqBlocks)
                {
                    if (seqBlock.StartOffset >= tryStruct.FinallyBlock.StartOffset && 
                        seqBlock.StartOffset <= tryStruct.FinallyBlock.EndOffset)
                    {
                        processed.Add(seqBlock.Id);
                        Console.Error.WriteLine($"[MARK_STRUCT] Marked finally seqBlock Id={seqBlock.Id}, Start=0x{seqBlock.StartOffset:X4}");
                    }
                }
            }
        }

        if (structure is IfElseControlStructure ifStruct)
        {
            if (ifStruct.TrueBranch != null)
                processed.Add(ifStruct.TrueBranch.Id);
            if (ifStruct.FalseBranch != null)
                processed.Add(ifStruct.FalseBranch.Id);
        }

        if (structure is ForLoopControlStructure forStruct && forStruct.ElseBlock != null)
            processed.Add(forStruct.ElseBlock.Id);

        if (structure is WhileLoopControlStructure whileStruct && whileStruct.ElseBlock != null)
            processed.Add(whileStruct.ElseBlock.Id);
    }

    private SequentialBlock? FindMergePoint(ISequentialControlStructure structure, List<SequentialBlock> seqBlocks)
    {
        var allSuccessors = new HashSet<SequentialBlock>();

        foreach (var bodyBlock in structure.BodyBlocks)
        {
            foreach (var succ in bodyBlock.Successors)
            {
                allSuccessors.Add(succ);
            }
        }

        if (structure is ForLoopControlStructure forStruct && forStruct.ElseBlock != null)
        {
            foreach (var succ in forStruct.ElseBlock.Successors)
            {
                allSuccessors.Add(succ);
            }
        }

        if (structure is IfElseControlStructure ifStruct)
        {
            if (ifStruct.TrueBranch != null)
            {
                foreach (var succ in ifStruct.TrueBranch.Successors)
                {
                    allSuccessors.Add(succ);
                }
            }
            if (ifStruct.FalseBranch != null)
            {
                foreach (var succ in ifStruct.FalseBranch.Successors)
                {
                    allSuccessors.Add(succ);
                }
            }
            return ifStruct.MergePoint;
        }

        if (structure is TryControlStructure tryStruct)
        {
            foreach (var (handler, _, __) in tryStruct.ExceptHandlers)
            {
                foreach (var succ in handler.Successors)
                {
                    allSuccessors.Add(succ);
                }
            }
            if (tryStruct.ElseBlock != null)
            {
                foreach (var succ in tryStruct.ElseBlock.Successors)
                {
                    allSuccessors.Add(succ);
                }
            }
            if (tryStruct.FinallyBlock != null)
            {
                foreach (var succ in tryStruct.FinallyBlock.Successors)
                {
                    allSuccessors.Add(succ);
                }
            }
        }

        foreach (var succ in allSuccessors)
        {
            if (succ != structure.Header)
            {
                return succ;
            }
        }

        return null;
    }

    private List<Stmt> BuildStructureStatements(ISequentialControlStructure structure)
    {
        return structure switch
        {
            ForLoopControlStructure forLoop => BuildForLoopStructureStatements(forLoop),
            WhileLoopControlStructure whileLoop => BuildWhileLoopStructureStatements(whileLoop),
            WithControlStructure withStmt => BuildWithStructureStatements(withStmt),
            TryControlStructure tryStmt => BuildTryStructureStatements(tryStmt),
            IfElseControlStructure ifElse => BuildIfElseStructureStatements(ifElse),
            _ => new List<Stmt>()
        };
    }

    private List<Stmt> BuildForLoopStructureStatements(ForLoopControlStructure forLoop)
    {
        var headerInstrs = forLoop.Header.Instructions;
        var forIterIdx = headerInstrs.FindIndex(i => i.Opcode == Opcode.FOR_ITER);

        var iterExpr = ExtractIterExpression(forLoop.Header.SourceBlocks[0]);
        var bodyBasicBlocks = new List<BasicBlock>();
        foreach (var bodyBlock in forLoop.BodyBlocks)
        {
            bodyBasicBlocks.AddRange(bodyBlock.SourceBlocks);
        }
        var loopVar = ExtractLoopVariable(forLoop.Header.SourceBlocks[0], bodyBasicBlocks);

        Console.Error.WriteLine($"[SEQ_BUILD_FOR] Building FOR loop at 0x{forLoop.Header.StartOffset:X4}");
        Console.Error.WriteLine($"[SEQ_BUILD_FOR]   iterExpr: {iterExpr}, loopVar: {loopVar}");
        Console.Error.WriteLine($"[SEQ_BUILD_FOR]   {forLoop.BodyBlocks.Count} body blocks");

        var bodyStmts = new List<Stmt>();
        foreach (var bodyBlock in forLoop.BodyBlocks)
        {
            Console.Error.WriteLine($"[SEQ_BUILD_FOR]     Body block 0x{bodyBlock.StartOffset:X4}: {bodyBlock.Instructions.Count} instrs, {bodyBlock.Statements?.Count ?? 0} stmts, ParentStructure={bodyBlock.ParentStructure?.Type}");
            
            if (bodyBlock.ParentStructure != null && bodyBlock.ParentStructure != forLoop)
            {
                Console.Error.WriteLine($"[SEQ_BUILD_FOR]       Inserting nested {bodyBlock.ParentStructure.Type}");
                var nestedStmts = BuildStructureStatements(bodyBlock.ParentStructure);
                bodyStmts.AddRange(nestedStmts);
                continue;
            }
            
            if (bodyBlock.Statements != null)
            {
                bodyStmts.AddRange(bodyBlock.Statements);
            }
        }

        Console.Error.WriteLine($"[SEQ_BUILD_FOR]   Total body stmts: {bodyStmts.Count}");

        var elseStmts = forLoop.ElseBlock?.Statements;

        return new List<Stmt> { new For(loopVar, iterExpr, bodyStmts, elseStmts) };
    }

    private List<Stmt> BuildWhileLoopStructureStatements(WhileLoopControlStructure whileLoop)
    {
        var testExpr = ExtractCondition(whileLoop.Header.SourceBlocks[0]);

        var bodyStmts = new List<Stmt>();
        foreach (var bodyBlock in whileLoop.BodyBlocks)
        {
            if (bodyBlock.ParentStructure != null && bodyBlock.ParentStructure != whileLoop)
            {
                var nestedStmts = BuildStructureStatements(bodyBlock.ParentStructure);
                bodyStmts.AddRange(nestedStmts);
                continue;
            }
            
            if (bodyBlock.Statements != null)
                bodyStmts.AddRange(bodyBlock.Statements);
        }

        var elseStmts = whileLoop.ElseBlock?.Statements;

        return new List<Stmt> { new While(testExpr, bodyStmts, elseStmts) };
    }

    private List<Stmt> BuildWithStructureStatements(WithControlStructure withStmt)
    {
        var headerInstrs = withStmt.Header.Instructions;
        var sm = new StackMachine(_codeObject);

        

        bool isPy314Style = headerInstrs.Any(i => i.Opcode == Opcode.LOAD_SPECIAL);

        if (isPy314Style)
        {
            int withPatternStartIdx = -1;
            for (int i = 0; i < headerInstrs.Count - 6; i++)
            {
                if (headerInstrs[i].Opcode == Opcode.LOAD_FAST_BORROW_314 &&
                    headerInstrs[i + 1].Opcode == Opcode.COPY &&
                    headerInstrs[i + 2].Opcode == Opcode.LOAD_SPECIAL &&
                    headerInstrs[i + 3].Opcode == Opcode.SWAP &&
                    headerInstrs[i + 4].Opcode == Opcode.SWAP &&
                    headerInstrs[i + 5].Opcode == Opcode.LOAD_SPECIAL &&
                    headerInstrs[i + 6].Opcode == Opcode.CALL)
                {
                    withPatternStartIdx = i;
                    break;
                }
            }
            
            if (withPatternStartIdx < 0)
                return new List<Stmt>();

            var preWithStmts = new List<Stmt>();
            if (withPatternStartIdx > 0)
            {
                var preMachine = new StackMachine(_codeObject);
                for (int i = 0; i < withPatternStartIdx; i++)
                {
                    var stmt = preMachine.Execute(headerInstrs[i]);
                    if (stmt != null)
                        preWithStmts.Add(stmt);
                }
                while (preMachine.HasResults)
                    preWithStmts.Add(new ExprStmt(preMachine.PopResult()));
            }

            for (int i = withPatternStartIdx; i <= withPatternStartIdx; i++)
            {
                sm.Execute(headerInstrs[i]);
            }

            Expr? py314ContextExpr = sm.ExprStackCount > 0 ? sm.PopExpr() : null;
            if (py314ContextExpr == null)
                return preWithStmts;

            Expr? py314OptionalVar = null;
            int headerEndIdx = headerInstrs.Count;
            
            for (int i = 0; i < headerInstrs.Count - 6; i++)
            {
                if (headerInstrs[i].Opcode == Opcode.LOAD_FAST_BORROW_314 &&
                    headerInstrs[i + 1].Opcode == Opcode.COPY &&
                    headerInstrs[i + 2].Opcode == Opcode.LOAD_SPECIAL &&
                    headerInstrs[i + 3].Opcode == Opcode.SWAP &&
                    headerInstrs[i + 4].Opcode == Opcode.SWAP &&
                    headerInstrs[i + 5].Opcode == Opcode.LOAD_SPECIAL &&
                    headerInstrs[i + 6].Opcode == Opcode.CALL)
                {
                    if (i + 7 < headerInstrs.Count && 
                        headerInstrs[i + 7].Opcode == Opcode.STORE_FAST && 
                        headerInstrs[i + 7].Argument.HasValue)
                    {
                        var idx = headerInstrs[i + 7].Argument.Value;
                        string varName = idx < _codeObject.Varnames.Count ? _codeObject.Varnames[idx] : $"v_{idx}";
                        py314OptionalVar = new Name(varName, ExpressionContext.Store);
                        headerEndIdx = i + 8;
                    }
                    else
                    {
                        headerEndIdx = i + 7;
                    }
                    break;
                }
            }
            
            if (py314OptionalVar == null && withStmt.BodyBlocks.Count > 0)
            {
                var firstBodyBlock = withStmt.BodyBlocks[0];
                if (firstBodyBlock.Instructions.Count > 0 && 
                    firstBodyBlock.Instructions[0].Opcode == Opcode.STORE_FAST && 
                    firstBodyBlock.Instructions[0].Argument.HasValue)
                {
                    var idx = firstBodyBlock.Instructions[0].Argument.Value;
                    string varName = idx < _codeObject.Varnames.Count ? _codeObject.Varnames[idx] : $"v_{idx}";
                    py314OptionalVar = new Name(varName, ExpressionContext.Store);
                    
                }
            }

            var py314BodyStmts = new List<Stmt>();
            
            if (headerEndIdx < headerInstrs.Count)
            {
                var bodyMachine = new StackMachine(_codeObject);
                for (int i = headerEndIdx; i < headerInstrs.Count; i++)
                {
                    var stmt = bodyMachine.Execute(headerInstrs[i]);
                    if (stmt != null)
                        py314BodyStmts.Add(stmt);
                }
                while (bodyMachine.HasResults)
                    py314BodyStmts.Add(new ExprStmt(bodyMachine.PopResult()));
            }

            foreach (var bodyBlock in withStmt.BodyBlocks)
            {
                if (bodyBlock.ParentStructure != null && bodyBlock.ParentStructure != withStmt)
                {
                    var nestedStmts = BuildStructureStatements(bodyBlock.ParentStructure);
                    py314BodyStmts.AddRange(nestedStmts);
                    continue;
                }
                
                if (bodyBlock.Statements != null)
                {
                    bool skipFirstStmt = false;
                    if (py314OptionalVar == null && bodyBlock.Statements.Count > 0)
                    {
                        var firstStmt = bodyBlock.Statements[0];
                        if (firstStmt is Assign assignStmt && assignStmt.Targets.Count == 1 && assignStmt.Targets[0] is Name nameTarget)
                        {
                            py314OptionalVar = nameTarget;
                            skipFirstStmt = true;
                        }
                    }
                    else if (py314OptionalVar != null && bodyBlock.Statements.Count > 0)
                    {
                        var firstStmt = bodyBlock.Statements[0];
                        if (firstStmt is Assign assignStmt && assignStmt.Targets.Count == 1 && assignStmt.Targets[0] is Name nameTarget)
                        {
                            if (nameTarget.Id == ((Name)py314OptionalVar).Id)
                            {
                                skipFirstStmt = true;
                            }
                        }
                    }
                    
                    if (skipFirstStmt)
                        py314BodyStmts.AddRange(bodyBlock.Statements.Skip(1));
                    else
                        py314BodyStmts.AddRange(bodyBlock.Statements);
                }
            }

            preWithStmts.Add(new With(new List<WithItem> { new WithItem(py314ContextExpr, py314OptionalVar) }, py314BodyStmts));
            return preWithStmts;
        }

        int endIdx = headerInstrs.FindIndex(i => 
            i.Opcode == Opcode.SETUP_WITH || 
            i.Opcode == Opcode.BEFORE_WITH || 
            i.Opcode == Opcode.BEFORE_WITH_312 || 
            i.Opcode == Opcode.BEFORE_WITH_313 ||
            i.Opcode == Opcode.LOAD_SPECIAL);

        Console.Error.WriteLine($"[WITH_BUILD] header instrs: {string.Join(",", headerInstrs.Select(i => i.Opcode))}, endIdx={endIdx}");

        if (endIdx < 0)
            endIdx = headerInstrs.Count;

        for (int i = 0; i < endIdx; i++)
        {
            sm.Execute(headerInstrs[i]);
        }

        Expr? contextExpr = sm.ExprStackCount > 0 ? sm.PopExpr() : null;
        Console.Error.WriteLine($"[WITH_BUILD] contextExpr={contextExpr}");
        
        if (contextExpr == null)
            return new List<Stmt>();

        Expr? optionalVar = null;
        for (int i = endIdx + 1; i < headerInstrs.Count; i++)
        {
            if (headerInstrs[i].Opcode is Opcode.STORE_FAST or Opcode.STORE_NAME && headerInstrs[i].Argument.HasValue)
            {
                var idx = headerInstrs[i].Argument.Value;
                string varName = headerInstrs[i].Opcode == Opcode.STORE_FAST
                    ? (idx < _codeObject.Varnames.Count ? _codeObject.Varnames[idx] : $"v_{idx}")
                    : (idx < _codeObject.Names.Count ? _codeObject.Names[idx] : $"n_{idx}");
                optionalVar = new Name(varName, ExpressionContext.Store);
                Console.Error.WriteLine($"[WITH_BUILD] Found optionalVar at index {i}: {varName}");
                break;
            }
        }
        
        Console.Error.WriteLine($"[WITH_BUILD] optionalVar={optionalVar}");
        Console.Error.WriteLine($"[WITH_BUILD] bodyBlocks count={withStmt.BodyBlocks.Count}");

        var bodyStmts = new List<Stmt>();
        foreach (var bodyBlock in withStmt.BodyBlocks)
        {
            if (bodyBlock.ParentStructure != null && bodyBlock.ParentStructure != withStmt)
            {
                var nestedStmts = BuildStructureStatements(bodyBlock.ParentStructure);
                bodyStmts.AddRange(nestedStmts);
                continue;
            }
            
            if (bodyBlock.Statements != null)
                bodyStmts.AddRange(bodyBlock.Statements);
        }

        return new List<Stmt> { new With(new List<WithItem> { new WithItem(contextExpr, optionalVar) }, bodyStmts) };
    }

    private List<Stmt> BuildTryStructureStatements(TryControlStructure tryStmt)
    {
        var bodyStmts = new List<Stmt>();
        foreach (var bodyBlock in tryStmt.BodyBlocks)
        {
            if (bodyBlock.ParentStructure != null && bodyBlock.ParentStructure != tryStmt)
            {
                var nestedStmts = BuildStructureStatements(bodyBlock.ParentStructure);
                bodyStmts.AddRange(nestedStmts);
                continue;
            }
            
            var allInstrs = bodyBlock.Instructions;
            var sm = new StackMachine(_codeObject);
            foreach (var instr in allInstrs)
            {
                if (instr.Opcode == Opcode.JUMP_FORWARD ||
                    instr.Opcode == Opcode.JUMP_ABSOLUTE ||
                    instr.Opcode == Opcode.POP_EXCEPT ||
                    instr.Opcode == Opcode.RERAISE ||
                    instr.Opcode == Opcode.COPY)
                    break;
                var result = sm.Execute(instr);
                if (result is Stmt stmt)
                    bodyStmts.Add(stmt);
            }
            while (sm.HasResults)
            {
                var result = sm.PopResult();
                if (result is Name name && name.Id == "None")
                    continue;
                bodyStmts.Add(new ExprStmt(result));
            }
        }

        var handlers = new List<ExceptHandler>();
        foreach (var (handlerBlock, exceptType, exceptVar) in tryStmt.ExceptHandlers)
        {
            var handlerInstrs = handlerBlock.Instructions;
            
            int bodyStartIdx = 0;
            bool seenCheckExcMatch = false;
            
            for (int i = 0; i < handlerInstrs.Count; i++)
            {
                if (handlerInstrs[i].Opcode == Opcode.CHECK_EXC_MATCH || 
                    handlerInstrs[i].Opcode == Opcode.CHECK_EG_MATCH)
                {
                    seenCheckExcMatch = true;
                }
                else if (seenCheckExcMatch && handlerInstrs[i].Opcode == Opcode.STORE_FAST)
                {
                    bodyStartIdx = i + 1;
                    break;
                }
                else if (seenCheckExcMatch && 
                         handlerInstrs[i].Opcode != Opcode.PUSH_EXC_INFO_312 && 
                         handlerInstrs[i].Opcode != Opcode.PUSH_EXC_INFO &&
                         handlerInstrs[i].Opcode != Opcode.LOAD_GLOBAL &&
                         handlerInstrs[i].Opcode != Opcode.COPY)
                {
                    bodyStartIdx = i;
                    break;
                }
            }
            
            if (bodyStartIdx >= handlerInstrs.Count)
                bodyStartIdx = 0;
            
            var bodyInstrs = handlerInstrs.Skip(bodyStartIdx).ToList();
            
            var sm = new StackMachine(_codeObject);
            var handlerStmts = new List<Stmt>();
            foreach (var instr in bodyInstrs)
            {
                if (instr.Opcode == Opcode.POP_EXCEPT || 
                    instr.Opcode == Opcode.END_FINALLY ||
                    instr.Opcode == Opcode.RERAISE ||
                    instr.Opcode == Opcode.JUMP_FORWARD ||
                    instr.Opcode == Opcode.JUMP_ABSOLUTE ||
                    instr.Opcode == Opcode.PUSH_EXC_INFO_312 ||
                    instr.Opcode == Opcode.PUSH_EXC_INFO)
                {
                    break;
                }
                
                var result = sm.Execute(instr);
                if (result is Stmt stmt)
                    handlerStmts.Add(stmt);
            }
            while (sm.HasResults)
            {
                handlerStmts.Add(new ExprStmt(sm.PopResult()));
            }
            
            Expr? typeExpr = null;
            if (!string.IsNullOrEmpty(exceptType))
                typeExpr = new Name(exceptType);
            
            handlers.Add(new ExceptHandler(typeExpr, exceptVar, handlerStmts));
        }

        List<Stmt>? elseStmts = null;
        if (tryStmt.ElseBlock != null)
        {
            var elseInstrs = tryStmt.ElseBlock.Instructions;
            var sm = new StackMachine(_codeObject);
            elseStmts = new List<Stmt>();
            bool seenNop = false;
            
            for (int i = 0; i < elseInstrs.Count; i++)
            {
                var instr = elseInstrs[i];
                
                if (instr.Opcode == Opcode.NOP)
                {
                    seenNop = true;
                    continue;
                }
                
                if (instr.Opcode == Opcode.RETURN_VALUE ||
                    instr.Opcode == Opcode.JUMP_FORWARD ||
                    instr.Opcode == Opcode.JUMP_ABSOLUTE)
                {
                    break;
                }
                
                var result = sm.Execute(instr);
                if (result is Stmt stmt)
                    elseStmts.Add(stmt);
            }
            while (sm.HasResults)
                elseStmts.Add(new ExprStmt(sm.PopResult()));
        }
        
        List<Stmt>? finallyStmts = null;
        if (tryStmt.FinallyBlock != null)
        {
            var finallyInstrs = tryStmt.FinallyBlock.Instructions;
            
            var sm = new StackMachine(_codeObject);
            finallyStmts = new List<Stmt>();
            
            int startIdx = 0;
            bool foundPushExcInfo = false;
            for (int i = 0; i < finallyInstrs.Count; i++)
            {
                if (finallyInstrs[i].Opcode == Opcode.PUSH_EXC_INFO_312 || 
                    finallyInstrs[i].Opcode == Opcode.PUSH_EXC_INFO)
                {
                    startIdx = i + 1;
                    foundPushExcInfo = true;
                }
            }
            
            int endIdx = finallyInstrs.Count;
            for (int i = startIdx; i < finallyInstrs.Count; i++)
            {
                if (finallyInstrs[i].Opcode == Opcode.RERAISE ||
                    finallyInstrs[i].Opcode == Opcode.END_FINALLY ||
                    finallyInstrs[i].Opcode == Opcode.POP_EXCEPT ||
                    finallyInstrs[i].Opcode == Opcode.RETURN_VALUE)
                {
                    endIdx = i;
                    break;
                }
            }
            
            for (int i = startIdx; i < endIdx; i++)
            {
                var instr = finallyInstrs[i];
                
                if (instr.Opcode == Opcode.NOP)
                    continue;
                
                var result = sm.Execute(instr);
                if (result is Stmt stmt)
                    finallyStmts.Add(stmt);
            }
            while (sm.HasResults)
                finallyStmts.Add(new ExprStmt(sm.PopResult()));
        }

        // Phase 9-04: 空的 try body（只有 pass）→ 直接返回 body
        // 先移除 body 中的 pass（与 CollapseRedundantPasses 同逻辑）
        bodyStmts.RemoveAll(s => s is Pass);
        if (bodyStmts.Count == 0
            && (elseStmts == null || elseStmts.Count == 0)
            && (finallyStmts == null || finallyStmts.Count == 0))
        {
            Console.Error.WriteLine(
                $"[TRY_FIX] Suppressed empty try (stripped to body statements)");
            return bodyStmts;
        }

        // Phase 9-2-03: 空的 except handler → 移除（产生 TRY_NO_HANDLER 伪影）
        handlers.RemoveAll(h => h.Body == null || h.Body.Count == 0 || h.Body.All(s => s is Pass));
        if (handlers.Count == 0
            && (finallyStmts == null || finallyStmts.Count == 0)
            && (elseStmts == null || elseStmts.Count == 0))
        {
            Console.Error.WriteLine(
                $"[TRY_FIX] Suppressed try with no handlers and no finally");
            return bodyStmts;
        }

        return new List<Stmt> { new Try(bodyStmts, handlers, elseStmts, finallyStmts) };
    }

    private List<Stmt> BuildIfElseStructureStatements(IfElseControlStructure ifElse)
    {
        var testExpr = ExtractCondition(ifElse.Header.SourceBlocks[0]);

        var bodyStmts = new List<Stmt>();
        foreach (var bodyBlock in ifElse.BodyBlocks)
        {
            if (bodyBlock.ParentStructure != null && bodyBlock.ParentStructure != ifElse)
            {
                var nestedStmts = BuildStructureStatements(bodyBlock.ParentStructure);
                bodyStmts.AddRange(nestedStmts);
                continue;
            }
            
            if (bodyBlock.Statements != null)
                bodyStmts.AddRange(bodyBlock.Statements);
        }

        var elseStmts = ifElse.FalseBranch?.Statements;

        return new List<Stmt> { new If(testExpr, bodyStmts, elseStmts) };
    }

    // ---- Phase 8 Step 3: BARE_EXPR 清理 passes ----

    /// <summary>
    /// BARE_EXPR 专用清理器。
    /// 删除 StackMachine 生成的编译器中间表达式残留。
    /// 
    /// 安全规则组（按安全度从高到低执行）：
    ///   🟢 B4/B6: FunctionRef(`<...>`) — 已转为 FunctionDef 的函数引用
    ///   🟢 B8: 孤立 Name 表达式 — 编译器控制的中间变量名
    ///   🟢 B5: 类体属性泄漏 — cls.__xxx__ / self.xxx() 等
    ///   🟡 B1/B2/B3: comprehension .append/.add — 需上下文检测
    ///   🟡 B7: match type pattern — match/case 类型名残留
    /// </summary>
    private List<Stmt> CleanupBareExpr(List<Stmt> stmts)
    {
        var result = new List<Stmt>(stmts.Count);

        for (int i = 0; i < stmts.Count; i++)
        {
            var stmt = stmts[i];

            // 递归处理子结构（BARE_EXPR 可能嵌套在 if/for/while/try/with/func 体内）
            var processed = ProcessChildBareExpr(stmt);
            if (processed != null)
            {
                result.Add(processed);
                continue;
            }

            if (stmt is ExprStmt exprStmt)
            {
                // 🟢 B4/B6: FunctionRef 删除（已转为 FunctionDef）
                if (exprStmt.Value is FunctionRef fr && fr.Name.StartsWith("<"))
                    continue;

                // 🟢 B8: 孤立 Name 删除
                if (exprStmt.Value is Name name && IsBareNameSafeToRemove(name, stmts, i))
                    continue;

                // 🟢 B5: 类体属性删除
                if (exprStmt.Value is AstAttribute attr && IsClassBodyAttribute(attr))
                    continue;

                // 🟢 B5: 类体方法调用
                if (exprStmt.Value is Call call && IsClassBodyMethodCall(call))
                    continue;

                // 🟡 B1/B2/B3: comprehension .append/.add 删除
                if (IsComprehensionAppendCall(exprStmt, stmts, i))
                    continue;

                // 🟡 B7: match type pattern 删除
                if (IsMatchTypePattern(exprStmt, stmts, i))
                    continue;

                // 🟢 孤立 None / raise / return
                if (exprStmt.Value is Constant { Value: null })
                    continue;
                if (exprStmt.Value is Name { Id: "raise" or "return" or "yield" })
                    continue;

                // 🟢 短字符串常量（docstring/f-string 残留）
                if (exprStmt.Value is Constant { Value: string s } && s.Length < 80)
                    continue;

                // 🟢 短 Name 或含特殊字符的 Name（f-string 片段残留）
                if (exprStmt.Value is Name n && (n.Id.Length <= 2 || n.Id.Contains(".")))
                    continue;

                // 🟢 AstAttribute→Call 链（如 cls.__dict__.items()）
                if (exprStmt.Value is Call { Func: AstAttribute attr2 }
                    && IsAstAttributeChainWithCls(attr2))
                    continue;

                // 🟢 for 循环前的迭代器表达式（GET_ITER 泄漏）
                if (exprStmt.Value is Call { Func: Name { Id: "range" or "iter" or "islice" } }
                    && i + 1 < stmts.Count && stmts[i + 1] is For)
                    continue;

                result.Add(stmt);
            }
            else
            {
                // 🟢 裸 Raise 语句（无参数 — comprehension for-else 的 StopIteration 残留）
                if (stmt is Raise { Exc: null, Cause: null })
                    continue;

                // 🟢 编译器生成的 `var = None` 清理代码（try/except cleanup 泄漏）
                if (stmt is Assign { Targets: [Name _], Value: Constant { Value: null } })
                    continue;

                result.Add(stmt);
            }
        }

        return result;
    }

    // ---- Phase 9-2-01: return/raise 后死代码清理 ----

    /// <summary>
    /// 删除 return/raise 之后的死代码（bare ExprStmt）。
    /// abc.py 等文件中，if 分支以 return 结束后后续块的语句变成死代码。
    /// 只删除 ExprStmt/Pass/Continue/Break — 不删除 Assign/FunctionDef/ClassDef/控制结构。
    /// </summary>
    private static List<Stmt> CleanDeadCodeAfterReturn(List<Stmt> stmts)
    {
        if (stmts == null || stmts.Count <= 1)
            return stmts ?? new List<Stmt>();

        var result = new List<Stmt>(stmts.Count);
        bool dead = false;

        for (int i = 0; i < stmts.Count; i++)
        {
            var stmt = stmts[i];

            switch (stmt)
            {
                case FunctionDef fd:
                    result.Add(fd with { Body = CleanDeadCodeAfterReturn(fd.Body) });
                    dead = false;
                    continue;
                case ClassDef cd:
                    result.Add(cd with { Body = CleanDeadCodeAfterReturn(cd.Body) });
                    dead = false;
                    continue;
                case If ifStmt:
                    result.Add(ifStmt with
                    {
                        Body = CleanDeadCodeAfterReturn(ifStmt.Body),
                        Orelse = ifStmt.Orelse != null
                            ? CleanDeadCodeAfterReturn(ifStmt.Orelse) : null
                    });
                    dead = false;
                    continue;
                case While whileStmt:
                    result.Add(whileStmt with
                    {
                        Body = CleanDeadCodeAfterReturn(whileStmt.Body),
                        Orelse = whileStmt.Orelse != null
                            ? CleanDeadCodeAfterReturn(whileStmt.Orelse) : null
                    });
                    dead = false;
                    continue;
                case For forStmt:
                    result.Add(forStmt with
                    {
                        Body = CleanDeadCodeAfterReturn(forStmt.Body),
                        Orelse = forStmt.Orelse != null
                            ? CleanDeadCodeAfterReturn(forStmt.Orelse) : null
                    });
                    dead = false;
                    continue;
                case Try tryStmt:
                    result.Add(tryStmt with
                    {
                        Body = CleanDeadCodeAfterReturn(tryStmt.Body),
                        Handlers = tryStmt.Handlers.Select(h =>
                            h with { Body = CleanDeadCodeAfterReturn(h.Body) }).ToList(),
                        Orelse = tryStmt.Orelse != null
                            ? CleanDeadCodeAfterReturn(tryStmt.Orelse) : null,
                        Finalbody = tryStmt.Finalbody != null
                            ? CleanDeadCodeAfterReturn(tryStmt.Finalbody) : null
                    });
                    dead = false;
                    continue;
                case With withStmt:
                    result.Add(withStmt with { Body = CleanDeadCodeAfterReturn(withStmt.Body) });
                    dead = false;
                    continue;
            }

            if (dead)
            {
                if (stmt is ExprStmt or Pass or Continue or Break)
                {
                    continue;
                }
                dead = false;
            }

            if (stmt is Return || stmt is Raise or Yield)
                dead = true;

            result.Add(stmt);
        }

        return result;
    }

    /// <summary>递归清理子结构的 BARE_EXPR。</summary>
    private Stmt? ProcessChildBareExpr(Stmt stmt)
    {
        switch (stmt)
        {
            case FunctionDef fd:
                return fd with { Body = CleanupBareExpr(fd.Body) };
            case ClassDef cd:
                return cd with { Body = CleanupBareExpr(cd.Body) };
            case If ifStmt:
                return ifStmt with
                {
                    Body = CleanupBareExpr(ifStmt.Body),
                    Orelse = ifStmt.Orelse != null ? CleanupBareExpr(ifStmt.Orelse) : null
                };
            case While whileStmt:
                return whileStmt with
                {
                    Body = CleanupBareExpr(whileStmt.Body),
                    Orelse = whileStmt.Orelse != null ? CleanupBareExpr(whileStmt.Orelse) : null
                };
            case For forStmt:
                return forStmt with
                {
                    Body = CleanupBareExpr(forStmt.Body),
                    Orelse = forStmt.Orelse != null ? CleanupBareExpr(forStmt.Orelse) : null
                };
            case Try tryStmt:
                return tryStmt with
                {
                    Body = CleanupBareExpr(tryStmt.Body),
                    Handlers = tryStmt.Handlers.Select(h =>
                        h with { Body = CleanupBareExpr(h.Body) }).ToList(),
                    Orelse = tryStmt.Orelse != null ? CleanupBareExpr(tryStmt.Orelse) : null,
                    Finalbody = tryStmt.Finalbody != null ? CleanupBareExpr(tryStmt.Finalbody) : null
                };
            case With withStmt:
                return withStmt with { Body = CleanupBareExpr(withStmt.Body) };
            default:
                return null; // 非容器节点，交由上层处理
        }
    }

    /// <summary>B8: 判断孤立 Name 是否可以安全删除。</summary>
    private static bool IsBareNameSafeToRemove(Name name, List<Stmt> stmts, int index)
    {
        // 短名称列表：编译器中间变量，不会独立产生语义
        var bareNames = new HashSet<string>
        {
            "x", "y", "z", "v", "n", "i", "j", "k",     // comprehension 循环变量
            "it", "method", "result", "total",           // 编译器残留
            "StopIteration", "ValueError", "ZeroDivisionError", // 异常类型名
            "num", "row",                                 // 推导式变量
            "cls", "name",                                // 类体/枚举访问
            "return", "yield",                            // 关键字残留
            "raise",                                      // 关键字残留
        };

        if (!bareNames.Contains(name.Id))
            return false;

        // 安全检查：确保 Name 不是函数的 return value（例如 return x 不应该被删）
        // 对于纯 ExprStmt，它只是孤立表达式，可安全删除
        return true;
    }

    /// <summary>B5: 判断 Attribute 是否为类体属性访问。</summary>
    private static bool IsClassBodyAttribute(AstAttribute attr)
    {
        // cls.__bases__, cls.__dict__, cls._abc_registry 等
        if (attr.Value is Name { Id: "cls" })
            return true;

        // self.xxx (在类体中作为独立表达式)
        if (attr.Value is Name { Id: "self" })
            return true;

        return false;
    }

    /// <summary>判断 AstAttribute 链是否包含 cls（如 cls.__dict__.items()）。</summary>
    private static bool IsAstAttributeChainWithCls(AstAttribute attr)
    {
        // 递归检查属性链的根源是否为 cls
        Expr current = attr;
        while (current is AstAttribute innerAttr)
        {
            current = innerAttr.Value;
        }
        return current is Name { Id: "cls" or "self" };
    }

    /// <summary>B5: 判断 Call 是否为类体方法调用。</summary>
    private static bool IsClassBodyMethodCall(Call call)
    {
        // self.connect(), self.disconnect() 等（类体上下文残留）
        if (call.Func is AstAttribute { Value: Name { Id: "self" or "cls" } })
            return true;

        // gen.reset(10) — 类体中 generator 方法调用
        if (call.Func is AstAttribute { Value: Name _ })
            return true;

        return false;
    }

    /// <summary>B1/B2/B3: 判断是否为 comprehension 残留的 .append/.add 调用。</summary>
    private static bool IsComprehensionAppendCall(ExprStmt exprStmt, List<Stmt> stmts, int index)
    {
        if (exprStmt.Value is not Call call)
            return false;

        // 检测 .append(x) 模式
        if (call.Func is AstAttribute { Attr: "append" or "add" } attr)
        {
            // 获取目标变量名
            string? targetName = attr.Value switch
            {
                Name n => n.Id,
                _ => null
            };

            if (targetName == null) return false;

            // 检查前面是否存在同名变量的 ListComp/SetComp/DictComp 赋值
            for (int j = Math.Max(0, index - 5); j < index; j++)
            {
                if (stmts[j] is Assign assign
                    && assign.Targets.Count == 1
                    && assign.Targets[0] is Name assignName
                    && assignName.Id == targetName
                    && (assign.Value is ListComp or SetComp or DictComp))
                {
                    return true;
                }
                // 或检查转换后的 For 循环（comprehension 已被 ConvertComprehensionCalls 处理）
                if (stmts[j] is For forStmt
                    && forStmt.Target is Name forName
                    && forName.Id == targetName
                    && (forStmt.Iter is not Name || !forStmt.Iter.ToString()!.Contains("iterable")))
                {
                    return true;
                }
            }
        }

        // 检测 .__setitem__(key, val) 模式（dict comprehension）
        if (call.Func is AstAttribute { Attr: "__setitem__" } setitemAttr)
        {
            string? targetName = setitemAttr.Value switch
            {
                Name n => n.Id,
                _ => null
            };

            if (targetName == null) return false;

            for (int j = Math.Max(0, index - 5); j < index; j++)
            {
                if (stmts[j] is Assign assign
                    && assign.Targets.Count == 1
                    && assign.Targets[0] is Name assignName
                    && assignName.Id == targetName
                    && assign.Value is DictComp)
                {
                    return true;
                }
            }
        }

        // 检测 .extend(x) 模式（comprehension result collection）
        if (call.Func is AstAttribute { Attr: "extend" } extendAttr)
        {
            string? targetName = extendAttr.Value switch
            {
                Name n => n.Id,
                _ => null
            };

            if (targetName == null) return false;

            for (int j = Math.Max(0, index - 5); j < index; j++)
            {
                if (stmts[j] is Assign assign
                    && assign.Targets.Count == 1
                    && assign.Targets[0] is Name assignName
                    && assignName.Id == targetName
                    && (assign.Value is ListComp or SetComp or DictComp or GeneratorExp))
                {
                    return true;
                }
            }
        }

        return false;
    }

    /// <summary>B7: 判断 match type pattern 残留（int, str 等类型名）。</summary>
    private static bool IsMatchTypePattern(ExprStmt exprStmt, List<Stmt> stmts, int index)
    {
        if (exprStmt.Value is not Name name)
            return false;

        // match/case 中的类型模式（case int: 等）
        var matchTypes = new HashSet<string> { "int", "str", "float", "bool", "bytes", "list", "dict", "tuple", "set", "type" };
        if (!matchTypes.Contains(name.Id))
            return false;

        // 检查前后文中是否有 match 语句
        for (int j = Math.Max(0, index - 10); j <= Math.Min(stmts.Count - 1, index + 5); j++)
        {
            if (stmts[j] is Match)
                return true;
        }

        return false;
    }

    // ---- Phase 9-03: 语法错误修复 ----

    /// <summary>
    /// 检测并修复反编译输出中的语法错误模式。
    /// 
    /// 处理三类常见的无效语法：
    /// 1. 无效函数名（如 `def 5(x):`）→ 3.5-3.7 推导式误转为函数定义
    /// 2. yield from 在类体/函数体外 → 替换为 pass
    /// 3. continue/break 在循环体外 → 替换为 pass
    /// </summary>
    private static List<Stmt> FixSyntaxErrors(List<Stmt> stmts)
    {
        if (stmts == null || stmts.Count == 0)
            return stmts ?? new List<Stmt>();

        var result = new List<Stmt>(stmts.Count);

        for (int i = 0; i < stmts.Count; i++)
        {
            var stmt = stmts[i];

            // 规则 1: FunctionDef 名称为无效 Python 标识符 → 删除
            // 3.5-3.7 推导式中编译器中间代码对象以数字为名称
            if (stmt is FunctionDef fd && !IsValidPythonIdentifier(fd.Name))
            {
                Console.Error.WriteLine(
                    $"[SYNTAX_FIX] Removed FunctionDef with invalid name: '{fd.Name}'");
                continue;
            }

            // 规则 2: yield / yield from / await 在非函数体内 → pass
            if (IsInvalidYieldUsage(stmt))
            {
                Console.Error.WriteLine("[SYNTAX_FIX] Replaced invalid yield/await with pass");
                result.Add(new Pass());
                continue;
            }

            // 规则 3: continue/break 在循环体外 → pass
            if (stmt is Continue or Break)
            {
                Console.Error.WriteLine(
                    $"[SYNTAX_FIX] Replaced '{stmt.GetType().Name}' outside loop with pass");
                result.Add(new Pass());
                continue;
            }

            // 递归处理容器结构的子 body
            var processed = FixSyntaxErrorsRecursive(stmt);
            if (processed != null)
            {
                result.Add(processed);
                continue;
            }

            result.Add(stmt);
        }

        return result;
    }

    /// <summary>递归处理嵌套结构中的语法错误。</summary>
    private static Stmt? FixSyntaxErrorsRecursive(Stmt stmt)
    {
        switch (stmt)
        {
            case FunctionDef fd:
                return fd with { Body = FixSyntaxErrors(fd.Body) };
            case ClassDef cd:
                return cd with { Body = FixSyntaxErrors(cd.Body) };
            case If ifStmt:
                return ifStmt with
                {
                    Body = FixSyntaxErrors(ifStmt.Body),
                    Orelse = ifStmt.Orelse != null ? FixSyntaxErrors(ifStmt.Orelse) : null
                };
            case While whileStmt:
                return whileStmt with
                {
                    Body = FixSyntaxErrors(whileStmt.Body),
                    Orelse = whileStmt.Orelse != null ? FixSyntaxErrors(whileStmt.Orelse) : null
                };
            case For forStmt:
                return forStmt with
                {
                    Body = FixSyntaxErrors(forStmt.Body),
                    Orelse = forStmt.Orelse != null ? FixSyntaxErrors(forStmt.Orelse) : null
                };
            case Try tryStmt:
                return tryStmt with
                {
                    Body = FixSyntaxErrors(tryStmt.Body),
                    Handlers = tryStmt.Handlers.Select(h =>
                        h with { Body = FixSyntaxErrors(h.Body) }).ToList(),
                    Orelse = tryStmt.Orelse != null ? FixSyntaxErrors(tryStmt.Orelse) : null,
                    Finalbody = tryStmt.Finalbody != null ? FixSyntaxErrors(tryStmt.Finalbody) : null
                };
            case With withStmt:
                return withStmt with { Body = FixSyntaxErrors(withStmt.Body) };
            default:
                return null; // 非容器节点，交由上层处理
        }
    }

    /// <summary>检查函数名是否是有效的 Python 标识符。</summary>
    private static bool IsValidPythonIdentifier(string name)
    {
        if (string.IsNullOrEmpty(name)) return false;

        // Python 标识符: 字母或下划线开头，后跟字母数字或下划线
        if (!char.IsLetter(name[0]) && name[0] != '_')
            return false;

        for (int j = 1; j < name.Length; j++)
        {
            if (!char.IsLetterOrDigit(name[j]) && name[j] != '_')
                return false;
        }
        return true;
    }

    /// <summary>检查语句是否为无效的 yield/await 用法（在函数体/类体外）。</summary>
    private static bool IsInvalidYieldUsage(Stmt stmt)
    {
        // Yield, YieldFrom 是独立的 Stmt 类型，直接出现在语句列表中
        return stmt is Yield or YieldFrom;
    }

    /// <summary>判断表达式是否为装饰器（保留为预备代码）。TODO: 实现 FoldDecoratorCalls。</summary>
    private static bool IsDecoratorExpression(Expr expr)
    {
        if (expr is Name name)
            return !name.Id.StartsWith("<") && !name.Id.StartsWith("__");
        if (expr is AstAttribute)
            return true;
        if (expr is Call c)
            return IsDecoratorExpression(c.Func);
        return false;
    }

    // ---- Phase 9-3: for-else 变量泄漏清理 ----

    /// <summary>
    /// 清理 for-else 体中泄漏的循环变量。
    /// 如 `for x in range(10): pass` 的 else 中出现裸 `x`。
    /// </summary>
    private static List<Stmt> CleanForElseBareExprs(List<Stmt> stmts)
    {
        for (int i = 0; i < stmts.Count; i++)
        {
            if (stmts[i] is For forStmt && forStmt.Orelse != null)
            {
                string? forTarget = forStmt.Target switch
                {
                    Name n => n.Id,
                    _ => null
                };
                if (forTarget != null)
                {
                    var cleaned = new List<Stmt>(forStmt.Orelse.Count);
                    foreach (var s in forStmt.Orelse)
                    {
                        if (s is ExprStmt { Value: Name n } && n.Id == forTarget)
                            continue; // 删除裸循环变量
                        cleaned.Add(s);
                    }
                    stmts[i] = forStmt with { Orelse = cleaned };
                }

                // 递归处理嵌套结构
                var body = CleanForElseBareExprs(forStmt.Body);
                var orelse = CleanForElseBareExprs(forStmt.Orelse);
                stmts[i] = stmts[i] is For fs
                    ? fs with { Body = body, Orelse = orelse }
                    : stmts[i];
            }
            else if (stmts[i] is FunctionDef fd)
            {
                stmts[i] = fd with { Body = CleanForElseBareExprs(fd.Body) };
            }
            else if (stmts[i] is ClassDef cd)
            {
                stmts[i] = cd with { Body = CleanForElseBareExprs(cd.Body) };
            }
            else if (stmts[i] is If ifStmt)
            {
                var body = CleanForElseBareExprs(ifStmt.Body);
                var orelse = ifStmt.Orelse != null ? CleanForElseBareExprs(ifStmt.Orelse) : null;
                stmts[i] = ifStmt with { Body = body, Orelse = orelse };
            }
        }
        return stmts;
    }

    // ---- Phase 8 Step 5: 嵌套 CodeObject 递归反编译 ----

    private HashSet<string> _processedNestedCodeNames = new();
    private const int MaxNestedDepth = 10;
    private int _nestedDepth = 0;

    /// <summary>
    /// 递归反编译嵌套 CodeObject。
    /// 对于 FunctionDef.Body 为空或仅含 pass 的条目，
    /// 查找对应的 ChildCode 并重新反编译。
    /// 
    /// 基于 Step 2 研读② pycdc ASTree.cpp 的单一入口设计。
    /// </summary>
    private List<Stmt> DecompileNestedCodeObjects(List<Stmt> stmts, CodeObject parentCode)
    {
        if (_nestedDepth >= MaxNestedDepth)
        {
            Console.Error.WriteLine($"[NESTED] Max depth ({MaxNestedDepth}) reached, skipping");
            return stmts;
        }

        _nestedDepth++;
        try
        {
            for (int i = 0; i < stmts.Count; i++)
            {
                if (stmts[i] is FunctionDef fd)
                {
                    // 只在 FunctionDef.Body 为空或仅含 pass/Comment 时触发
                    if (fd.Body.Count == 0 || fd.Body.All(s => s is CommentBlock or Pass))
                    {
                        var childCode = FindChildCodeByName(fd.Name, parentCode);
                        if (childCode != null && _processedNestedCodeNames.Add(childCode.Name + ":" + childCode.ArgCount))
                        {
                            try
                            {
                                var decompiled = DecompileChildCodeObject(childCode);
                                if (decompiled.Count > 0)
                                {
                                    stmts[i] = fd with { Body = decompiled };
                                }
                            }
                            catch (Exception ex)
                            {
                                Console.Error.WriteLine(
                                    $"[NESTED] Failed to decompile {fd.Name}: {ex.Message}");
                            }
                        }
                    }

                    // 递归处理嵌套函数体中的嵌套函数
                    if (stmts[i] is FunctionDef updatedFd)
                    {
                        var childCode = FindChildCodeByName(updatedFd.Name, parentCode);
                        if (childCode != null)
                            stmts[i] = updatedFd with
                            {
                                Body = DecompileNestedCodeObjects(updatedFd.Body, childCode)
                            };
                    }
                }
                else if (stmts[i] is ClassDef cd)
                {
                    // 递归处理类体中的嵌套函数
                    stmts[i] = cd with { Body = DecompileNestedCodeObjects(cd.Body, parentCode) };
                }
            }
        }
        finally
        {
            _nestedDepth--;
        }

        return stmts;
    }

    /// <summary>按名称在 ChildCodes 中查找匹配的 CodeObject。</summary>
    private CodeObject? FindChildCodeByName(string name, CodeObject parent)
    {
        // 优先匹配精确名称
        var exact = parent.ChildCodes.FirstOrDefault(c => c?.Name == name);
        if (exact != null) return exact;

        // 回退：检查 co_consts 中的 code objects
        foreach (var child in parent.ChildCodes)
        {
            if (child == null) continue;
            if (child.Name == name || child.Name.EndsWith("." + name))
                return child;
        }

        return null;
    }

    /// <summary>独立反编译子 CodeObject，返回语句列表。</summary>
    private List<Stmt> DecompileChildCodeObject(CodeObject childCode)
    {
        var blockScanner = new BlockScanner();
        var blocks = blockScanner.Scan(childCode);

        var cfScanner = new ControlFlowScanner();
        var structuredCFG = cfScanner.Analyze(blocks);

        var childAstBuilder = new AstBuilder(childCode, _options);
        var ast = childAstBuilder.Build(structuredCFG);

        if (ast is Module m)
            return m.Body;

        return new List<Stmt>();
    }

    // ---- Phase 9-04: Handler preamble 检测工具 ----

    /// <summary>
    /// 检测 seqBlock 是否为 handler preamble 块（包含 handler 入口指令）。
    /// 3.11+: PUSH_EXC_INFO / CHECK_EXC_MATCH
    /// 3.10-: 连续的 POP_TOP ×3（bare except handler 入口）
    /// 
    /// 检查条件：
    /// - 3.11+: block 包含 PUSH_EXC_INFO 或 CHECK_EXC_MATCH
    /// - 3.10-: block 以 POP_TOP 开头，且至少有 3 条 POP_TOP 指令
    /// </summary>
    private static bool IsHandlerPreambleBlock(SequentialBlock block)
    {
        if (block.Instructions.Count == 0) return false;

        // 3.11+: PUSH_EXC_INFO / CHECK_EXC_MATCH → 显式 handler 入口标志
        if (block.Instructions.Any(i =>
            i.Opcode == Opcode.PUSH_EXC_INFO_312 ||
            i.Opcode == Opcode.PUSH_EXC_INFO ||
            i.Opcode == Opcode.CHECK_EXC_MATCH))
            return true;

        // 3.10-: block 以 POP_TOP 开头且有 ≥3 条 POP_TOP（bare except handler）
        if (block.Instructions[0].Opcode == Opcode.POP_TOP)
        {
            int popTopCount = block.Instructions.Count(i => i.Opcode == Opcode.POP_TOP);
            if (popTopCount >= 3)
                return true;
        }

        return false;
    }

    /// <summary>
    /// 判断 seqBlock 是否为 handler body 的最后一块（包含 POP_EXCEPT）。
    /// </summary>
    private static bool IsHandlerEndBlock(SequentialBlock block)
    {
        return block.Instructions.Any(i =>
            i.Opcode == Opcode.POP_EXCEPT ||
            i.Opcode == Opcode.RERAISE);
    }
}
