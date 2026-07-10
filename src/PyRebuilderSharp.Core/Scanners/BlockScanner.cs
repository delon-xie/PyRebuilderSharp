using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.CFG;
using PyRebuilderSharp.Core.Versioning;

namespace PyRebuilderSharp.Core.Scanners;

/// <summary>
/// Phase 1: 分块扫描器。
/// 负责将字节码指令序列划分为基本块。
/// 核心算法：Leader标记法。
/// </summary>
public class BlockScanner : IBlockScanner
{
    /// <summary>
    /// 将指令序列划分为基本块。
    /// </summary>
    public List<BasicBlock> Scan(CodeObject codeObj)
    {
        var instructions = codeObj.Instructions;

        var leaders = MarkLeaders(instructions, codeObj.ExceptionTable, codeObj);
        var blocks = SplitAtLeaders(instructions, leaders);
        LinkBlocks(blocks, codeObj.ExceptionTable, codeObj);

        // Phase 9-01: 清理 handler 块中错误连接到 class/func 定义的后继边
        CleanHandlerSuccessors(blocks);

        MergeOrphanBlocks(blocks);
        MarkBlockProperties(blocks);

        return blocks;
    }

    /// <summary>
    /// 标记Leader指令。
    /// Leader是基本块的起始指令。
    /// </summary>
    private SortedSet<int> MarkLeaders(List<Instruction> instructions, List<ExceptionTableEntry>? exceptionTable = null, CodeObject? codeObj = null)
    {
        var leaders = new SortedSet<int> { 0 };

        for (int i = 0; i < instructions.Count; i++)
            {
                var instr = instructions[i];

                if (JumpHelper.IsTerminal(instr.Opcode))
            {
                if (i + 1 < instructions.Count)
                    leaders.Add(instructions[i + 1].Offset);
            }
            else if (JumpHelper.IsConditionalJump(instr.Opcode))
            {
                var target = ResolveJumpTarget(instr, codeObj);
                if (target.HasValue)
                    leaders.Add(target.Value);
                if (i + 1 < instructions.Count)
                    leaders.Add(instructions[i + 1].Offset);
            }
            else if (JumpHelper.IsUnconditionalJump(instr.Opcode))
            {
                var target = ResolveJumpTarget(instr, codeObj);
                if (target.HasValue)
                    leaders.Add(target.Value);
            }
            // SETUP_FINALLY: 异常处理器入口也要标记为 leader
            // 仅限 SETUP_FINALLY，不含 SETUP_EXCEPT（3.8-3.10 中 opcode 121 为 JUMP_IF_NOT_EXC_MATCH，
            // 其 argument 是跳转距离而非 handler 偏移）
            else if (instr.Opcode == Opcode.SETUP_FINALLY)
            {
                if (instr.Argument.HasValue)
                {
                    var handlerOffset = instr.Offset + 2 + instr.Argument.Value;
                    leaders.Add(handlerOffset);
                }
            }
        }

        // 3.11+: ExceptionTable 条目定义 try/except/finally/match handler 入口
        // 同时拆块于 try 体起始/结束边界，使块边界与异常条目对齐
        if (exceptionTable != null)
            {
                foreach (var entry in exceptionTable)
                {
                    leaders.Add(entry.TargetOffset);               // handler 入口
                    leaders.Add(entry.StartOffset);                // try 体起始
                    leaders.Add(entry.EndOffset);                  // try 体结束（独占）
                    
                }
            }

            Console.Error.WriteLine($"[BLOCK_DEBUG] Final leaders: {string.Join(", ", leaders)}");
        return leaders;
    }

