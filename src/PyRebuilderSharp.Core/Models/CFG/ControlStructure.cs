using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Models.CFG;

/// <summary>
/// 控制结构抽象基类。
/// </summary>
public abstract record ControlStructure
{
    public BasicBlock Header { get; init; } = null!;
    public List<BasicBlock> BodyBlocks { get; init; } = new();
}

public record SequenceStructure(BasicBlock Header) : ControlStructure;

public record IfElseStructure(
    BasicBlock Header,
    BasicBlock? TrueBranch,
    BasicBlock? FalseBranch,
    BasicBlock? MergePoint
) : ControlStructure;

public record LoopStructure(
    BasicBlock Header,
    BasicBlock? BodyEntry,
    BasicBlock? BackEdge,
    BasicBlock? ElseBlock,
    LoopType Type
) : ControlStructure;

public enum LoopType { For, While, DoWhile, Infinite }

public record TryStructure(
    BasicBlock Header,
    BasicBlock? TryBody,
    List<(BasicBlock Handler, BasicBlock? Guard)> ExceptHandlers,
    BasicBlock? ElseBody,
    BasicBlock? FinallyBody
) : ControlStructure;
