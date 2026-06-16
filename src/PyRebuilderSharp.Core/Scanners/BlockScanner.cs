using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.CFG;

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
        LinkBlocks(blocks, codeObj.ExceptionTable);
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
            else if (instr.Opcode == Opcode.SETUP_FINALLY || instr.Opcode == Opcode.SETUP_EXCEPT)
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

        return leaders;
    }

    /// <summary>
    /// 解析跳转目标为绝对偏移。
    /// JUMP_FORWARD/FOR_ITER/SETUP_FINALLY 使用相对偏移，
    /// JUMP_ABSOLUTE 使用绝对偏移，
    /// JUMP_BACKWARD 使用反向相对偏移。
    /// 3.12+ wordcode: 条件跳转（POP_JUMP_IF_TRUE/FALSE 等）参数已转为字节偏移，
    /// 需要计算 instr.Offset + 2 + arg 得到绝对目标。
    /// </summary>
    private static int? ResolveJumpTarget(Instruction instr, CodeObject? codeObj = null)
    {
        if (!instr.Argument.HasValue) return null;

        // 检测 wordcode: 3.11+ 所有指令均为 2 字节，偏移均为偶数
        // 而非 wordcode（3.10-）的指令长度可变（1或3字节），可能存在奇数偏移
        // 注意：此检测需在所有指令上检查，因为简单函数可能无 ExceptionTable
        bool isWordcode = codeObj?.Instructions != null
            && codeObj.Instructions.Count > 1
            && codeObj.Instructions.All(i => i.Offset % 2 == 0);

        return instr.Opcode switch
        {
            Opcode.JUMP_ABSOLUTE => instr.Argument.Value,
            Opcode.JUMP_FORWARD or Opcode.FOR_ITER
                => instr.Offset + 2 + instr.Argument.Value,
            Opcode.JUMP_BACKWARD => instr.Offset + 2 - instr.Argument.Value,
            // 3.12+ wordcode: 条件跳转参数是相对字节偏移，需加上当前指令+2
            Opcode.POP_JUMP_IF_TRUE or Opcode.POP_JUMP_IF_FALSE
                or Opcode.JUMP_IF_TRUE_OR_POP or Opcode.JUMP_IF_FALSE_OR_POP
                when isWordcode => instr.Offset + 2 + instr.Argument.Value,
            _ => instr.Argument.Value
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

    private void LinkBlocks(List<BasicBlock> blocks, List<ExceptionTableEntry>? exceptionTable = null)
    {
        for (int i = 0; i < blocks.Count; i++)
        {
            var block = blocks[i];
            var lastInstr = block.Instructions.LastOrDefault();

            if (lastInstr == default) continue;

            switch (lastInstr.Opcode)
            {
                case Opcode.RETURN_VALUE:
                case Opcode.RAISE_VARARGS:
                    block.Flags |= BlockFlags.Exit;
                    ResolveIntermediateJumps(block, blocks);
                    // Exit blocks (RERAISE) still need a sequential fallthrough
                    // for try/except handler → code after try/except
                    if (i + 1 < blocks.Count)
                        AddSuccessor(block, blocks[i + 1]);                    break;

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
                                var target = ResolveJumpTarget(ins)!.Value;
                                AddSuccessor(block, FindBlockByOffset(blocks, target));
                            }
                        }
                    }
                    else
                    {
                        AddSuccessor(block, FindBlockByOffset(blocks, ResolveJumpTarget(lastInstr)!.Value));
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
                                AddSuccessor(block, FindBlockByOffset(blocks, ResolveJumpTarget(ins)!.Value));
                        }
                    }
                    break;

                case Opcode.POP_JUMP_IF_TRUE:
                case Opcode.POP_JUMP_IF_FALSE:
                case Opcode.JUMP_IF_TRUE_OR_POP:
                case Opcode.JUMP_IF_FALSE_OR_POP:
                case Opcode.FOR_ITER:
                    AddSuccessor(block, FindBlockByOffset(blocks, ResolveJumpTarget(lastInstr)!.Value));
                    if (i + 1 < blocks.Count)
                        AddSuccessor(block, blocks[i + 1]);
                    break;

                default:
                    if (i + 1 < blocks.Count)
                        AddSuccessor(block, blocks[i + 1]);
                    break;
            }
        }

        // 3.11+: ExceptionTable handler 边 — try 体 → handler 块
        if (exceptionTable != null)
        {
            foreach (var entry in exceptionTable)
            {
                var handlerBlock = FindBlockByOffset(blocks, entry.TargetOffset);
                if (handlerBlock == null) continue;

                // 找出 try 体覆盖范围的最后一个块
                for (int j = 0; j < blocks.Count; j++)
                {
                    if (blocks[j].StartOffset >= entry.StartOffset
                        && blocks[j].EndOffset <= entry.EndOffset)
                    {
                        AddSuccessor(blocks[j], handlerBlock);
                    }
                    if (blocks[j].StartOffset > entry.EndOffset) break;
                }
            }
        }
    }

    private void ResolveIntermediateJumps(BasicBlock block, List<BasicBlock> blocks)
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
                    var target = ResolveJumpTarget(ins);
                    if (target.HasValue)
                        AddSuccessor(block, FindBlockByOffset(blocks, target.Value));
                }
            }
        }
    }

    private void AddSuccessor(BasicBlock from, BasicBlock? to)
    {
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
}