    /// <summary>
    /// 解析跳转目标为绝对字节偏移。
    /// 不同 Python 版本的跳转参数格式不同：
    ///   - 2.7, 3.5: 可变长度指令，arg = 绝对或相对指令数（需公式转换）
    ///   - 3.6-3.9: wordcode（2字节/指令），arg = 指令索引（需 *2 转字节偏移）
    ///     参考 CPython 3.6: Include/opcode.h wordcode 格式，参数为指令计数
    ///     Python/compile.c: assembler emits arg as instruction index
    ///   - 3.10+: wordcode，arg 已在 ParseInstructions 中转为字节偏移
    ///     参考 CPython 3.10: Python/compile.c line ~785 "jumps are absolute byte offsets"
    ///   - 3.12+: wordcode + caches，参数已为字节偏移
    /// </summary>
    private static int? ResolveJumpTarget(Instruction instr, CodeObject? codeObj = null)
    {
        if (!instr.Argument.HasValue) return null;

        // -- 检测是否使用 CACHE（3.11+）—
        bool hasCaches = codeObj?.Version switch
        {
            PythonVersion.Py311 or PythonVersion.Py312 or PythonVersion.Py313 or PythonVersion.Py314 => true,
            _ => false
        };
        // 参考 CPython 3.12: Include/internal/pycore_opcode.h 的 FOR_ITER_CACHE_ENTRIES = 1

        // -- 检测 wordcode 格式（启发式：所有指令偏移均为偶数）--
        // 3.6-3.14 均使用 wordcode（2字节/指令），偏移均为偶数
        // 非 wordcode（2.7, 3.5）指令长度可变，可能存在奇数偏移
        bool isWordcode = codeObj?.Instructions != null
            && codeObj.Instructions.Count > 1
            && codeObj.Instructions.All(i => i.Offset % 2 == 0);

        // -- 检测 3.6-3.9 wordcode（arg 为指令数，需 *2 转字节偏移）--
        // 使用显式版本 case 而非 boolean flag 组合
        bool is36To39Wordcode = codeObj?.Version switch
        {
            PythonVersion.Py36 or PythonVersion.Py37 or PythonVersion.Py38 or PythonVersion.Py39 => true,
            _ => false
        };

        return instr.Opcode switch
        {
            // 3.13+ 和 3.14 在解析阶段已将跳转参数转为绝对字节偏移，不复算
            Opcode.JUMP_BACKWARD or Opcode.JUMP_BACKWARD_NO_INTERRUPT
                or Opcode.FOR_ITER or Opcode.JUMP_FORWARD
                or Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                when codeObj?.Version >= PythonVersion.Py313 => instr.Argument.Value,
            Opcode.JUMP_ABSOLUTE => is36To39Wordcode ? instr.Argument.Value : instr.Argument.Value,
            // 参考 CPython 3.8: Include/opcode.h wordcode 格式
            //     JUMPTO(x) = first_instr + x / sizeof(_Py_CODEUNIT)
            //     (Python/ceval.c 3.8) — arg 是字节偏移，非指令索引
            Opcode.JUMP_FORWARD or Opcode.FOR_ITER
                => instr.Offset + 2 + (is36To39Wordcode ? instr.Argument.Value : instr.Argument.Value)
                // 3.11+ (HasCaches): FOR_ITER 有 1 个 CACHE 条目(2字节)，跳转需额外偏移
                + (hasCaches && instr.Opcode == Opcode.FOR_ITER ? 2 : 0),
            // 参考 CPython 3.12: Include/internal/pycore_opcode.h
            //     FOR_ITER 的 cache 偏移 = FOR_ITER_CACHE_ENTRIES * 2 = 2
            Opcode.JUMP_BACKWARD or Opcode.JUMP_BACKWARD_NO_INTERRUPT => instr.Offset + 2 - instr.Argument.Value,
            // 3.12+ wordcode: 条件跳转参数是相对字节偏移，需加上当前指令+2
            // 3.6-3.9 wordcode: 参数已为绝对字节偏移
            Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                or Opcode.POP_JUMP_IF_NONE or Opcode.POP_JUMP_IF_NOT_NONE
                when isWordcode => (is36To39Wordcode || codeObj?.Version == PythonVersion.Py310)
                    ? instr.Argument.Value  // 3.6-3.9: 绝对字节偏移; 3.10: 已在 ParseInstructions *2 转为绝对字节偏移
                    : instr.Offset + 2 + instr.Argument.Value,  // 3.11+: 相对字节偏移
            _ => is36To39Wordcode ? instr.Argument.Value : instr.Argument.Value
        };
    }

