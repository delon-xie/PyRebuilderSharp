namespace PyRebuilderSharp.Core.Models.CFG;

/// <summary>
/// 结构化控制流图 - 包含高级控制结构信息。
/// </summary>
public class StructuredCFG
{
    public ControlFlowGraph RawCFG { get; init; } = null!;
    public List<ControlStructure> Structures { get; } = new();
    public Dictionary<BasicBlock, ControlStructure> BlockToStructure { get; } = new();
}
