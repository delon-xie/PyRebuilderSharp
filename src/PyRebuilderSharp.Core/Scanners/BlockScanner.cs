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

        var leaders = MarkLeaders(instructions);
        var blocks = SplitAtLeaders(instructions, leaders);
        LinkBlocks(blocks);
        MarkBlockProperties(blocks);

        return blocks;
    }

    /// <summary>
    /// 标记Leader指令。
    /// Leader是基本块的起始指令。
    /// </summary>
    private SortedSet<int> MarkLeaders(List<Instruction> instructions)
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
                var target = ResolveJumpTarget(instr);
                if (target.HasValue)
                    leaders.Add(target.Value);
                if (i + 1 < instructions.Count)
                    leaders.Add(instructions[i + 1].Offset);
            }
            else if (JumpHelper.IsUnconditionalJump(instr.Opcode))
            {
                var target = ResolveJumpTarget(instr);
                if (target.HasValue)
                    leaders.Add(target.Value);
            }
            // SETUP_FINALLY: 异常处理器入口也要标记为 leader
            else if (instr.Opcode == Opcode.SETUP_FINALLY)
            {
                if (instr.Argument.HasValue)
                {
                    // 在 Python 3.8 中 SETUP_FINALLY 偏移量是相对于当前指令后的
                    var handlerOffset = instr.Offset + 2 + instr.Argument.Value;
                    leaders.Add(handlerOffset);
                }
            }
        }

        return leaders;
    }

    /// <summary>
    /// 解析跳转目标为绝对偏移。
    /// JUMP_FORWARD/FOR_ITER/SETUP_FINALLY 使用相对偏移，
    /// JUMP_ABSOLUTE 使用绝对偏移，
    /// JUMP_BACKWARD 使用反向相对偏移。
    /// </summary>
    private static int? ResolveJumpTarget(Instruction instr)
    {
        if (!instr.Argument.HasValue) return null;
        return instr.Opcode switch
        {
            Opcode.JUMP_ABSOLUTE => instr.Argument.Value,
            Opcode.JUMP_FORWARD or Opcode.FOR_ITER
                => instr.Offset + 2 + instr.Argument.Value,
            Opcode.JUMP_BACKWARD => instr.Offset - instr.Argument.Value,
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

    private void LinkBlocks(List<BasicBlock> blocks)
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
                    break;

                case Opcode.JUMP_ABSOLUTE:
                case Opcode.JUMP_FORWARD:
                case Opcode.JUMP_BACKWARD:
                    AddSuccessor(block, FindBlockByOffset(blocks, ResolveJumpTarget(lastInstr)!.Value));
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
}