    private List<BasicBlock> SplitAtLeaders(List<Instruction> instructions, SortedSet<int> leaders)
    {
        var blocks = new List<BasicBlock>();
        var leaderArray = leaders.ToArray();

        for (int i = 0; i < leaderArray.Length; i++)
        {
            int startOffset = leaderArray[i];
            int endOffset = (i + 1 < leaderArray.Length)
                ? leaderArray[i + 1] - 1
                : (instructions.Count > 0 ? instructions.Last().Offset : 0);

            var block = new BasicBlock
            {
                StartOffset = startOffset,
                EndOffset = endOffset
            };

            foreach (var instr in instructions)
            {
                if (instr.Offset >= startOffset && instr.Offset <= endOffset)
                    block.Instructions.Add(instr);
            }

            blocks.Add(block);
        }

        return blocks;
    }

    private void LinkBlocks(List<BasicBlock> blocks, List<ExceptionTableEntry>? exceptionTable = null, CodeObject? codeObj = null)
    {
        for (int i = 0; i < blocks.Count; i++)
        {
            var block = blocks[i];
            var lastInstr = block.Instructions.LastOrDefault();

            if (lastInstr == default) continue;

            if (block.StartOffset == 0)
            {
                Console.Error.WriteLine($"[BLOCK_LINK] Entry block 0x{block.StartOffset:X4} last instruction: {lastInstr.Opcode}");
            }

            switch (lastInstr.Opcode)
            {
                case Opcode.RETURN_VALUE:
                    block.Flags |= BlockFlags.Exit;
                    ResolveIntermediateJumps(block, blocks, codeObj);
                    if (block.StartOffset == 0)
                    {
                        Console.Error.WriteLine($"[BLOCK_LINK] Entry block 0x{block.StartOffset:X4} has RETURN_VALUE as last instruction, no fallthrough");
                    }
                    // 注意：RETURN_VALUE 是函数终止指令，不产生顺序后继。
                    // RAISE_VARARGS 的 fallthrough 由下一条 case 处理。
                    break;

                case Opcode.RETURN_GENERATOR_313:
                    block.Flags |= BlockFlags.Exit;
                    ResolveIntermediateJumps(block, blocks, codeObj);
                    break;

                case Opcode.RAISE_VARARGS:
                    block.Flags |= BlockFlags.Exit;
                    ResolveIntermediateJumps(block, blocks, codeObj);
                    // RAISE_VARARGS (RERAISE) 仍需要顺序后继，用于 try/except handler → code after try/except
                    if (i + 1 < blocks.Count)
                        AddSuccessor(block, blocks[i + 1]);
                    break;

                case Opcode.JUMP_ABSOLUTE:
                case Opcode.JUMP_FORWARD:
                case Opcode.JUMP_BACKWARD:
                    // 扫描块内所有无条件跳转的回边（嵌套循环/嵌套 try 的回边在同一块）
                    if (lastInstr.Opcode == Opcode.JUMP_ABSOLUTE)
                    {
                        foreach (var ins in block.Instructions)
                        {
                            if (ins.Opcode == Opcode.JUMP_ABSOLUTE && ins.Argument.HasValue)
                                AddSuccessor(block, FindBlockByOffset(blocks, ins.Argument.Value));
                            else if (ins.Opcode == Opcode.JUMP_BACKWARD && ins.Argument.HasValue)
                            {
                                var target = ResolveJumpTarget(ins, codeObj)!.Value;
                                AddSuccessor(block, FindBlockByOffset(blocks, target));
                            }
                        }
                    }
                    else
                    {
                        AddSuccessor(block, FindBlockByOffset(blocks, ResolveJumpTarget(lastInstr, codeObj)!.Value));
                    }
                    // 扫描块内所有中间跳转（含无条件跳转如 JUMP_FORWARD 在 RERAISE 前）
                    foreach (var ins in block.Instructions)
                    {
                        if (ins.Opcode is Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                            or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                            or Opcode.FOR_ITER
                            or Opcode.JUMP_FORWARD or Opcode.JUMP_ABSOLUTE)
                        {
                            if (ins.Argument.HasValue && ins.Offset != lastInstr.Offset)
                                AddSuccessor(block, FindBlockByOffset(blocks, ResolveJumpTarget(ins, codeObj)!.Value));
                        }
                    }
                    break;

                case Opcode.POP_JUMP_IF_TRUE:
                case Opcode.POP_JUMP_IF_FALSE:
                case Opcode.JUMP_IF_TRUE_OR_POP:
                case Opcode.JUMP_IF_FALSE_OR_POP:
                case Opcode.FOR_ITER:
                case Opcode.POP_JUMP_IF_NONE:
                case Opcode.POP_JUMP_IF_NOT_NONE:
                    var jumpTarget = ResolveJumpTarget(lastInstr, codeObj);
                    if (jumpTarget.HasValue)
                    {
                        var jumpBlock = FindBlockByOffset(blocks, jumpTarget.Value);
                        if (jumpBlock != null)
                            AddSuccessor(block, jumpBlock);
                        else
                            Console.Error.WriteLine($"[BLOCK_LINK] Warning: jump target block not found for {lastInstr.Opcode} at 0x{lastInstr.Offset:X4}");
                    }
                    if (i + 1 < blocks.Count)
                    {
                        var fallthroughBlock = blocks[i + 1];
                        AddSuccessor(block, fallthroughBlock);
                        Console.Error.WriteLine($"[BLOCK_LINK] {lastInstr.Opcode} at 0x{lastInstr.Offset:X4} added fallthrough successor 0x{fallthroughBlock.StartOffset:X4}");
                    }
                    break;

                default:
                    // 终端指令（RETURN_VALUE, RAISE_VARARGS 等）不产生后继
                    // 参考 CPython 3.12: Python/ceval.c — 终端指令后代码不可达
                    if (!JumpHelper.IsTerminal(lastInstr.Opcode))
                    {
                        if (i + 1 < blocks.Count)
                        {
                            AddSuccessor(block, blocks[i + 1]);
                            if (block.StartOffset == 0)
                            {
                                Console.Error.WriteLine(
                                    $"[BLOCK_LINK] Entry block 0x{block.StartOffset:X4} has {block.Instructions.Count} instructions, last opcode={lastInstr.Opcode}, added successor 0x{blocks[i + 1].StartOffset:X4}");
                            }
                        }
                    }
                    break;
            }
        }

        // 3.11+: ExceptionTable handler 边 — try 体 → handler 块
        // 注意：排除 class/func 定义块（Phase 9-01），防止 handler→class/func 错误边
        if (exceptionTable != null)
        {
            foreach (var entry in exceptionTable)
            {
                var handlerBlock = FindBlockByOffset(blocks, entry.TargetOffset);
                if (handlerBlock == null) continue;

                // 标注 handler block 的 ExceptionHandler flag
                handlerBlock.Flags |= BlockFlags.ExceptionHandler;

                // 找出 try 体覆盖范围的最后一个块
                for (int j = 0; j < blocks.Count; j++)
                {
                    if (blocks[j].StartOffset >= entry.StartOffset
                        && blocks[j].EndOffset <= entry.EndOffset)
                    {
                        // Phase 9-01: 不将 class/func 定义块链接到 handler
                        if (!IsClassOrFuncDefinition(blocks[j]))
                            AddSuccessor(blocks[j], handlerBlock);
                    }
                    if (blocks[j].StartOffset > entry.EndOffset) break;
                }
            }
        }
    }

