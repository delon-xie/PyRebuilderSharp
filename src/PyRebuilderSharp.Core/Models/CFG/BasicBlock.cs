using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Models.CFG;

/// <summary>
/// 基本块 - 控制流图中的最小单位。
/// 包含连续的、无分支的指令序列。
/// </summary>
public class BasicBlock
{
    private static int _nextId;

    /// <summary>全局唯一标识</summary>
    public int Id { get; } = Interlocked.Increment(ref _nextId);

    /// <summary>起始偏移量</summary>
    public int StartOffset { get; init; }

    /// <summary>结束偏移量</summary>
    public int EndOffset { get; init; }

    /// <summary>块内指令列表</summary>
    public List<Instruction> Instructions { get; } = new();

    // ---- 控制流关系 ----
    public HashSet<BasicBlock> Predecessors { get; } = new();
    public HashSet<BasicBlock> Successors { get; } = new();

    // ---- 异常处理关系 ----
    public HashSet<BasicBlock> ExceptionHandlers { get; } = new();
    public BasicBlock? FinallyBlock { get; set; }

    // ---- 块属性 ----
    public BlockFlags Flags { get; set; } = BlockFlags.None;

    public override string ToString()
        => $"BB#{Id}[0x{StartOffset:X4}-0x{EndOffset:X4}]";
}
