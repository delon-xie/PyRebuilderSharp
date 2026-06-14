using PyRebuilderSharp.Core.Models.AST;
using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.CFG;
using PyRebuilderSharp.Core.Scanners;

namespace PyRebuilderSharp.Core.Builders;

/// <summary>
/// AST构建器 — 使用 BlockDecompiler 进行逐块反编译。
/// 对每个基本块调用 BlockDecompiler，失败块输出注释。
/// </summary>
public class AstBuilder
{
    private readonly BlockDecompiler _blockDecompiler;
    private readonly CodeObject _codeObject;
    private Dictionary<int, BlockResult> _blockResults = new();
    private HashSet<int> _loopHeaderOffsets = new();
    private List<BasicBlock> _allBlocks = new();
    private readonly Dictionary<int, BasicBlock> _blockByOffset = new();
    private readonly HashSet<int> _processedBlockIds = new(); // 已实际处理的块 ID（用于孤儿块检测）

    public AstBuilder(CodeObject codeObject)
    {
        _codeObject = codeObject;
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

        var stmts = BuildStatements(cfg.Entry, new HashSet<BasicBlock>());

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
                    var blockDecomp = new BlockDecompiler();
                    var blockResult = blockDecomp.DecompileBlock(orphan.Instructions, _codeObject, orphan.Id);
                    if (blockResult.IsSuccess)
                    {
                        // 过滤孤儿块的无效内容：仅含 return None 时跳过
                        bool isEmptyReturn = blockResult.Statements.Count == 1
                            && blockResult.Statements[0] is Return r
                            && r.Value is Constant { Value: null };
                        
                        if (!isEmptyReturn)
                        {
                            stmts.Add(new CommentBlock($"# orphan @0x{orphan.StartOffset:X4}"));
                            stmts.AddRange(blockResult.Statements);
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
                Opcode.JUMP_IF_TRUE_OR_POP
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
        
        // Remove trailing module-level return None
        if (stmts.Count > 0 && stmts[^1] is Return ret && ret.Value is Constant { Value: null })
        {
            stmts.RemoveAt(stmts.Count - 1);
        }
        
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
                    ConvertAugAssign(classDef.Body)));
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

        // 检测 with 语句 (SETUP_WITH 模式)
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
            // 标记 handler 块为 visited 
            var handlerAbs = GetHandlerOffset(block);
            List<BasicBlock> handlerBlocks = new();
            if (handlerAbs.HasValue)
            {
                FindBlocksFromOffset(handlerAbs.Value, handlerBlocks);
                foreach (var hb in handlerBlocks)
                    visited.Add(hb);
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
                    if (!visited.Contains(succ))
                    {
                        visited.Add(succ);
                        stmts.AddRange(BuildStatements(succ, visited));
                    }
                }
            }
            return stmts;
        }

        // 3.11+: 通过 ExceptionTable 检测 try/except
        if (_codeObject.ExceptionTable.Count > 0)
        {
            var try311Stmts = BuildTryFromExceptionTable(block, visited);
            if (try311Stmts != null)
            {
                stmts.AddRange(try311Stmts);
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
        var iterExpr = ExtractIterExpression(header);

        var bodyBlocks = new List<BasicBlock>();
        // FOR_ITER 的后继：[fallthrough body, jump-to-exit]
        // 取第一个后继作为 body（fallthrough），跳过 exit 路径
        var bodyEntry = header.Successors
            .OrderBy(s => s.StartOffset)
            .FirstOrDefault();
        if (bodyEntry != null)
            CollectBodyBlocks(bodyEntry, header, bodyBlocks, visited);

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
    /// 从块中检测 SETUP_FINALLY/SETUP_EXCEPT → try/except 模式并构建 Try AST。
    /// 如果块不包含 SETUP_FINALLY，返回 null。
    /// </summary>
    private bool IsTrySetupOpcode(Opcode op, bool isPython38Plus)
    {
        if (op == Opcode.SETUP_FINALLY) return true;
        // SETUP_EXCEPT (121) 仅在 3.5-3.7 有效，3.8+ 是 JUMP_IF_NOT_EXC_MATCH
        if (!isPython38Plus && op == Opcode.SETUP_EXCEPT) return true;
        return false;
    }

    private List<BasicBlock> GetAllBlocks() => _allBlocks;

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
            i.Opcode == Opcode.MATCH_SEQUENCE_312 ||
            i.Opcode == Opcode.MATCH_MAPPING_312 ||
            i.Opcode == Opcode.MATCH_KEYS_312);
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
                ins.Opcode == Opcode.MATCH_SEQUENCE_312 ||
                ins.Opcode == Opcode.MATCH_MAPPING_312)
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
    /// 3.11+: 通过 ExceptionTable 检测 try/except。
    /// 如果 block 的字节码范围在某个 ExceptionTable 条目的 try 体内，构建 Try AST 并设置 IsGroup。
    /// </summary>
    private List<Stmt>? BuildTryFromExceptionTable(BasicBlock block, HashSet<BasicBlock> visited)
    {
        var instrs = block.Instructions;
        if (instrs.Count == 0) return null;
        var blockStart = instrs[0].Offset;
        var blockEnd = instrs.Last().Offset;

        var matchingEntry = _codeObject.ExceptionTable.FirstOrDefault(e =>
            blockStart >= e.StartOffset && blockEnd <= e.EndOffset);
        if (matchingEntry == null) return null;

        var handlerBlock = FindBlockByOffset(matchingEntry.TargetOffset);
        if (handlerBlock == null || visited.Contains(handlerBlock)) return null;

        var tryBlocks = new List<BasicBlock>();
        foreach (var b in GetAllBlocks())
        {
            if (b.Instructions.Count == 0) continue;
            var start = b.Instructions[0].Offset;
            if (start >= matchingEntry.StartOffset && start < matchingEntry.EndOffset)
                tryBlocks.Add(b);
        }
        if (tryBlocks.Count == 0) return null;

        var tryBody = new List<Stmt>();
        var tryVisited = new HashSet<BasicBlock>();
        foreach (var tb in tryBlocks)
        {
            if (tb == block)
            {
                var machine = new StackMachine(_codeObject);
                foreach (var ins in tb.Instructions)
                {
                    var stmt = machine.Execute(ins);
                    if (stmt != null) tryBody.Add(stmt);
                }
                while (machine.HasResults)
                    tryBody.Add(new ExprStmt(machine.PopResult()));
            }
            else if (!visited.Contains(tb) && !tryVisited.Contains(tb))
            {
                tryBody.AddRange(BuildStatements(tb, tryVisited));
            }
        }

        visited.Add(handlerBlock);
        var handlerMachine = new StackMachine(_codeObject);
        var handlerBody = new List<Stmt>();
        foreach (var ins in handlerBlock.Instructions)
        {
            var stmt = handlerMachine.Execute(ins);
            if (stmt != null) handlerBody.Add(stmt);
        }
        while (handlerMachine.HasResults)
            handlerBody.Add(new ExprStmt(handlerMachine.PopResult()));

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
                visited.Add(succ);
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
        var setupIdx = instrs.FindIndex(i => IsTrySetupOpcode(i.Opcode, _codeObject.IsPython38Plus));
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
                if (IsTrySetupOpcode(preBodyInstrs[i].Opcode, _codeObject.IsPython38Plus))
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
                // 只跟随 handler 链内的跳转，不跟随 Exit 块的后缀（避免跳转到 handler 以外的代码）
                foreach (var succ in cur.Successors)
                {
                    if (!cur.Flags.HasFlag(BlockFlags.Exit))
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
        if (setupIdx < 0) return null;

        // 1. 提取 SETUP_WITH 之前的上下文表达式
        var preMachine = new StackMachine(_codeObject);
        var preStmts = new List<Stmt>();
        for (int i = 0; i < setupIdx; i++)
        {
            var stmt = preMachine.Execute(instrs[i]);
            if (stmt != null) preStmts.Add(stmt);
        }

        // 在 SETUP_WITH 之前的最终表达式就是上下文管理器
        Expr? contextExpr = null;
        while (preMachine.HasResults)
            contextExpr = preMachine.PopResult();
        if (contextExpr == null && preMachine.ExprStackCount > 0)
            contextExpr = preMachine.PopExpr();

        // 2. 提取可选的 as 变量
        // SETUP_WITH 后是 BEFORE_WITH，然后 STORE_FAST/NAME 或 POP_TOP
        Expr? optionalVar = null;
        for (int i = setupIdx + 1; i < instrs.Count; i++)
        {
            var op = instrs[i].Opcode;
            if (op == Opcode.BEFORE_WITH || op == Opcode.SETUP_WITH || op == Opcode.WITH_EXCEPT_START)
                continue;
            if (op == Opcode.POP_TOP)
                break; // 没有 as 变量
            if ((op == Opcode.STORE_FAST || op == Opcode.STORE_NAME) && instrs[i].Argument.HasValue)
            {
                var idx = instrs[i].Argument.Value;
                string varName;
                if (op == Opcode.STORE_FAST)
                    varName = idx < _codeObject.Varnames.Count ? _codeObject.Varnames[idx] : $"v_{idx}";
                else
                    varName = idx < _codeObject.Names.Count ? _codeObject.Names[idx] : $"n_{idx}";
                optionalVar = new Name(varName, ExpressionContext.Store);
                break;
            }
            break;
        }

        // 3. 提取 body — 当前块内剩余指令 + 后继块
        var handlerRel = instrs[setupIdx].Argument ?? 0;
        var handlerAbs = instrs[setupIdx].Offset + 2 + handlerRel * 2;

        // 跳过变量赋值指令找到 body 起始位置
        int bodyStart = setupIdx + 1;
        for (; bodyStart < instrs.Count; bodyStart++)
        {
            var op = instrs[bodyStart].Opcode;
            if (op == Opcode.BEFORE_WITH || op == Opcode.WITH_EXCEPT_START)
                continue;
            if (op == Opcode.POP_TOP || op == Opcode.STORE_FAST || op == Opcode.STORE_NAME)
                continue;
            break;
        }

        // 处理当前块内的 body 指令（到 POP_BLOCK 之前）
        var bodyStmts = new List<Stmt>();
        var bodyMachine = new StackMachine(_codeObject);
        for (int i = bodyStart; i < instrs.Count; i++)
        {
            if (instrs[i].Opcode == Opcode.POP_BLOCK)
                break;
            if (instrs[i].Opcode == Opcode.RETURN_VALUE && i < instrs.Count - 1)
                continue; // 跳过 handler 部分的 RETURN_VALUE
            var stmt = bodyMachine.Execute(instrs[i]);
            if (stmt != null) bodyStmts.Add(stmt);
        }
        while (bodyMachine.HasResults)
            bodyStmts.Add(new ExprStmt(bodyMachine.PopResult()));

        // 收集后继块作为 body（如 with 体内含循环/分支时）
        var bodyBlocks = new List<BasicBlock>();
        var bodyCollector = new HashSet<BasicBlock> { block };
        var blockQueue = new Queue<BasicBlock>();
        foreach (var succ in block.Successors.OrderBy(s => s.StartOffset))
        {
            if (succ == null || succ.StartOffset >= handlerAbs || bodyCollector.Contains(succ))
                continue;
            if (succ.StartOffset < instrs[setupIdx].Offset + 2) continue;
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

        // 从 visited 移除以支持递归
        foreach (var bb in bodyBlocks)
            visited.Remove(bb);

        // 合并后继块的 body 语句
        foreach (var bodyBlock in bodyBlocks)
            bodyStmts.AddRange(GetStructuredBlockStmts(bodyBlock, visited));

        // 构建 With AST
        var items = new List<WithItem>
        {
            new(contextExpr ?? new Name("_", ExpressionContext.Load), optionalVar)
        };
        var result = new List<Stmt>();
        // 前缀语句
        foreach (var ps in preStmts)
        {
            // 过滤掉来自 LOAD_GLOBAL/CALL_FUNCTION 等已经作为上下文表达式的语句
            if (ps is ExprStmt e && e.Value == contextExpr)
                continue;
            result.Add(ps);
        }
        result.Add(new With(items, bodyStmts));
        return result;
    }

    private List<Stmt> BuildWhileLoop(BasicBlock header, HashSet<BasicBlock> visited)
    {
        // v3.10+: 如果 header 内含 SETUP_FINALLY（try body 在 while 体内），
        // 则 POP_JUMP 是内层 if 的条件，不是 while 循环的条件。
        // 此时从 predecessor（while 入口条件块）提取条件。
        bool hasTryBeforeJump = header.Instructions.Any(i => IsTrySetupOpcode(i.Opcode, _codeObject.IsPython38Plus));
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
        if (header.Instructions.Any(i => IsTrySetupOpcode(i.Opcode, _codeObject.IsPython38Plus)))
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
        if (header.Instructions.Any(i => IsTrySetupOpcode(i.Opcode, _codeObject.IsPython38Plus)))
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
        var targetOffset = lastInstr.Argument!.Value;

        // POP_JUMP_IF_FALSE: body = fallthrough, else = jump target
        // POP_JUMP_IF_TRUE:  body = same fallthrough, but condition needs NEGATION
        bool isJumpIfTrue = lastInstr.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_TRUE_PY38;
        
        var bodyBranch = FindFallthrough(header);
        var afterBranch = FindBlockByOffset(targetOffset);
        
        if (isJumpIfTrue && testExpr != null)
            testExpr = new UnaryOp(UnaryOperator.Not, testExpr);

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
        if (afterBranch != null && !visited.Contains(afterBranch))
        {
            // 检测是否为 else 子句（非 elif 链）
            // 条件：after 块的唯一前驱是条件块，且 body 不以终端指令结尾
            bool isElseClause = false;
            if (bodyBranch != null)
            {
                isElseClause = afterBranch.Predecessors.Count == 1
                    && afterBranch.Predecessors.Contains(header);
            }

            if (isElseClause)
            {
                // 同时检测 body 的最后一条语句是否为终止语句（Return/Raise/Break/Continue）
                // 若是，则 afterBranch 是顺序代码而非 else 子句
                bool bodyEndsWithTerminal = bodyStmts.Count > 0
                    && bodyStmts[^1] is Return or Raise or Break or Continue;
                if (bodyEndsWithTerminal)
                    isElseClause = false;
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
                afterStmts = BuildStatements(afterBranch, visited);
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
        result.Add(new If(testExpr, bodyStmts, orelse));
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
            return tryResult;
        }

        // 检测 if/else 条件分支
        if (IsConditionBranch(block))
        {
            // 检查是否为循环继续（向后跳转 → 不是 if/else）
            var lastInstr = block.Instructions.LastOrDefault();
            if (lastInstr.Argument.HasValue && lastInstr.Argument.Value < block.StartOffset)
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
        
        // 检测 continue：body 为空且块末尾有 JUMP_ABSOLUTE 到循环头
        if (bodyStmts.Count == 0 && bodyBranch != null)
        {
            var lastInBody = bodyBranch.Instructions.LastOrDefault();
            if (lastInBody != default && lastInBody.Opcode == Opcode.JUMP_ABSOLUTE
                && lastInBody.Argument.HasValue && _loopHeaderOffsets.Contains(lastInBody.Argument.Value))
            {
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

        // Pop from expression stack (not _results), since LOAD_CONST pushes there
        if (stackMachine.ExprStackCount > 0)
            return stackMachine.PopExpr();
        return stackMachine.HasResults ? stackMachine.PopResult() : new Constant(true);
    }

    private Expr ExtractIterExpression(BasicBlock header)
    {
        // 在 for 循环的 header block 中，FOR_ITER 可能在独立的块中，
        // 而迭代表达式在 predecessor 块中
        // 所以寻找 headr 的前驱块中的内容
        
        // 先看 header 自身中 FOR_ITER 之前的指令
        var iterInstrs = header.Instructions
            .TakeWhile(i => i.Opcode != Opcode.FOR_ITER)
            .ToList();
        
        // 如果 header 自身没有找到 LOAD，检查前驱块
        if (iterInstrs.Count <= 1)
        {
            foreach (var pred in header.Predecessors)
            {
                var predInstrs = pred.Instructions.ToList();
                if (predInstrs.Count > 0)
                {
                    // 找到 LOAD_NAME/LOAD_FAST/LOAD_GLOBAL + GET_ITER 模式
                    var loadIdx = predInstrs.FindIndex(i => 
                        i.Opcode is Opcode.LOAD_NAME or Opcode.LOAD_FAST or Opcode.LOAD_GLOBAL 
                        or Opcode.LOAD_CONST or Opcode.LOAD_ATTR);
                    if (loadIdx >= 0)
                    {
                        // 从 load 指令开始取到末尾
                        iterInstrs = predInstrs.Skip(loadIdx).ToList();
                        break;
                    }
                }
            }
        }

        // 去掉末尾的 GET_ITER
        if (iterInstrs.Count > 0 && iterInstrs.Last().Opcode == Opcode.GET_ITER)
            iterInstrs = iterInstrs.Take(iterInstrs.Count - 1).ToList();

        var stackMachine = new StackMachine(_codeObject);
        foreach (var instr in iterInstrs)
            stackMachine.Execute(instr);

        // 迭代表达式在 expr 栈上，不在 _results 中
        if (stackMachine.ExprStackCount > 0)
            return stackMachine.PopExpr();
        return stackMachine.HasResults ? stackMachine.PopResult() : new Name("iterable", ExpressionContext.Load);
    }

    private Expr ExtractLoopVariable(BasicBlock header, List<BasicBlock> bodyBlocks)
    {
        foreach (var bodyBlock in bodyBlocks)
        {
            // 检测 UNPACK_SEQUENCE n → 元组解包循环变量（如 for a, b in ...）
            var unpackIdx = bodyBlock.Instructions.FindIndex(i => i.Opcode == Opcode.UNPACK_SEQUENCE);
            if (unpackIdx >= 0 && bodyBlock.Instructions[unpackIdx].Argument.HasValue)
            {
                int count = bodyBlock.Instructions[unpackIdx].Argument.Value;
                var names = new List<Expr>();
                // UNPACK_SEQUENCE 后跟 count 个 STORE_FAST/STORE_NAME
                for (int i = unpackIdx + 1; i < bodyBlock.Instructions.Count && names.Count < count; i++)
                {
                    var instr = bodyBlock.Instructions[i];
                    if (instr.Opcode == Opcode.STORE_FAST && instr.Argument.HasValue
                        && instr.Argument.Value >= 0 && instr.Argument.Value < _codeObject.Varnames.Count)
                        names.Add(new Name(_codeObject.Varnames[instr.Argument.Value], ExpressionContext.Store));
                    else if (instr.Opcode == Opcode.STORE_NAME && instr.Argument.HasValue
                        && instr.Argument.Value >= 0 && instr.Argument.Value < _codeObject.Names.Count)
                        names.Add(new Name(_codeObject.Names[instr.Argument.Value], ExpressionContext.Store));
                    else break;
                }
                if (names.Count == count)
                    return new ListLiteral(names, ContainerKind.Tuple);
            }

            foreach (var instr in bodyBlock.Instructions)
            {
                if ((instr.Opcode == Opcode.STORE_FAST || instr.Opcode == Opcode.STORE_NAME)
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
                    else
                    {
                        if (idx < 0 || idx >= _codeObject.Names.Count)
                            continue;
                        varName = _codeObject.Names[idx];
                    }
                    return new Name(varName, ExpressionContext.Store);
                }
            }
        }
        return new Name("_", ExpressionContext.Store);
    }

    private void CollectBodyBlocks(
        BasicBlock entry, BasicBlock header,
        List<BasicBlock> bodyBlocks, HashSet<BasicBlock> visited)
    {
        var worklist = new Queue<BasicBlock>();
        worklist.Enqueue(entry);

        while (worklist.Count > 0)
        {
            var current = worklist.Dequeue();
            if (current == header || visited.Contains(current))
                continue;

            bodyBlocks.Add(current);
            visited.Add(current);

            // v3.10: 回边条件块（POP_JUMP_IF_TRUE 目标 < 自身偏移）的后继是循环出口，不是 body 的一部分
            var lastInstr = current.Instructions.LastOrDefault();
            bool isBackEdgeBlock = lastInstr != default
                && JumpHelper.IsJump(lastInstr.Opcode)
                && lastInstr.Argument.HasValue
                && lastInstr.Argument.Value < current.StartOffset;

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
                    currentResult.Add(fd);
                    continue;
                }
                if (stmt is ClassDef cd)
                {
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
                        var funcDef = BuildFunctionDef(fnName, funcRef);
                        currentResult.Add(funcDef ?? stmt);
                        continue;
                    }
                    // ClassDef
                    if (assign.Value is Call call && call.Func is Name callFuncName && callFuncName.Id == "__build_class__")
                    {
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

        return result;
    }

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

        // Decompile class body from the child code object
        var body = DecompileChildCode(funcRef.Code);

        // 过滤 class body 中的 __module__ / __qualname__ 元数据赋值
        body = body.Where(s => s is not Assign a
            || a.Targets.Count != 1
            || a.Targets[0] is not Name n
            || (n.Id != "__module__" && n.Id != "__qualname__" && n.Id != "__classcell__")).ToList();

        // 过滤 class body 中的 return 语句（class body 无 return）
        body = body.Where(s => s is not Return).ToList();

        return new ClassDef(className, bases, body);
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
        var childCodes = _codeObject?.ChildCodes ?? new List<CodeObject>();
        if (childCodes.Count == 0)
            return stmts;

        var result = new List<Stmt>(stmts.Count);
        int childIdx = 0;

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
                        var classDef = new ClassDef(
                            className,
                            new List<Expr>(),
                            funcDef.Body
                        );
                        result.Add(classDef);
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