    private void ResolveIntermediateJumps(BasicBlock block, List<BasicBlock> blocks, CodeObject? codeObj = null)
    {
        foreach (var ins in block.Instructions)
        {
            if (ins.Opcode is Opcode.JUMP_FORWARD or Opcode.JUMP_ABSOLUTE
                or Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                or Opcode.FOR_ITER)
            {
                if (ins.Argument.HasValue)
                {
                    var target = ResolveJumpTarget(ins, codeObj);
                    if (target.HasValue)
                        AddSuccessor(block, FindBlockByOffset(blocks, target.Value));
                }
            }
        }
    }

    private void AddSuccessor(BasicBlock from, BasicBlock? to)
    {
        if (to == null) return;
        from.Successors.Add(to);
        to.Predecessors.Add(from);
    }

    private BasicBlock? FindBlockByOffset(List<BasicBlock> blocks, int offset)
        => blocks.FirstOrDefault(b => b.StartOffset <= offset && offset <= b.EndOffset);

    private void MarkBlockProperties(List<BasicBlock> blocks)
    {
        if (blocks.Count > 0)
            blocks[0].Flags |= BlockFlags.Entry;

        foreach (var block in blocks)
        {
            var lastInstr = block.Instructions.LastOrDefault();
            if (lastInstr != default && JumpHelper.IsTerminal(lastInstr.Opcode))
                block.Flags |= BlockFlags.Exit;
        }
    }

