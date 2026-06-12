using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Scanners;

namespace PyRebuilderSharp.Core.Models.CFG;

/// <summary>
/// 控制流图 - 整个函数的控制流表示。
/// </summary>
public class ControlFlowGraph
{
    /// <summary>入口块</summary>
    public BasicBlock Entry { get; init; } = null!;

    /// <summary>退出块（合成）</summary>
    public BasicBlock Exit { get; init; } = null!;

    /// <summary>所有基本块</summary>
    public List<BasicBlock> Blocks { get; } = new();

    /// <summary>偏移量到块的映射</summary>
    public Dictionary<int, BasicBlock> BlockByOffset { get; } = new();

    /// <summary>
    /// 获取所有跳转目标偏移量。
    /// </summary>
    public HashSet<int> GetAllJumpTargets()
    {
        var targets = new HashSet<int>();
        foreach (var block in Blocks)
        {
            var lastInstr = block.Instructions.LastOrDefault();
            if (lastInstr != default && JumpHelper.IsJump(lastInstr.Opcode))
            {
                if (lastInstr.Argument.HasValue)
                    targets.Add(lastInstr.Argument.Value);
            }
        }
        return targets;
    }
}
