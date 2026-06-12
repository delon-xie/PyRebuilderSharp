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
    private readonly Dictionary<int, BasicBlock> _blockByOffset = new();
    private Dictionary<int, BlockResult> _blockResults = new();
    private HashSet<int> _loopHeaderOffsets = new();

    /// <summary>
    /// 总基本块数（用于统计）。
    /// </summary>
    public int TotalBlockCount { get; private set; }

    /// <summary>
    /// 反编译失败的基本块数（用于统计）。
    /// </summary>
    public int FailedBlockCount { get; private set; }

    public AstBuilder(CodeObject codeObject)
    {
        _codeObject = codeObject;
        _blockDecompiler = new BlockDecompiler();
    }

    /// <summary>
    /// 从结构化CFG构建AST。
    /// </summary>
    public AstNode Build(StructuredCFG structuredCFG)
    {
        var cfg = structuredCFG.RawCFG;
        _blockResults = _blockDecompiler.DecompileBlocks(cfg.Blocks, _codeObject);
        
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
        
        stmts = PostProcessFunctionDefs(stmts);
        
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

        // 检测 try/except (SETUP_FINALLY 模式)
        var tryBodyStmts = BuildTryFromBlock(block, visited);
        if (tryBodyStmts != null)
        {
            stmts.AddRange(tryBodyStmts);
            // 标记 handler 块为 visited
            var handlerAbs = GetHandlerOffset(block);
            if (handlerAbs.HasValue)
            {
                var handlerBlocks = new List<BasicBlock>();
                FindBlocksFromOffset(handlerAbs.Value, handlerBlocks);
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
    /// 从块中检测 SETUP_FINALLY → try/except 模式并构建 Try AST。
    /// 如果块不包含 SETUP_FINALLY，返回 null。
    /// </summary>
    private List<Stmt>? BuildTryFromBlock(BasicBlock block, HashSet<BasicBlock> visited)
    {
        var instrs = block.Instructions;
        // 查找 SETUP_FINALLY
        var setupIdx = instrs.FindIndex(i => i.Opcode == Opcode.SETUP_FINALLY);
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
            // 遇到 POP_BLOCK 块时停止（try body 结束标志）
            if (cur.Instructions.Any(i => i.Opcode == Opcode.POP_BLOCK))
            {
                tryBodyBlocks.Add(cur);
                break;
            }
            // 跳过 FOR_ITER 块（属于外层循环，不是 try body 的一部分）
            if (cur.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
            {
                // 检查是否为外层循环（非嵌套在 try body 中的内层循环）
                var forIterEntry = cur.Successors.OrderBy(s => s.StartOffset).FirstOrDefault();
                if (forIterEntry == block)
                    continue;
            }
            tryBodyBlocks.Add(cur);
            foreach (var succ in cur.Successors.OrderBy(s => s.StartOffset))
            {
                // 跳过 FOR_ITER 块：如果 FOR_ITER 的 body entry 是当前 block 本身，
                // 说明 for-loop 是 OUTER（try 在 for-loop 内），不处理
                // 排除向内收集（避免收集到 handler 中）
                if (succ == null) continue;
                if (succ.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
                {
                    var forIterEntry = succ.Successors
                        .OrderBy(s => s.StartOffset).FirstOrDefault();
                    if (forIterEntry == block)
                        continue;
                }
                if (succ.StartOffset < handlerAbs && !tryBodyCollector.Contains(succ))
                    blockQueue.Enqueue(succ);
            }
        }

        // 反编译 try body：当前块中 SETUP_FINALLY 之后的指令用 StackMachine
        // 后继块用 GetStructuredBlockStmts（支持嵌套控制结构）
        // 使用 {block} 作为 visited 防止 GET_ITER/RETURN_VALUE 块被重复收集
        // 勿用 tryBodyCollector（内层块也被标记为 visited → GetStructuredBlockStmts 返回空）
        var tryBodyVisited = new HashSet<BasicBlock> { block };
        var tryStmts = new List<Stmt>();
        // 1) 当前块中 SETUP_FINALLY 之后的指令
        var preBodyInstrs = new List<Instruction>();
        for (int i = setupIdx + 1; i < instrs.Count; i++)
        {
            if (instrs[i].Offset >= handlerAbs) break;
            preBodyInstrs.Add(instrs[i]);
        }
        if (preBodyInstrs.Count > 0)
        {
            var preMachine = new StackMachine(_codeObject);
            foreach (var ins in preBodyInstrs)
            {
                var stmt = preMachine.Execute(ins);
                if (stmt != null) tryStmts.Add(stmt);
            }
            while (preMachine.HasResults)
                tryStmts.Add(new ExprStmt(preMachine.PopResult()));

            // 检测 if/else 条件跳转：如果当前块末尾是 POP_JUMP_IF_*，
            // 说明 try 体内有 if 条件（条件指令和 SETUP_FINALLY 在同一块）
            var lastPre = preBodyInstrs.LastOrDefault();
            if (lastPre != default && JumpHelper.IsConditionalJump(lastPre.Opcode) && lastPre.Argument.HasValue)
            {
                var cond = preMachine.ExprStackCount > 0 ? preMachine.PopExpr() : null;
                if (cond != null)
                {
                    // 条件在栈上，两个后继就是 if/else 分支
                    // 注意：不用 tryBodyCollector 过滤（后继块可能在收集阶段已加入）
                    var sortedSucc = block.Successors
                        .Where(s => s.StartOffset < handlerAbs)
                        .OrderBy(s => s.StartOffset).ToList();
                    // 收集分支块中的语句（跳过 POP_BLOCK 指令）
                    var ifTrueBlock = sortedSucc.Count >= 1 ? sortedSucc[0] : null;  // fallthrough
                    var ifFalseBlock = sortedSucc.Count >= 2 ? sortedSucc[^1] : null; // jump target
                    
                    // 处理 true 分支（跳过 POP_BLOCK）
                    var trueStmts = new List<Stmt>();
                    if (ifTrueBlock != null)
                    {
                        var beforePop = ifTrueBlock.Instructions.TakeWhile(i => i.Opcode != Opcode.POP_BLOCK).ToList();
                        if (beforePop.Count > 0)
                        {
                            var sm = new StackMachine(_codeObject);
                            foreach (var ins in beforePop) { var s = sm.Execute(ins); if (s != null) trueStmts.Add(s); }
                            while (sm.HasResults) trueStmts.Add(new ExprStmt(sm.PopResult()));
                        }
                    }
                    
                    // 处理 false 分支（跳过 POP_BLOCK）
                    var falseStmts = new List<Stmt>();
                    if (ifFalseBlock != null)
                    {
                        var beforePop = ifFalseBlock.Instructions.TakeWhile(i => i.Opcode != Opcode.POP_BLOCK).ToList();
                        if (beforePop.Count > 0)
                        {
                            var sm2 = new StackMachine(_codeObject);
                            foreach (var ins in beforePop) { var s = sm2.Execute(ins); if (s != null) falseStmts.Add(s); }
                            while (sm2.HasResults) falseStmts.Add(new ExprStmt(sm2.PopResult()));
                        }
                    }
                    tryStmts.Add(new If(cond, trueStmts, falseStmts.Count > 0 ? falseStmts : null));
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
        var popBlockBlock = tryBodyBlocks.LastOrDefault(b =>
            b.Instructions.Any(i => i.Opcode == Opcode.POP_BLOCK));
        if (popBlockBlock != null)
        {
            var jfInstr = popBlockBlock.Instructions.FirstOrDefault(
                i => i.Opcode == Opcode.JUMP_FORWARD);
            if (jfInstr.Argument.HasValue)
                elseJumpTarget = jfInstr.Offset + 2 + jfInstr.Argument.Value;
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
                            || ins.Opcode == Opcode.LOAD_NAME || ins.Opcode == Opcode.LOAD_GLOBAL
                            || ins.Opcode == Opcode.JUMP_IF_NOT_EXC_MATCH
                            || ins.Opcode == Opcode.RERAISE
                            || ins.Opcode == Opcode.POP_EXCEPT || ins.Opcode == Opcode.END_FINALLY
                            || ins.Opcode == Opcode.RETURN_VALUE)
                        {
                            isHandlerPart = true;
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
                foreach (var ins in hb.Instructions)
                {
                    if (ins.Opcode == Opcode.LOAD_NAME || ins.Opcode == Opcode.LOAD_GLOBAL)
                    {
                        var typeName = _codeObject.Names.Count > (ins.Argument ?? 0)
                            ? _codeObject.Names[ins.Argument!.Value] : null;
                        if (typeName != null && typeName != "__doc__" && !typeName.StartsWith("__"))
                            exceptType = new Name(typeName, ExpressionContext.Load);
                    }
                }
            }
            handlers.Add(new ExceptHandler(exceptType, null, handlerBody));

            // 检测 else 子句：try body 的 POP_BLOCK 后 JUMP_FORWARD → else body
            if (elseJumpTarget.HasValue)
            {
                var elseBlocks = new List<BasicBlock>();
                FindBlocksFromOffset(elseJumpTarget.Value, elseBlocks);
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
                foreach (var succ in cur.Successors)
                    queue.Enqueue(succ);
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
    /// 获取块中第一个 SETUP_FINALLY 的 handler 绝对偏移。
    /// </summary>
    private int? GetHandlerOffset(BasicBlock block)
    {
        foreach (var ins in block.Instructions)
        {
            if (ins.Opcode == Opcode.SETUP_FINALLY && ins.Argument.HasValue)
                return ins.Offset + 2 + ins.Argument.Value * 2;
        }
        return null;
    }

    private List<Stmt> BuildWhileLoop(BasicBlock header, HashSet<BasicBlock> visited)
    {
        var testExpr = ExtractCondition(header);

        var bodyBlocks = new List<BasicBlock>();
        // body entry = 第一个后继（fallthrough），exit = 第二个后继（jump target）
        var sortedSucc = header.Successors.OrderBy(s => s.StartOffset).ToList();
        var bodyEntry = sortedSucc.FirstOrDefault();
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
        var testExpr = ExtractCondition(header);
        if (header.Instructions.Count == 0) return new List<Stmt>();
        var lastInstr = header.Instructions.Last();
        var targetOffset = lastInstr.Argument!.Value;

        // 统一规则：不论 POP_JUMP_IF_TRUE 还是 POP_JUMP_IF_FALSE，
        // if-body 总是 fallthrough，跳过代码（else/after）总是 jump target
        var bodyBranch = FindFallthrough(header);
        var afterBranch = FindBlockByOffset(targetOffset);

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

        var result = new List<Stmt> { new If(testExpr, bodyStmts, orelse) };
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
        if (block.Flags.HasFlag(BlockFlags.LoopHeader))
        {
            return BuildLoop(block, visited);
        }

        // 检测 for-loop 头：FOR_ITER 是条件跳转但不是 if/else，
        // 即使 LoopHeader 标志未设置（当 for-loop 的 GET_ITER 在另一个块中时）
        if (block.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
        {
            return BuildForLoop(block, visited);
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

        // 检测 try/except
        var tryResult = BuildTryFromBlock(block, visited);
        if (tryResult != null)
        {
            // 注意：try builder 不会标记 handler 块为 visited
            // 由调用方在 tryResult 返回后处理，防止干扰外部作用域的 visited
            return tryResult;
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

        var bodyBranch = FindFallthrough(header);
        var afterBranch = FindBlockByOffset(targetOffset);

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
        // 第一个 body block 的 STORE_NAME/STORE_FAST 指令就是循环变量
        foreach (var bodyBlock in bodyBlocks)
        {
            foreach (var instr in bodyBlock.Instructions)
            {
                if ((instr.Opcode == Opcode.STORE_FAST || instr.Opcode == Opcode.STORE_NAME)
                    && instr.Argument.HasValue)
                {
                    string varName;
                    if (instr.Opcode == Opcode.STORE_FAST)
                        varName = _codeObject.Varnames[instr.Argument.Value];
                    else
                        varName = _codeObject.Names[instr.Argument.Value];
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

            foreach (var succ in current.Successors)
            {
                if (succ != header && !visited.Contains(succ))
                    worklist.Enqueue(succ);
            }
        }
    }

    private BasicBlock? FindElseBlock(BasicBlock header)
        => header.Successors.FirstOrDefault(s => !s.Flags.HasFlag(BlockFlags.LoopBody));

    private BasicBlock? FindBlockByOffset(int offset)
    {
        _blockByOffset.TryGetValue(offset, out var block);
        return block;
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
    // ===================================================================

    /// <summary>
    /// 扫描语句列表，将 Assign(Name, FunctionRef) 转换为真正的 FunctionDef，
    /// 将 `__build_class__` 模式转换为 ClassDef。
    /// </summary>
    private List<Stmt> PostProcessFunctionDefs(List<Stmt> stmts)
    {
        var result = new List<Stmt>(stmts.Count);
        foreach (var stmt in stmts)
        {
            // 递归处理嵌套在控制结构中的语句（函数定义可能被 if/while/for/try 嵌套）
            if (stmt is If ifNode)
            {
                var body = PostProcessFunctionDefs(ifNode.Body);
                var orelse = ifNode.Orelse != null ? PostProcessFunctionDefs(ifNode.Orelse) : null;
                result.Add(new If(ifNode.Test, body, orelse));
                continue;
            }
            if (stmt is While whileNode)
            {
                var body = PostProcessFunctionDefs(whileNode.Body);
                var orelse = whileNode.Orelse != null ? PostProcessFunctionDefs(whileNode.Orelse) : null;
                result.Add(new While(whileNode.Test, body, orelse));
                continue;
            }
            if (stmt is For forNode)
            {
                var body = PostProcessFunctionDefs(forNode.Body);
                var orelse = forNode.Orelse != null ? PostProcessFunctionDefs(forNode.Orelse) : null;
                result.Add(new For(forNode.Target, forNode.Iter, body, orelse));
                continue;
            }
            if (stmt is Try tryNode)
            {
                var body = PostProcessFunctionDefs(tryNode.Body);
                var handlers = tryNode.Handlers.Select(h =>
                    new ExceptHandler(h.Type, h.Name, PostProcessFunctionDefs(h.Body))).ToList();
                var orelse = tryNode.Orelse != null ? PostProcessFunctionDefs(tryNode.Orelse) : null;
                var finalbody = tryNode.Finalbody != null ? PostProcessFunctionDefs(tryNode.Finalbody) : null;
                result.Add(new Try(body, handlers, orelse, finalbody));
                continue;
            }
            if (stmt is FunctionDef fd)
            {
                // 递归处理函数体
                result.Add(new FunctionDef(fd.Name, fd.Args,
                    PostProcessFunctionDefs(fd.Body),
                    fd.Decorators, fd.Returns,
                    fd.IsGenerator, fd.IsAsync));
                continue;
            }
            if (stmt is ClassDef cd)
            {
                result.Add(new ClassDef(cd.Name, cd.Bases,
                    PostProcessFunctionDefs(cd.Body), cd.Decorators));
                continue;
            }

            // ---- Original transformation logic for top-level stmts ----
            if (stmt is Assign assign && assign.Targets.Count == 1
                && assign.Targets[0] is Name targetName)
            {
                // ---- Case 0: Lambda — Assign + FunctionRef with "<lambda>" name ----
                if (assign.Value is FunctionRef funcRef1
                    && (funcRef1.Name == "<lambda>" || funcRef1.Code?.Name == "<lambda>"))
                {
                    var lambda = BuildLambda(funcRef1);
                    if (lambda != null)
                        result.Add(new Assign(new List<Expr> { new Name(targetName.Id, ExpressionContext.Store) }, lambda));
                    else
                        result.Add(stmt);
                    continue;
                }

                // ---- Case 1: Assign + FunctionRef → FunctionDef ----
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
                    if (funcDef != null)
                        result.Add(funcDef);
                    else
                        result.Add(stmt);
                    continue;
                }

                // ---- Case 2: Assign + Call(__build_class__, ...) → ClassDef ----
                if (assign.Value is Call call && call.Func is Name callFuncName && callFuncName.Id == "__build_class__")
                {
                    // 类名来自 STORE_NAME 的目标名（pycdc 格式中 __build_class__ 参数不是类名）
                    var classDef = ExtractClassDef(call, targetName.Id);
                    if (classDef != null)
                        result.Add(classDef);
                    else
                        result.Add(stmt);
                    continue;
                }

                // ---- Case 3: Assign(Name, Name) with same name → import ----
                if (assign.Value is Name valName && valName.Id == targetName.Id)
                {
                    result.Add(new Import(new List<Alias> { new Alias(targetName.Id, null) }));
                    continue;
                }

                // ---- Case 4: Assign(Name, Attribute(module, name)) with import marker → from ... import ----
                if (assign.Value is Models.AST.Attribute attr && attr.Value is Name modName 
                    && attr.Ctx == ExpressionContext.Load && attr.IsImportFrom)
                {
                    result.Add(new ImportFrom(modName.Id, new List<Alias> { new Alias(targetName.Id, null) }, 0));
                    continue;
                }

                result.Add(stmt);
            }
            else
            {
                result.Add(stmt);
            }
        }
        return result;
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
            || (n.Id != "__module__" && n.Id != "__qualname__")).ToList();

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

        // 3. 去掉函数名中的 qualname 前缀（如 C.foobar → foobar）
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
}
