using PyRebuilderSharp.Core.Models.AST;
using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.CFG;
using PyRebuilderSharp.Core.Scanners;
using PyRebuilderSharp.Core.Versioning;

namespace PyRebuilderSharp.Core.Builders;

/// <summary>
/// AST构建器 — 使用 BlockDecompiler 进行逐块反编译。
/// 对每个基本块调用 BlockDecompiler，失败块输出注释。
/// </summary>
public class AstBuilder
{
    private readonly BlockDecompiler _blockDecompiler;
    private readonly CodeObject _codeObject;
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
        var cfg = structuredCFG.RawCFG;
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
                _loopHeaderOffsets.Add(b.StartOffset);
        }

        var stmts = new List<Stmt>();
        var visited = new HashSet<BasicBlock>();

        // 3.11+: 在 BuildStatements 之前预处理 ExceptionTable try/except
        if (_codeObject.ExceptionTable.Count > 0)
        {
            // 第一步：处理 ET 条目（优先于 preBlocks，确保 visited 干净）
            foreach (var entry in _sortedExceptionTable)
            {
                var entryBlock = FindBlockByOffset(entry.StartOffset);
                if (entryBlock == null || visited.Contains(entryBlock)) continue;
                var etStmts = BuildTryFromExceptionTable(entryBlock, visited);
                if (etStmts != null)
                {
                    stmts.AddRange(etStmts);
                    foreach (var b in GetBlocksInRange(entry.StartOffset, entry.EndOffset))
                    {
                        _processedBlockIds.Add(b.Id);
                        visited.Add(b);
                    }
                    var handler = FindBlockByOffset(entry.TargetOffset);
                    if (handler != null)
                    {
                        _processedBlockIds.Add(handler.Id);
                        visited.Add(handler);
                        // Handler 后继：只处理前向边（偏移 ≥ handler 起始），且跳过自身也是 ET handler 的块
                        foreach (var succ in handler.Successors)
                        {
                            if (!visited.Contains(succ)
                                && succ.StartOffset >= entry.TargetOffset
                                && !_codeObject.ExceptionTable.Any(e => e.TargetOffset == succ.StartOffset))
                            {
                                visited.Add(succ);
                                stmts.AddRange(BuildStatements(succ, visited));
                            }
                        }
                    }
                    
                    // 标记所有共享同一 handler 的 ET 条目的 try 体块为已处理
                    // 这些是相同 try/except 结构的嵌套清理条目（depth>0），不应生成独立 try/except
                    foreach (var sibling in _sortedExceptionTable
                        .Where(e => e.TargetOffset == entry.TargetOffset && e.StartOffset != entry.StartOffset))
                    {
                        foreach (var b in GetBlocksInRange(sibling.StartOffset, sibling.EndOffset))
                        {
                            if (!visited.Contains(b))
                            {
                                _processedBlockIds.Add(b.Id);
                                visited.Add(b);
                            }
                        }
                    }
                }
            }

            // 第二步：处理第一个 ET 条目之前的块（docstring、def/class 定义等）
            var firstET = _sortedExceptionTable.First();
            var preBlocks = GetBlocksInRange(0, firstET.StartOffset)
                .Where(b => !visited.Contains(b))
                .ToList();
            foreach (var preBlock in preBlocks)
            {
                stmts.AddRange(BuildStatements(preBlock, visited));
            }

            // 第三步：处理 try 体结束与 handler 起始之间的 fall-through 块
            // 这些块是 try 体成功执行后的正常流程（如 ABCMeta 类定义等顶层声明）
            foreach (var entry in _sortedExceptionTable)
            {
                var fallthroughStart = entry.EndOffset;
                var fallthroughEnd = entry.TargetOffset;
                // 仅当 handler 在 try 体之后（前向）时处理 fall-through
                if (fallthroughEnd <= fallthroughStart) continue;

                var fallthroughBlocks = GetBlocksInRange(fallthroughStart, fallthroughEnd)
                    .Where(b => !visited.Contains(b))
                    .ToList();
                foreach (var fb in fallthroughBlocks)
                {
                    stmts.AddRange(BuildStatements(fb, visited));
                }
            }

            // 第四步：处理每个 ET 条目
            foreach (var entry in _sortedExceptionTable)
            {
                var entryBlock = FindBlockByOffset(entry.StartOffset);
                if (entryBlock == null || visited.Contains(entryBlock)) continue;

                var etStmts = BuildTryFromExceptionTable(entryBlock, visited);
                if (etStmts != null)
                {
                    stmts.AddRange(etStmts);
                    // Mark try body blocks as processed
                    foreach (var b in GetBlocksInRange(entry.StartOffset, entry.EndOffset))
                    {
                        _processedBlockIds.Add(b.Id);
                        visited.Add(b);
                    }
                    // Mark handler and successors
                    var handler = FindBlockByOffset(entry.TargetOffset);
                    if (handler != null)
                    {
                        _processedBlockIds.Add(handler.Id);
                        visited.Add(handler);
                        foreach (var succ in handler.Successors)
                        {
                            // 跳过通过 RERAISE/RAISE_VARARGS 的人工 fallthrough 边连接到类/函数定义的后继块。
                            // 这些边是 BlockScanner 为保持 CFG 连通性添加的人工边，但类/函数定义应作为
                            // try/except 后的正常代码流处理，而非 handler 的后继。
                            bool isHandlerFallthroughToDefinition = succ.Instructions.Count > 0
                                && (succ.Instructions[0].Opcode == Opcode.LOAD_BUILD_CLASS
                                    || succ.Instructions[0].Opcode == Opcode.MAKE_FUNCTION);
                            if (!visited.Contains(succ)
                                && succ.StartOffset >= entry.TargetOffset
                                && !_codeObject.ExceptionTable.Any(e => e.TargetOffset == succ.StartOffset)
                                && !isHandlerFallthroughToDefinition)
                            {
                                visited.Add(succ);
                                stmts.AddRange(BuildStatements(succ, visited));
                            }
                        }
                    }
                }
                else
                {
                    // etStmts 为 null（如 handler 已被访问），但 entry 块仍需标记为已处理
                    // 避免残余块变为孤儿
                    _processedBlockIds.Add(entryBlock.Id);
                    visited.Add(entryBlock);
                    // 同时标记 try 体中的块
                    foreach (var b in GetBlocksInRange(entry.StartOffset, entry.EndOffset))
                    {
                        if (!visited.Contains(b))
                        {
                            _processedBlockIds.Add(b.Id);
                            visited.Add(b);
                        }
                    }
                }
            }
        }
        else
        {
            // No ET: normal single-pass BuildStatements
            stmts.AddRange(BuildStatements(cfg.Entry, visited));
        }

        // 确保所有块都被处理
        // 使用 _processedBlockIds（BuildStatements 实际处理的块）而非 CollectVisited（只跟随 successor 边）
        // 防止 try/except 的 handler 块标记为 visited 导致其后缀块被静默跳过
        var unvisited = cfg.Blocks
            .Where(b => !_processedBlockIds.Contains(b.Id))
            .OrderBy(b => b.StartOffset)
            .ToList();
        
        if (unvisited.Count > 0)
        {
            Console.Error.WriteLine($"[WARN] {unvisited.Count} unprocessed blocks — recovering");

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
                        Console.Error.WriteLine($"[ORPHAN] @0x{orphan.StartOffset:X4} func={_codeObject.Name} ver={_codeObject.Version} class={classification} instrs={orphan.Instructions.Count}");
                        bool hasHandlerPreamble = classification == "handler_pre" || classification == "handler_chain";

                        if (hasHandlerPreamble)
                        {
                            _processedBlockIds.Add(orphan.Id);
                            continue;
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
                                _processedBlockIds.Add(orphan.Id);
                            continue;
                        }

                        if (!isEmptyReturn && _options.ShowOrphanBlocks)
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
                                    var lo = _allBlocks.Count > 0 ? _allBlocks[^1].EndOffset : 0;
                                    bool early = lo > 0 && orphan.StartOffset < lo / 3;
                                    if (early) stmts.InsertRange(0, recovered);
                                    else stmts.AddRange(recovered);
                                    continue;
                                }
                            }

                            // 根据偏移位置插入孤儿块内容，而非始终追加在末尾。
                            // 早期偏移的孤儿块（如函数体开头的初始化语句 `abstracts = set()`）
                            // 应出现在函数开头而非末尾。
                            var orphanStmts = new List<Stmt>
                            {
                                new CommentBlock($"# orphan @0x{orphan.StartOffset:X4}")
                            };
                            // 过滤孤儿块中的 raise 语句：这些是失去处理器上下文的不可达异常重抛，
                            // 不应出现在反编译输出中。
                            foreach (var s in blockResult.Statements)
                            {
                                if (s is Raise) continue;
                                // 过滤孤立 None 表达式（异常处理残留）
                                if (s is ExprStmt { Value: Constant { Value: null } }) continue;
                                // 过滤孤立变量引用（如 solo name / 'string' / classdict = 异常处理残留）
                                if (s is ExprStmt { Value: Name }) continue;
                                if (s is ExprStmt { Value: Constant { Value: string } }) continue;
                                orphanStmts.Add(s);
                            }

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
                Console.Error.WriteLine($"[WARN] {missed.Count} instructions not decompiled");
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
            Console.Error.WriteLine(
                $"[SUMMARY] {cfg.Blocks.Count} blocks: {processedCount} processed, " +
                $"{orphanCnt} orphan, {_codeObject.Instructions.Count} instrs");
            if (_options.ShowSummary)
                stmts.Add(new CommentBlock(
                    $"# [SUMMARY] {cfg.Blocks.Count} blocks · {processedCount} processed · " +
                    $"{orphanCnt} orphan · {_codeObject.Instructions.Count} instr"));
        }

        stmts = PostProcessFunctionDefs(stmts);
        // Fallback: position-based ChildCode matching
        stmts = ConvertChildCodesToFunctionDefs(stmts);
        
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
        stmts = stmts.Where(s => !(s is Return ret && ret.Value is Constant { Value: null })).ToList();
        
        // Convert __doc__ = '...' to bare docstring (ExprStmt with string constant)
        stmts = ConvertDocstring(stmts);
        
        // Convert i = i + 1 to i += 1 (augmented assignment)
        stmts = ConvertAugAssign(stmts);
        
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
                result.Add(new FunctionDef(
                    funcDef.Name, funcDef.Args,
                    ConvertAugAssign(funcDef.Body),
                    funcDef.Decorators,
                    funcDef.Returns,
                    funcDef.IsGenerator, funcDef.IsAsync));
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
            _processedBlockIds.Add(block.Id);
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
            stmts.AddRange(BuildLoop(block, visited));
            foreach (var succ in block.Successors)
            {
                if (!visited.Contains(succ))
                    stmts.AddRange(BuildStatements(succ, visited));
            }
            return stmts;
        }

        // 检测 for-loop 头：FOR_ITER 是条件跳转但不是 if/else，
        // 即使 LoopHeader 标志未设置
        if (block.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
        {
            var loopAst = BuildForLoop(block, visited);
            stmts.AddRange(loopAst);
            // 处理循环出口块的后继（如循环后的顺序代码）
            // exit = 偏移较大的 successor（跳转目标），body = 偏移较小的 successor（fallthrough）
            var bodySorter = block.Successors.Where(s => s != null).OrderBy(s => s.StartOffset).ToList();
            var bodyEntry = bodySorter.FirstOrDefault();
            foreach (var succ in block.Successors)
            {
                if (succ == null) continue;
                // 跳过 body 块（已在 BuildForLoop 中被 GetStructuredBlockStmts 处理）
                if (succ == bodyEntry) continue;
                // exit 块可能已被 body 块的后继检测误加入 visited，移除以确保处理
                if (visited.Contains(succ))
                    visited.Remove(succ);
                stmts.AddRange(BuildStatements(succ, visited));
            }
            return stmts;
        }

        // 检测 with 语句 (SETUP_WITH / BEFORE_WITH 模式)
        var withStmts = BuildWithFromBlock(block, visited);
        if (withStmts != null)
        {
            stmts.AddRange(withStmts);
            // 标记 SETUP_WITH 的 handler 块为 visited
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

        // 检测 try/except (SETUP_FINALLY 模式)
        var tryBodyStmts = BuildTryFromBlock(block, visited);
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
        if (_codeObject.ExceptionTable.Count > 0)
        {
            if (_codeObject.Name == "<module>" && !_diagETPrinted)
            {
                _diagETPrinted = true;
            }
            var try311Stmts = BuildTryFromExceptionTable(block, visited);
            if (try311Stmts != null)
            {
                stmts.AddRange(try311Stmts);
                // 继续处理 try/except 后面的块（else 分支、类定义等）
                var firstTry = try311Stmts.FirstOrDefault() as Try;
                if (firstTry != null && firstTry.Orelse != null)
                {
                    // Orelse 已在 BuildTryFromExceptionTable 中填充，无需额外处理
                }
                else
                {
                    // 处理 handler 块的后缀块（类定义等在 try/except 之后的代码）
                    var matchingEntry = _codeObject.ExceptionTable
                        .FirstOrDefault(e => block.Instructions.Count > 0
                            && block.Instructions[0].Offset >= e.StartOffset
                            && block.Instructions[0].Offset < e.EndOffset);
                    if (matchingEntry != null)
                    {
                        var handlerBlock = FindBlockByOffset(matchingEntry.TargetOffset);
                        if (handlerBlock != null)
                        {
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
                return stmts;
            }
            
            // 检测 match/case
            var matchStmts = BuildMatchFromExceptionTable(block, visited);
            if (matchStmts != null)
            {
                stmts.AddRange(matchStmts);
                return stmts;
            }
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

        // 检查是否为条件分支
        if (IsConditionBranch(block))
        {
            stmts.AddRange(BuildIfElse(block, visited));
            return stmts;
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

        // 递归处理后继块
        foreach (var succ in block.Successors.OrderBy(s => s.StartOffset))
        {
            if (!visited.Contains(succ))
                stmts.AddRange(BuildStatements(succ, visited));
        }

        return stmts;
    }

    private List<Stmt> BuildLoop(BasicBlock header, HashSet<BasicBlock> visited)
    {
        bool isForLoop = header.Instructions.Any(i =>
            i.Opcode == Opcode.GET_ITER || i.Opcode == Opcode.FOR_ITER);

        if (isForLoop)
            return BuildForLoop(header, visited);
        else
            return BuildWhileLoop(header, visited);
    }

    private List<Stmt> BuildForLoop(BasicBlock header, HashSet<BasicBlock> visited)
    {
        // 确保 header 在 visited 中，防止从 GetStructuredBlockStmts 调入时
        // body 块的后继 FOR_ITER 被再次检测导致递归循环
        visited.Add(header);
        _processedBlockIds.Add(header.Id);
        var iterExpr = ExtractIterExpression(header);

        var bodyBlocks = new List<BasicBlock>();
        // FOR_ITER 的后继：[fallthrough body, jump-to-exit]
        // 取第一个后继作为 body（fallthrough），跳过 exit 路径
        var bodyEntry = header.Successors
            .OrderBy(s => s.StartOffset)
            .FirstOrDefault();
        var exitBlock = header.Successors
            .OrderByDescending(s => s.StartOffset)
            .FirstOrDefault(b => b != bodyEntry);
        if (bodyEntry != null)
        {
            CollectBodyBlocks(bodyEntry, header, bodyBlocks, visited, exitBlock);
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

        var target = ExtractLoopVariable(header, bodyBlocks);

        // 处理 body 中可能残留的循环变量赋值（STORE_NAME/STORE_FAST 因栈不完整产生无效 Assign）
        // FOR_ITER 的栈效果在前驱块，body 块中单独的 STORE 会产生 Assign(target, null)
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

        // 移除 body 末尾的 continue（JUMP_ABSOLUTE 回到 FOR_ITER 产生）
        while (bodyStmts.Count > 0 && bodyStmts[^1] is Continue)
            bodyStmts.RemoveAt(bodyStmts.Count - 1);

        return new List<Stmt> { new For(target, iterExpr, bodyStmts, null) };
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

        // Collect blocks from first until StartOffset >= endExclusive
        var result = new List<BasicBlock>();
        for (int i = first; i < list.Count; i++)
        {
            if (list[i].Instructions[0].Offset >= endExclusive)
                break;
            result.Add(list[i]);
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
        var localVisited = new HashSet<BasicBlock>();

        while (currentBlock != null && !localVisited.Contains(currentBlock)
            && currentBlock.Instructions.Count >= 3
            && currentBlock.Instructions.Any(i => i.Opcode == Opcode.COPY))
        {
            localVisited.Add(currentBlock);
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
            if (nextCaseBlock == null || !localVisited.Add(nextCaseBlock))
                nextCaseBlock = null;

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
        var instrs = block.Instructions;
        if (instrs.Count == 0) return null;
        var blockStart = instrs[0].Offset;
        var blockEnd = instrs.Last().Offset;

        // Find the outermost entry that covers this block (lowest depth = 0 or 1 first)
        var matchingEntry = _codeObject.ExceptionTable
            .Where(e => blockStart >= e.StartOffset && blockEnd <= e.EndOffset)
            .OrderBy(e => e.Depth)
            .FirstOrDefault();
        if (matchingEntry == null)
        {
            return null;
        }

        // 3.11+ for 循环体有隐式 ET 条目（清理/异常安全），
        // 应跳过 try/except 检测 — for 循环已有独立块处理。
        bool isForLoopBody = _codeObject.Instructions
            .Any(i => i.Opcode == Opcode.FOR_ITER && i.Argument.HasValue
                && i.Argument.Value == matchingEntry.StartOffset);
        if (isForLoopBody)
        {
            return null;
        }

        var handlerBlock = FindBlockByOffset(matchingEntry.TargetOffset);
        if (handlerBlock == null || visited.Contains(handlerBlock))
        {
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
            if (tryBlocks.Count == 0) return null;
        }

        var tryBody = new List<Stmt>();
        var tryVisited = new HashSet<BasicBlock>();
        foreach (var tb in tryBlocks)
        {
            if (tb == block)
            {
                var result = _blockResults.GetValueOrDefault(block.Id);
                if (result?.Statements != null)
                {
                    var filtered = result.Statements.Where(s => s is not Raise).ToList();
                    if (filtered.Count > 0)
                        tryBody.AddRange(filtered);
                }
            }
            else if (!visited.Contains(tb) && !tryVisited.Contains(tb))
            {
                tryBody.AddRange(BuildStatements(tb, visited));
            }
        }

        // 跳过仅有基础设施指令（Raise/异常处理）的 try 体
        // 这些是 CPython 嵌套清理条目，不应生成独立 try/except
        if (tryBody.Count == 0 && tryBlocks.All(tb =>
        {
            var r = _blockResults.GetValueOrDefault(tb.Id);
            return r?.Statements == null || r.Statements.All(s => s is Raise or ExprStmt);
        }))
        {
            return null;
        }

        visited.Add(handlerBlock);
        var handlerResult = _blockResults.GetValueOrDefault(handlerBlock.Id);
        var handlerBody = handlerResult?.Statements
            ?.Where(s => s is not Raise and not CommentBlock)
            .ToList() ?? new List<Stmt>();

        // Collect body from all handler successor blocks within the handler range
        // Handler range = from handler target to the EndOffset of the ET entry covering it
        var handlerET = _codeObject.ExceptionTable
            .FirstOrDefault(e => e.StartOffset == matchingEntry.TargetOffset);
        var handlerEnd = handlerET != null
            ? handlerET.EndOffset
            : matchingEntry.EndOffset;
        foreach (var succ in handlerBlock.Successors.OrderBy(s => s.StartOffset))
        {
            if (succ.Instructions.Count == 0) continue;
            var succStart = succ.Instructions[0].Offset;
            if (succStart >= matchingEntry.TargetOffset && succStart < handlerEnd
                && !visited.Contains(succ))
            {
                // 跳过类/函数定义块 — 这些是结构边界，不是 handler 后继体
                bool isDefBlock = succ.Instructions.Any(i =>
                    i.Opcode == Opcode.MAKE_FUNCTION
                    || i.Opcode == Opcode.MAKE_CLOSURE
                    || i.Opcode == Opcode.LOAD_BUILD_CLASS);
                if (isDefBlock) continue;

                var succResult = _blockResults.GetValueOrDefault(succ.Id);
                if (succResult?.Statements != null)
                {
                    handlerBody.AddRange(succResult.Statements
                        .Where(s => s is not Raise and not CommentBlock));
                }
                visited.Add(succ);
                _processedBlockIds.Add(succ.Id);
            }
        }

        bool isGroup = handlerBlock.Instructions.Any(i => i.Opcode == Opcode.CHECK_EG_MATCH);

        Expr? exceptType = null;
        string? exceptName = null;
        for (int i = 0; i < handlerBlock.Instructions.Count; i++)
        {
            var ins = handlerBlock.Instructions[i];
            if (ins.Opcode == Opcode.CHECK_EXC_MATCH || ins.Opcode == Opcode.CHECK_EG_MATCH)
            {
                if (i > 0)
                {
                    var typeLoad = handlerBlock.Instructions[i - 1];
                    if (typeLoad.Opcode == Opcode.LOAD_NAME)
                    {
                        var name = _codeObject.Names.ElementAtOrDefault(typeLoad.Argument ?? 0);
                        if (name != null) exceptType = new Name(name);
                    }
                }
                break;
            }
            if (ins.Opcode == Opcode.STORE_NAME)
                exceptName = _codeObject.Names.ElementAtOrDefault(ins.Argument ?? 0);
        }

        var handlers = new List<ExceptHandler>
        {
            new ExceptHandler(exceptType, exceptName, handlerBody, isGroup)
        };

        foreach (var succ in handlerBlock.Successors)
        {
            if (!visited.Contains(succ) && succ.StartOffset <= matchingEntry.EndOffset)
            {
                // 同样跳过类/函数定义块
                bool isDefBlock = succ.Instructions.Any(i =>
                    i.Opcode == Opcode.MAKE_FUNCTION
                    || i.Opcode == Opcode.MAKE_CLOSURE
                    || i.Opcode == Opcode.LOAD_BUILD_CLASS);
                if (!isDefBlock)
                    visited.Add(succ);
            }
        }

        return new List<Stmt> { new Try(tryBody, handlers) };
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
        // 优先从 tryBodyBlocks 中找，如果为空则从当前 block 中找
        var popBlockBlock = tryBodyBlocks.Count > 0
            ? tryBodyBlocks.LastOrDefault(b =>
                b.Instructions.Any(i => i.Opcode == Opcode.POP_BLOCK))
            : block;
        // 当前块也可能包含 POP_BLOCK + JUMP_FORWARD（try body 在单块内）
        if (popBlockBlock != null)
        {
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

        // 提取 handler body 语句
        var handlerInstrs = new List<Instruction>();
        bool handlerFound = false, seenBody = false, isFinally = false;
        foreach (var hb in handlerBlocks)
        {
            if (handlerFound) break;
            foreach (var ins in hb.Instructions)
            {
                if (ins.Opcode == Opcode.POP_EXCEPT)
                {
                    handlerFound = true;
                    break;
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
                if (ins.Opcode is Opcode.JUMP_FORWARD or Opcode.JUMP_ABSOLUTE)
                    continue;
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
        if (handlerBody.Count == 0)
            handlerBody.Add(new Pass());

        // 检测 handler 类型：except（以 DUP_TOP 或 POP_TOP×3 开头）还是 finally（无两者）
        bool isExceptHandler = false;
        int topCount = 0;
        foreach (var hb in handlerBlocks)
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
            foreach (var hb in handlerBlocks)
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
                // else body 在 POP_BLOCK 之后、handler 之前。
                // 收集 from=elseJumpTarget(=after_all) 是错的，它指向 handler 之后。
                // 正确做法：从 popBlockBlock 的后继中找 offset < handlerAbs 的块
                var elseBlocks = new List<BasicBlock>();
                // 从 POP_BLOCK 块的后继开始（不在 handler 区域内）
                foreach (var succ in (popBlockBlock ?? block).Successors)
                {
                    if (succ == null || succ.StartOffset >= handlerAbs)
                        continue;
                    if (succ.StartOffset < (instrs[setupIdx].Offset + 2))
                        continue;
                    // 跳过 handler 入口块
                    if (succ.Id == (handlerEntryBlock?.Id ?? -1))
                        continue;
                    elseBlocks.Add(succ);
                }
                if (elseBlocks.Count > 0)
                {
                    var elseStmts = new List<Stmt>();
                    foreach (var eb in elseBlocks)
                    {
                        var ebInstrs = eb.Instructions
                            .Where(i => i.Opcode != Opcode.RETURN_VALUE
                                && i.Opcode != Opcode.RERAISE)
                            .ToList();
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
                        // 将 else 块标记为已访问，防止外部重复处理
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
        var withIdx = setupIdx >= 0 ? setupIdx : beforeWithIdx;
        if (withIdx < 0) return null;
        bool isSetupWith = setupIdx >= 0;

        // 1. 提取 with 之前的上下文表达式
        var preMachine = new StackMachine(_codeObject);
        for (int i = 0; i < withIdx; i++)
        {
            var stmt = preMachine.Execute(instrs[i]);
        }

        Expr? contextExpr = preMachine.ExprStackCount > 0 ? preMachine.PopExpr() : null;
        if (contextExpr == null) return null;

        // 2. 提取可选的 as 变量
        Expr? optionalVar = null;
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

        // 3. 确定 handler 起始偏移和 body 范围
        int handlerAbs;
        if (isSetupWith)
        {
            // pre-3.11: SETUP_WITH arg = handler offset (in wordcode units)
            var handlerRel = instrs[setupIdx].Argument ?? 0;
            handlerAbs = instrs[setupIdx].Offset + 2 + handlerRel * 2;
        }
        else
        {
            // 3.11+: 用 ExceptionTable 找 WITH_EXCEPT_START handler 的起始偏移
            handlerAbs = -1;
            if (_codeObject.ExceptionTable != null)
            {
                var blockStart = instrs[0].Offset;
                var blockEnd = instrs[^1].Offset;
                var withET = _codeObject.ExceptionTable
                    .FirstOrDefault(e => e.TargetOffset > blockStart
                        && e.TargetOffset < blockEnd + 4);
                if (withET != null)
                    handlerAbs = withET.TargetOffset;
            }
            if (handlerAbs < 0) return null; // no ET entry found
        }

        // 4. 跳过变量赋值找到 body 起始
        int bodyStart = withIdx + 1;
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

        // 5. 处理当前块内的 body 指令
        var bodyStmts = new List<Stmt>();
        var bodyMachine = new StackMachine(_codeObject);
        for (int i = bodyStart; i < instrs.Count; i++)
        {
            if (isSetupWith && instrs[i].Opcode == Opcode.POP_BLOCK)
                break;
            if (!isSetupWith)
            {
                // 3.11+: 遇到 handler 起始或 cleanup 前停止
                if (instrs[i].Opcode == Opcode.WITH_EXCEPT_START) break;
                if (instrs[i].Offset >= handlerAbs && handlerAbs > 0) break;
            }
            var stmt = bodyMachine.Execute(instrs[i]);
            if (stmt != null) bodyStmts.Add(stmt);
        }
        while (bodyMachine.HasResults)
            bodyStmts.Add(new ExprStmt(bodyMachine.PopResult()));

        // 6. 收集后继块作为 body
        var bodyBlocks = new List<BasicBlock>();
        var bodyCollector = new HashSet<BasicBlock> { block };
        var blockQueue = new Queue<BasicBlock>();
        foreach (var succ in block.Successors.OrderBy(s => s.StartOffset))
        {
            if (succ == null || succ.StartOffset >= handlerAbs || bodyCollector.Contains(succ))
                continue;
            if (succ.StartOffset < instrs[withIdx].Offset + 2) continue;
            blockQueue.Enqueue(succ);
        }
        while (blockQueue.Count > 0)
        {
            var current = blockQueue.Dequeue();
            if (current == null || bodyCollector.Contains(current)) continue;
            if (current.StartOffset >= handlerAbs) continue;
            bodyCollector.Add(current);
            bodyBlocks.Add(current);
            foreach (var succ in current.Successors)
            {
                if (succ != null && !bodyCollector.Contains(succ) && succ.StartOffset < handlerAbs)
                    blockQueue.Enqueue(succ);
            }
        }

        foreach (var bb in bodyBlocks)
            visited.Remove(bb);
        foreach (var bodyBlock in bodyBlocks)
            bodyStmts.AddRange(GetStructuredBlockStmts(bodyBlock, visited));

        // 标记 handler 块为 visited
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
            testExpr = ExtractCondition(header);
        }

        var bodyBlocks = new List<BasicBlock>();
        // body entry = 第一个后继（fallthrough），exit = 第二个后继（jump target）
        // 注意：不能按 offset 排序取 FirstOrDefault，因为跳转目标可能比 body 偏移小（v3.8+）
        // 正确做法：从 header 的 POP_JUMP 指令获取跳转目标偏移，排除该块后余下的就是 body
        var lastInstr = header.Instructions.LastOrDefault();
        BasicBlock? bodyEntry = null;
        if (lastInstr != default && lastInstr.Argument.HasValue)
        {
            var jumpTargetOffset = lastInstr.Argument.Value;
            // body entry = 不是跳转目标的 successor
            bodyEntry = header.Successors.FirstOrDefault(s => s.StartOffset != jumpTargetOffset);
        }
        bodyEntry ??= header.Successors.OrderBy(s => s.StartOffset).FirstOrDefault();
        if (bodyEntry != null)
            CollectBodyBlocks(bodyEntry, header, bodyBlocks, visited);

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
            foreach (var bodyBlock in bodyBlocks)
            {
                var stmts = GetStructuredBlockStmts(bodyBlock, visited);
                bodyStmts.AddRange(stmts);
            }
        }

        return new List<Stmt> { new While(testExpr, bodyStmts, null) };
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
    private List<Stmt> BuildWhileLoopBody(BasicBlock header, HashSet<BasicBlock> visited)
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

        // 非自循环：从 header 的后继中收集 LoopBody 块
        var bodyBlocks = new List<BasicBlock>();
        var localSeen = new HashSet<BasicBlock>();
        foreach (var succ in header.Successors)
        {
            // 只收集 LoopBody 标记的块，避免越界
            if (succ != header && succ.Flags.HasFlag(BlockFlags.LoopBody))
                CollectBodyBlocksFrom(succ, header, bodyBlocks, localSeen);
        }

        // 如果 header 自身也包含条件分支（if/else 在 while 体内），
        // 用 block 结果 + 后继分支处理，避免 GetStructuredBlockStmts 递归循环头
        if (IsConditionBranch(header) && header.Instructions.Count > 1)
        {
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
            var sortedSucc = header.Successors
                .Where(s => s.Flags.HasFlag(BlockFlags.LoopBody))
                .OrderBy(s => s.StartOffset)
                .ToList();
            
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
    /// 从起始块收集 LoopBody 块，用局部 visited 防止越界。
    /// </summary>
    private void CollectBodyBlocksFrom(BasicBlock entry, BasicBlock header,
        List<BasicBlock> bodyBlocks, HashSet<BasicBlock> localSeen)
    {
        var worklist = new Queue<BasicBlock>();
        worklist.Enqueue(entry);
        while (worklist.Count > 0)
        {
            var current = worklist.Dequeue();
            if (current == header || localSeen.Contains(current))
                continue;
            if (!current.Flags.HasFlag(BlockFlags.LoopBody))
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
    /// 检测 body 链是否以终端指令结束（RETURN/RAISE）。
    /// 只检测 body 入口块本身的最后指令，不沿路径追踪（避免走到 after 代码区）。
    /// </summary>
    private bool BodyEndsWithTerminal(BasicBlock entry)
    {
        if (entry == null) return false;
        var lastIns = entry.Instructions.LastOrDefault();
        return lastIns != default && JumpHelper.IsTerminal(lastIns.Opcode);
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
                headerInitStmts.Add(s);
            }
        }

        var testExpr = ExtractCondition(header);
        if (header.Instructions.Count == 0) return new List<Stmt>();
        var lastInstr = header.Instructions.Last();
        // 3.12+ wordcode
        var targetOffset = lastInstr.Argument!.Value;
        var isWordcode = _codeObject.Instructions.Count > 1
                      && _codeObject.Instructions.All(i => i.Offset % 2 == 0);
        // 3.10 特殊处理：ParseInstructionsWordcode 已将 arg *2 转为绝对字节偏移
        // 3.11+ wordcode: arg 是相对字节偏移，需加上 current_offset + 2
        // 3.13+: PycReader 已解析为绝对字节偏移（见 PycReader.ParseInstructions311Plus）
        if (isWordcode
            && lastInstr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38
            && _codeObject.Version != PythonVersion.Py310
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
        }
        
        // 检测 OR 短接链: POP_JUMP_IF_TRUE + fallthrough 为条件分支
        // if a or b: bytecode = "POP_JUMP_IF_TRUE → body ; POP_JUMP_IF_FALSE → after"
        bool isOrChain = isJumpIfTrue && bodyBranch != null && IsConditionBranch(bodyBranch);
        if (!isOrChain && isJumpIfTrue && testExpr != null)
            testExpr = new UnaryOp(UnaryOperator.Not, testExpr);

        // OR 短接: POP_JUMP_IF_TRUE + fallthrough 为条件分支
        if ((isOrChain || lastInstr.Opcode is Opcode.JUMP_IF_TRUE_OR_POP) && afterBranch != null)
        {
            // body 在 jump target (afterBranch), else 是 fallthrough (bodyBranch = 第二条件)
            var savedBody = bodyBranch;
            bodyBranch = afterBranch;   // body = print
            afterBranch = savedBody;    // else = 第二条件检查
        }

        // 检测 while 循环模式：bodyBranch 是循环头（LoopHeader）
        // 在 Python 3.10 中，while 循环的条件在前驱块，body 是独立的 LoopHeader
        // 排除 for-loop 头（有 GET_ITER/FOR_ITER 指令的 LoopHeader），for-loop 走 GetStructuredBlockStmts
        var isForLoop = bodyBranch != null && bodyBranch.Instructions.Any(
            i => i.Opcode is Opcode.GET_ITER or Opcode.FOR_ITER);
        if (bodyBranch != null && bodyBranch.Flags.HasFlag(BlockFlags.LoopHeader) && !isForLoop)
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
            // 构建 while 体
            var wBody = BuildWhileLoopBody(bodyBranch, visited);
            var wAfter = afterBranch != null && !visited.Contains(afterBranch)
                ? BuildStatements(afterBranch, visited)
                : null;
            var wResult = new List<Stmt>();
            wResult.AddRange(initStmts);
            wResult.Add(new While(whileTest, wBody, null));
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
            // afterBranch 通过条件跳转到达，可能已被 CFG 误加入 visited（如 RAISE 块的伪后继）。
            // 重新允许 else 子句检测。
            if (visited.Contains(afterBranch))
                visited.Remove(afterBranch);

            // 检测是否为 else 子句（非 elif 链）
            // 条件：after 块的任意前驱是条件块（即通过条件跳转到达），
            // 且 body 不以非条件跳转结尾
            bool isElseClause = false;
            if (bodyBranch != null && afterBranch != null)
            {
                // afterBranch 是 else 子句的条件：
                // (1) body 以终端指令结尾（不能 fallthrough 到 afterBranch）
                // (2) afterBranch 不含条件跳转指令（不是 elif 链的一部分）
                bool bodyEndsWithTerminal = bodyStmts.Count > 0
                    && bodyStmts[^1] is Return or Raise or Break or Continue;
                bool isConditionBlock = afterBranch.Instructions.Any(i =>
                    i.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                        or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                        or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38);
                isElseClause = bodyEndsWithTerminal && !isConditionBlock;
            }

            if (isElseClause)
            {
                // 用 BuildBlockOnly 只取 else 块本身的语句（不追踪后继）
                var elseBody = BuildBlockOnly(afterBranch, visited);
                orelse = elseBody
                    .Where(s => !(s is Return ret && ret.Value is Constant { Value: null }))
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
            var ifChain = afterStmts.TakeWhile(s => s is If).ToList();
            if (ifChain.Count > 0)
            {
                orelse = ifChain; // elif 链
            }
            else
            {
                // 非 If 语句：检测是否为 else 子句
                // 条件：after 块的唯一前驱是条件块（POP_JUMP_IF_FALSE 目标）
                // 且 body 链不以 RETURN/RAISE 结尾（否则不会 JUMP 跳过）
                bool isElseClause = false;
                if (afterBranch != null && bodyBranch != null)
                {
                    isElseClause = afterBranch.Predecessors.Count == 1
                        && afterBranch.Predecessors.Contains(header)
                        && !BodyEndsWithTerminal(bodyBranch);
                }

                if (isElseClause)
                {
                    // 过滤 orelse 中的 module-level return None
                    orelse = afterStmts
                        .Where(s => !(s is Return ret && ret.Value is Constant { Value: null }))
                        .ToList();
                    if (orelse.Count == 0) orelse = null;
                }
                else
                {
                    // 非 If 的尾部，过滤 return None
                    foreach (var s in afterStmts)
                        if (!(s is Return ret && ret.Value is Constant { Value: null }))
                            tailCode.Add(s);
                }
            }
            }

        var result = new List<Stmt>();
        result.AddRange(headerInitStmts);

        // 优化: 条件为 Constant(true) 时跳过 If，直接内联 body
        if (testExpr is Constant { Value: bool tv } && tv)
        {
            result.AddRange(bodyStmts);
            result.AddRange(tailCode);
            return result;
        }

        // AND 短接合并: POP_JUMP_IF_FALSE/JUMP_IF_FALSE_OR_POP + body 首条为 If → BoolOp(And, ...)
        if ((lastInstr.Opcode is Opcode.POP_JUMP_IF_FALSE or Opcode.JUMP_IF_FALSE_OR_POP
                or Opcode.POP_JUMP_IF_FALSE_PY38)
            && bodyStmts.Count > 0 && bodyStmts[0] is If innerIf && orelse == null)
        {
            var mergedTest = MergeBoolOpValues(BoolOperator.And, new List<Expr> { testExpr, innerIf.Test });
            result.Add(new If(mergedTest, innerIf.Body, innerIf.Orelse));
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
        else
        {
            result.Add(new If(testExpr, bodyStmts, orelse));
        }
        result.AddRange(tailCode);
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
        return result.Statements;
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
            bool hasForIter = block.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER);
            bool hasGetIter = block.Instructions.Any(i => i.Opcode == Opcode.GET_ITER);
            if (!(hasGetIter && !hasForIter))
                return BuildLoop(block, visited);
        }

        // 检测 for-loop 头：FOR_ITER 是条件跳转但不是 if/else，
        // 即使 LoopHeader 标志未设置（当 for-loop 的 GET_ITER 在另一个块中时）
        if (block.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
        {
            return BuildForLoop(block, visited);
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
        if (_codeObject.ExceptionTable != null && _codeObject.ExceptionTable.Count > 0)
        {
            var etTry = BuildTryFromExceptionTable(block, visited);
            if (etTry != null)
                return etTry;
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
        if (forLoopHeader != null && !visited.Contains(forLoopHeader))
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
        var testExpr = ExtractCondition(header);
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
        if (bodyStmts.Count == 0 && bodyBranch != null)
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
                    // JUMP_BACKWARD 总是向后跳转（相对于自身偏移）
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
            var ifChain = afterStmts.TakeWhile(s => s is If).ToList();
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
        bool bodyIsJustContinue = bodyStmts.Count == 1 && bodyStmts[0] is Continue;
        if (bodyIsJustContinue && orelse != null && orelse.Count > 0)
        {
            bodyStmts = orelse;
            orelse = null;
            // 移除否定：重新提取原始条件（不经过 isJumpIfTrue 的 Not 包装）
            testExpr = ExtractCondition(header);
        }

        var result = new List<Stmt> { new If(testExpr, bodyStmts, orelse) };
        result.AddRange(tailCode);
        return result;
    }

    private Expr ExtractCondition(BasicBlock block)
    {
        if (block.Instructions.Count == 0)
            return new Constant(true);
            
        var conditionInstrs = block.Instructions
            .Take(block.Instructions.Count - 1)
            .ToList();

        var stackMachine = new StackMachine(_codeObject);
        foreach (var instr in conditionInstrs)
            stackMachine.Execute(instr);

        if (stackMachine.ExprStackCount > 0)
            return stackMachine.PopExpr();
            
        // elif 模式：COMPARE_OP 因缺少 subject（已在之前块中 COPY）而返回 null。
        // 从前驱块中复制 subject，用扩展指令列表重新构造比较表达式。
        if (stackMachine.ExprStackCount == 0 && stackMachine.HasResults == false && conditionInstrs.Count > 0
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
                        return sm2.PopExpr();
                }
            }
        }
        
        return stackMachine.HasResults ? stackMachine.PopResult() : new Constant(true);
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
        int forIterIdx = _codeObject.Instructions.FindIndex(i =>
            i.Opcode == Opcode.FOR_ITER
            && i.Offset >= header.StartOffset
            && i.Offset <= header.EndOffset);
        if (forIterIdx > 0)
        {
            int getIterIdx = -1;
            for (int i = forIterIdx - 1; i >= 0; i--)
            {
                var op = _codeObject.Instructions[i].Opcode;
                if (op == Opcode.GET_ITER) { getIterIdx = i; break; }
                if (JumpHelper.IsJump(op) || op == Opcode.RETURN_VALUE
                    || op == Opcode.RAISE_VARARGS)
                    break;
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

                if (startIdx < getIterIdx)
                {
                    var iterBuilder = _codeObject.Instructions.GetRange(startIdx, getIterIdx - startIdx);
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
                        if (expr != null) return expr;
                    }
                }
            }
        }

        // Fallback 3: header's own instructions before FOR_ITER
        var iterInstrs = header.Instructions
            .TakeWhile(i => i.Opcode != Opcode.FOR_ITER)
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

                if ((instr.Opcode == Opcode.STORE_FAST || instr.Opcode == Opcode.STORE_NAME
                        || instr.Opcode == Opcode.STORE_DEREF)
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
                        // and len(varnames) + freevar_index for free variables
                        if (idx < _codeObject.Varnames.Count)
                            varName = _codeObject.Varnames[idx];
                        else if (idx - _codeObject.Varnames.Count < _codeObject.Freevars.Count)
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
            else if (instr.Opcode == Opcode.STORE_DEREF && instr.Argument.HasValue)
            {
                int idx = instr.Argument.Value;
                string cellName;
                // CPython 3.12+ STORE_DEREF uses varname index for cell variables,
                // and len(varnames) + freevar_index for free variables
                if (idx < _codeObject.Varnames.Count)
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
        bool hasHandlerPre = instrs.Any(i =>
            i.Opcode == Opcode.DUP_TOP || i.Opcode == Opcode.POP_EXCEPT
            || i.Opcode == Opcode.END_FINALLY || i.Opcode == Opcode.JUMP_IF_NOT_EXC_MATCH
            || i.Opcode == Opcode.CHECK_EXC_MATCH || i.Opcode == Opcode.CHECK_EG_MATCH
            || i.Opcode == Opcode.RERAISE);
        if (hasHandlerPre) return "handler_pre";
        if (instrs.Any(i => i.Opcode == Opcode.JUMP_BACKWARD || i.Opcode == Opcode.JUMP_BACKWARD_NO_INTERRUPT))
            return "jump_back_loop";
        if (instrs.Any(i => i.Opcode == Opcode.FOR_ITER)) return "for_iter";
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
        BasicBlock? exitBlock = null)
    {
        var worklist = new Queue<BasicBlock>();
        worklist.Enqueue(entry);

        while (worklist.Count > 0)
        {
            var current = worklist.Dequeue();
            if (current == header || visited.Contains(current))
                continue;
            // 排除循环出口块（FOR_ITER 的跳转目标），防止收集到循环后代码
            if (exitBlock != null && current == exitBlock)
                continue;

            bodyBlocks.Add(current);
            visited.Add(current);

            // v3.10: 回边条件块（POP_JUMP_IF_TRUE 目标 < 自身偏移）的后继是循环出口，不是 body 的一部分
            // 3.12+ wordcode: 使用解析后的目标偏移，否则 wordcode arg（已 *2）总是 < 块偏移
            var lastInstr = current.Instructions.LastOrDefault();
            // 3.12+ wordcode: 使用解析后的目标偏移，否则 wordcode arg（已 *2）总是 < 块偏移
            int resolvedBackEdge = int.MaxValue;
            if (lastInstr != default && lastInstr.Argument.HasValue)
            {
                var iwc = _codeObject.Instructions.Count > 1
                       && _codeObject.Instructions.All(i => i.Offset % 2 == 0);
                resolvedBackEdge = lastInstr.Opcode switch
                {
                    Opcode.JUMP_ABSOLUTE => lastInstr.Argument.Value,
                    Opcode.JUMP_FORWARD or Opcode.FOR_ITER => lastInstr.Offset + 2 + lastInstr.Argument.Value,
                    Opcode.JUMP_BACKWARD => lastInstr.Offset + 2 - lastInstr.Argument.Value,
                    Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                        or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                        when iwc => lastInstr.Offset + 2 + lastInstr.Argument.Value,
                    _ => lastInstr.Argument.Value
                };
            }
            bool isBackEdgeBlock = lastInstr != default
                && JumpHelper.IsJump(lastInstr.Opcode)
                && lastInstr.Argument.HasValue
                && resolvedBackEdge < current.StartOffset;

            foreach (var succ in current.Successors)
            {
                if (succ != header && !visited.Contains(succ))
                {
                    // 回边块的 fallthrough 是循环出口
                    if (isBackEdgeBlock)
                        continue;
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
                    if (assign.Value is Call call && call.Func is Name callFuncName && callFuncName.Id == "__build_class__")
                    {
                        if (!seenNames.Add(targetName.Id))
                        {
                            // 替换已存在的重复定义（保留最后一个，通常是正确的版本）
                            Console.Error.WriteLine($"[DEDUP] ClassDef '{targetName.Id}' replaced at line {currentResult.Count}");
                            // 搜索 FunctionDef 或 ClassDef
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
                        var classDef = ExtractClassDef(call, targetName.Id);
                        currentResult.Add(classDef ?? stmt);
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
                    if (assign.Value is Call decoratorCall && decoratorCall.Args.Count == 1
                        && decoratorCall.Args[0] is FunctionRef)
                    {
                        BuildFunctionDefWithDecorators(targetName, decoratorCall, currentResult);
                        continue;
                    }
                    if (assign.Value is Call outerCall && outerCall.Args.Count == 1
                        && outerCall.Args[0] is Call innerCall && innerCall.Args.Count == 1
                        && innerCall.Args[0] is FunctionRef)
                    {
                        BuildFunctionDefWithDecorators(targetName, outerCall, currentResult);
                        continue;
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
            
            var funcDef = BuildFunctionDef(cleanName, funcRef);
            if (funcDef != null)
            {
                // Recreate FunctionDef with decorators
                result.Add(funcDef with { Decorators = decorators });
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

        // 过滤 class body 中的 __module__ / __qualname__ 元数据赋值
        body = body.Where(s => s is not Assign a
            || a.Targets.Count != 1
            || a.Targets[0] is not Name n
            || (n.Id != "__module__" && n.Id != "__qualname__" && n.Id != "__classcell__"
                && n.Id != "__static_attributes__" && n.Id != "__firstlineno__"
                && n.Id != "__classdictcell__")).ToList();

        // 将第一个 __doc__ = '...' 转换为裸字符串表达式（类体 docstring）
        if (body.Count > 0 && body[0] is Assign docAssign
            && docAssign.Targets.Count == 1 && docAssign.Targets[0] is Name docName
            && docName.Id == "__doc__" && docAssign.Value is Constant docConst)
        {
            body[0] = new ExprStmt(docConst);
        }

        // 过滤 class body 中的 return 语句（class body 无 return）
        body = body.Where(s => s is not Return).ToList();

        return new ClassDef(className, bases, body, null, keywords);
    }

    /// <summary>
    /// 从 FunctionRef 构建一个完整的 FunctionDef AST。
    /// 递归反编译子代码对象以获取函数体。
    /// </summary>
    private FunctionDef? BuildFunctionDef(string name, FunctionRef funcRef)
    {
        if (funcRef.Code == null) return null;

        var childCode = funcRef.Code;

        // 1. 提取函数参数
        var args = new List<Parameter>();
        for (int i = 0; i < childCode.ArgCount && i < childCode.Varnames.Count; i++)
        {
            args.Add(new Parameter(childCode.Varnames[i]));
        }

        // 1.5 设置默认参数值（从 FunctionRef.DefaultExprs 获取）
        //    defaults 列表对应最后 N 个位置参数（从后往前）
        if (funcRef.DefaultExprs != null && funcRef.DefaultExprs.Count > 0)
        {
            int startIdx = args.Count - funcRef.DefaultExprs.Count;
            for (int i = 0; i < funcRef.DefaultExprs.Count; i++)
            {
                int argIdx = startIdx + i;
                if (argIdx >= 0 && argIdx < args.Count)
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

        // 3. 去掉函数体末尾的隐式 return None（由 LOAD_CONST None + RETURN_VALUE 产生）
        StripTrailingReturnNone(body);

        // 4. 去掉函数名中的 qualname 前缀（如 C.foobar → foobar）
        var cleanName = name;
        var lastDot = name.LastIndexOf('.');
        if (lastDot >= 0) cleanName = name[(lastDot + 1)..];

        // 4. 生成 FunctionDef
        return new FunctionDef(
            cleanName,
            args,
            body,
            IsGenerator: childCode.IsGenerator,
            IsAsync: childCode.IsCoroutine || childCode.IsAsyncGenerator
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
            if (s is Return ret && ret.Value is Constant { Value: null })
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
            var childBuilder = new AstBuilder(childCode);
            var ast = childBuilder.Build(cfg);
            if (ast is Module m)
                return m.Body;
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
            args.Add(new Parameter(childCode.Varnames[i]));

        // 2. 反编译函数体，提取返回表达式
        var body = DecompileChildCode(childCode);
        if (body.Count == 0) return new Lambda(args, new Constant(null));

        // 找到最后一个 Return 语句，提取其表达式
        for (int i = body.Count - 1; i >= 0; i--)
        {
            if (body[i] is Return ret && ret.Value != null)
                return new Lambda(args, ret.Value);
        }

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
            if (stmt is Assign assign && assign.Targets.Count == 1
                && assign.Targets[0] is Name targetName
                && assign.Value is Constant constVal
                && (constVal.Value == null || constVal.Value is CodeObject)
                && childIdx < childCodes.Count)
            {
                var cc = childCodes[childIdx];
                childIdx++;
                var funcDef = BuildFunctionDef(cc.Name ?? targetName.Id, new FunctionRef(cc, cc.Name ?? targetName.Id));
                if (funcDef != null)
                {
                    // Detect class body: FunctionDef with no args and contains methods
                    if (funcDef.Args.Count == 0 && HasNestedFunctions(funcDef.Body))
                    {
                        // Use the STORE_NAME target as class name (more reliable than code object's name)
                        var className = targetName.Id;
                        // Try to get a better name from the code object if available
                        if (!string.IsNullOrEmpty(cc.Name) && cc.Name != "<module>" && !cc.Name.StartsWith("name_"))
                            className = cc.Name;
                        // 跳过已在 PostProcessFunctionDefs 中正确定义的类（有 bases 的版本更完整）
                        if (existingDefNames.Contains(className) || !localSeen.Add(className))
                        {
                            result.Add(stmt);
                            continue;
                        }
                        var classDef = new ClassDef(
                            className,
                            new List<Expr>(),
                            funcDef.Body
                        );
                        result.Add(classDef);
                        continue;
                    }
                    // 跳过已在 PostProcessFunctionDefs 中正确定义或本方法已创建的函数
                    if (existingDefNames.Contains(funcDef.Name) || !localSeen.Add(funcDef.Name))
                    {
                        result.Add(stmt);
                        continue;
                    }
                    result.Add(funcDef);
                    continue;
                }
            }
            result.Add(stmt);
        }
        return result;
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
}