    /// <summary>
    /// 合并 RETURN_VALUE 后无前驱的孤儿块指令到后继可达块。
    /// CPython 中 RETURN_VALUE 后的指令不被任何跳转指向，但在 MarkLeaders 中
    /// 会被标记为 leader（指令紧跟 terminal），导致孤立块。
    /// 不删除孤儿块本身（避免引用失效），仅复制指令到后继块。
    /// 参考 CPython 3.10 Include/opcode.h: RETURN_VALUE = 83 (terminal)
    /// </summary>
    private void MergeOrphanBlocks(List<BasicBlock> blocks)
    {
        for (int i = 0; i < blocks.Count; i++)
        {
            var block = blocks[i];
            var lastInstr = block.Instructions.LastOrDefault();
            if (lastInstr == default) continue;

            // RETURN_VALUE/RETURN_GENERATOR_313 后紧跟的块且无其他前驱 → 合并指令到后继可达块
            if ((lastInstr.Opcode == Opcode.RETURN_VALUE || lastInstr.Opcode == Opcode.RETURN_GENERATOR_313)
                && i + 1 < blocks.Count
                && blocks[i + 1].Predecessors.Count == 0)
            {
                var orphanBlock = blocks[i + 1];
                // 找到 orphanBlock 后的第一个有前驱的块，将 orphan 的指令合并进去
                for (int j = i + 1; j < blocks.Count; j++)
                {
                    if (blocks[j].Predecessors.Count > 0)
                    {
                        blocks[j].Instructions.InsertRange(0, orphanBlock.Instructions);
                        // 清空孤儿块指令，防止下游孤儿恢复添加多余注释
                        orphanBlock.Instructions.Clear();
                        break;
                    }
                }
                // 不清除 orphanBlock 的指令或删除块（防止下游引用失效），
                // 0 前驱的块在 CFG 遍历中会被自然跳过。
            }
        }
    }

    // ---- Phase 9-01: 清理 handler→class/func 错误边 ----

    /// <summary>
    /// 清理 handler 块中错误连接到 class/func 定义的后继边。
    /// 
    /// 问题：BlockScanner.LinkBlocks 将 handler 后的所有 fallthrough 块无差别链接，
    /// 当后续块是 class 定义（LOAD_BUILD_CLASS）或函数定义（MAKE_FUNCTION）时，
    /// 这些定义被错误地作为 handler 的后继，导致反编译输出中 class/func 被嵌套在
    /// try-except 的 handler 内。
    /// 
    /// 修复：检测 handler 块的 successors 中的 class/func 定义块，移除错误边后
    /// 将被移除的块连接到最近的公共前驱。
    /// </summary>
    private void CleanHandlerSuccessors(List<BasicBlock> blocks)
    {
        // Step 1: 收集所有 handler 块的后继中属于 class/func 定义的块
        var edgesToRemove = new List<(BasicBlock From, BasicBlock To)>();

        // 检查所有可能是 handler 的块（标记了 ExceptionHandler flag，或位于 try 范围附近）
        foreach (var block in blocks)
        {
            bool isHandler = block.Flags.HasFlag(BlockFlags.ExceptionHandler);

            // 非 handler 块也检查：通过 HandlerDepth 标注或 SETUP_FINALLY 目标块
            // 但 BlockScanner 可能尚未标注。通过 ExceptionTable 和目标块特征判断：
            // handler 块的特征：包含 handler preamble opcodes 且不在 try body 范围内
            if (!isHandler)
            {
                // 检查块是否包含 handler preamble 特有的 opcode
                // PUSH_EXC_INFO / CHECK_EXC_MATCH → 3.11+ handler
                // 连续的 POP_TOP (3次以上) → 3.10- bare handler
                int popTopCount = block.Instructions.Count(i => i.Opcode == Opcode.POP_TOP);
                bool hasPreamble = block.Instructions.Any(i =>
                    i.Opcode == Opcode.PUSH_EXC_INFO_312 ||
                    i.Opcode == Opcode.PUSH_EXC_INFO ||
                    i.Opcode == Opcode.CHECK_EXC_MATCH)
                    || popTopCount >= 3;
                if (hasPreamble)
                {
                    isHandler = true;
                    block.Flags |= BlockFlags.ExceptionHandler;
                }
            }

            if (!isHandler) continue;

            foreach (var succ in block.Successors.ToList())
            {
                if (IsClassOrFuncDefinition(succ))
                {
                    edgesToRemove.Add((block, succ));
                }
            }
        }

        if (edgesToRemove.Count == 0) return;

        // Step 2: 移除错误边
        foreach (var (from, to) in edgesToRemove)
        {
            from.Successors.Remove(to);
            to.Predecessors.Remove(from);
            Console.Error.WriteLine(
                $"[CFG_CLEAN] Removed handler→class/func edge: 0x{from.StartOffset:X4} → 0x{to.StartOffset:X4}");
        }

        // Step 3: 确保被移除的 class/func block 有前面的 predecessor
        foreach (var (_, to) in edgesToRemove)
        {
            if (to.Predecessors.Count == 0)
            {
                int idx = blocks.IndexOf(to);
                for (int j = idx - 1; j >= 0; j--)
                {
                    if (!blocks[j].Flags.HasFlag(BlockFlags.ExceptionHandler)
                        && blocks[j].Successors.Count > 0
                        && !blocks[j].Successors.Contains(to))
                    {
                        AddSuccessor(blocks[j], to);
                        Console.Error.WriteLine(
                            $"[CFG_CLEAN] Reconnected class/func block 0x{to.StartOffset:X4} via predecessor 0x{blocks[j].StartOffset:X4}");
                        break;
                    }
                }
            }
        }
    }

    /// <summary>检测 block 是否为 class 或 function 定义的开头。</summary>
    private static bool IsClassOrFuncDefinition(BasicBlock block)
    {
        if (block.Instructions.Count == 0) return false;

        var firstOp = block.Instructions[0].Opcode;

        // class 定义: LOAD_BUILD_CLASS
        if (firstOp == Opcode.LOAD_BUILD_CLASS)
            return true;

        // 函数定义: 块以 LOAD_CONST(code_object) 或 LOAD_CLOSURE 开头，后跟 MAKE_FUNCTION
        if (firstOp == Opcode.LOAD_CONST || firstOp == Opcode.LOAD_CLOSURE)
        {
            return block.Instructions.Any(i =>
                i.Opcode == Opcode.MAKE_FUNCTION ||
                i.Opcode == Opcode.MAKE_CLOSURE);
        }

        return false;
    }
}
