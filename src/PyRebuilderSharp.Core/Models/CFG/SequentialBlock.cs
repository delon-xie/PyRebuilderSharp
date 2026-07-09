using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.AST;

namespace PyRebuilderSharp.Core.Models.CFG;

public class SequentialBlock
{
    private static int _nextId;

    public int Id { get; } = Interlocked.Increment(ref _nextId);
    
    public int StartOffset { get; set; }
    
    public int EndOffset { get; set; }
    
    public List<Instruction> Instructions { get; } = new();
    
    public List<BasicBlock> SourceBlocks { get; } = new();
    
    public bool HasSetupWith { get; set; }
    
    public bool HasSetupFinally { get; set; }
    
    public bool HasSetupExcept { get; set; }
    
    public bool HasBeforeWith { get; set; }
    
    public bool HasLoadSpecial { get; set; }
    
    public bool EndsWithJump { get; set; }
    
    public int? JumpTarget { get; set; }
    
    public bool IsLoopHeader { get; set; }
    
    public bool IsConditionHeader { get; set; }
    
    public bool IsExceptionHandler { get; set; }
    
    // Phase 2: ExceptionTable 标注
    public bool IsTryHeader { get; set; }
    
    public bool IsExceptBlock { get; set; }
    
    public int ExceptionTryStartOffset { get; set; }
    
    public int ExceptionTryEndOffset { get; set; }
    
    // Phase 3: 控制块起始标注
    public bool IsWithHeader { get; set; }
    
    // Phase 4: 回边标注
    public bool IsBackEdgeTarget { get; set; }
    
    public bool IsLoopBody { get; set; }
    
    // Phase 2a: Match/Case 标注
    public bool IsMatchHeader { get; set; }
    
    public bool IsCaseEntry { get; set; }
    
    // Phase 2b: For/While 细分标注
    public bool IsForLoopHeader { get; set; }
    
    public bool IsWhileLoopHeader { get; set; }
    
    public int ForIterExitTarget { get; set; }
    
    public bool IsForIterBody { get; set; }
    
    // Phase 2c: Handler 深度标注
    public int HandlerDepth { get; set; } = -1;
    
    public bool IsFinallyBlock { get; set; }
    
    public bool IsTryElseBlock { get; set; }
    
    // Phase 3b: 汇聚点/出口标注
    public bool IsMergePoint { get; set; }
    
    public bool IsBreakTarget { get; set; }
    
    public bool IsContinueTarget { get; set; }
    
    public int StructureExitOffset { get; set; }
    
    public bool IsDeadCodeBlock { get; set; }
    
    public int PredecessorCount { get; set; }
    
    public int SuccessorCount { get; set; }
    
    public List<SequentialBlock> Successors { get; } = new();
    
    public List<ExceptionTableEntry> ExceptionTableEntries { get; } = new();
    
    public List<Stmt>? Statements { get; set; }
    
    public bool IsProcessed { get; set; }
    
    public ISequentialControlStructure? ParentStructure { get; set; }

    public override string ToString()
        => $"SB#{Id}[0x{StartOffset:X4}-0x{EndOffset:X4}]";
}

public enum ControlStructureType
{
    Unknown,
    ForLoop,
    WhileLoop,
    With,
    Try,
    IfElse
}

public interface ISequentialControlStructure
{
    ControlStructureType Type { get; }
    SequentialBlock Header { get; }
    List<SequentialBlock> BodyBlocks { get; }
}

public class ForLoopControlStructure : ISequentialControlStructure
{
    public ControlStructureType Type => ControlStructureType.ForLoop;
    public SequentialBlock Header { get; set; } = null!;
    public SequentialBlock? BodyEntry { get; set; }
    public SequentialBlock? BackEdge { get; set; }
    public SequentialBlock? ElseBlock { get; set; }
    public List<SequentialBlock> BodyBlocks { get; } = new();

    public ForLoopControlStructure(SequentialBlock header, SequentialBlock? bodyEntry, SequentialBlock? backEdge, SequentialBlock? elseBlock, List<SequentialBlock> bodyBlocks)
    {
        Header = header;
        BodyEntry = bodyEntry;
        BackEdge = backEdge;
        ElseBlock = elseBlock;
        BodyBlocks.AddRange(bodyBlocks);
    }
}

public class WhileLoopControlStructure : ISequentialControlStructure
{
    public ControlStructureType Type => ControlStructureType.WhileLoop;
    public SequentialBlock Header { get; set; } = null!;
    public SequentialBlock? BodyEntry { get; set; }
    public SequentialBlock? BackEdge { get; set; }
    public SequentialBlock? ElseBlock { get; set; }
    public List<SequentialBlock> BodyBlocks { get; } = new();

    public WhileLoopControlStructure(SequentialBlock header, SequentialBlock? bodyEntry, SequentialBlock? backEdge, SequentialBlock? elseBlock, List<SequentialBlock> bodyBlocks)
    {
        Header = header;
        BodyEntry = bodyEntry;
        BackEdge = backEdge;
        ElseBlock = elseBlock;
        BodyBlocks.AddRange(bodyBlocks);
    }
}

public class WithControlStructure : ISequentialControlStructure
{
    public ControlStructureType Type => ControlStructureType.With;
    public SequentialBlock Header { get; set; } = null!;
    public SequentialBlock? HandlerBlock { get; set; }
    public List<SequentialBlock> BodyBlocks { get; } = new();

    public WithControlStructure(SequentialBlock header, SequentialBlock? handlerBlock, List<SequentialBlock> bodyBlocks)
    {
        Header = header;
        HandlerBlock = handlerBlock;
        BodyBlocks.AddRange(bodyBlocks);
    }
}

public class TryControlStructure : ISequentialControlStructure
{
    public ControlStructureType Type => ControlStructureType.Try;
    public SequentialBlock Header { get; set; } = null!;
    public List<(SequentialBlock Handler, string? ExceptionType, string? ExceptionVar)> ExceptHandlers { get; } = new();
    public SequentialBlock? ElseBlock { get; set; }
    public SequentialBlock? FinallyBlock { get; set; }
    public List<SequentialBlock> BodyBlocks { get; } = new();

    public TryControlStructure(SequentialBlock header, List<(SequentialBlock Handler, string? ExceptionType, string? ExceptionVar)> exceptHandlers, SequentialBlock? elseBlock, SequentialBlock? finallyBlock, List<SequentialBlock> bodyBlocks)
    {
        Header = header;
        ExceptHandlers = exceptHandlers;
        ElseBlock = elseBlock;
        FinallyBlock = finallyBlock;
        BodyBlocks.AddRange(bodyBlocks);
    }
}

public class IfElseControlStructure : ISequentialControlStructure
{
    public ControlStructureType Type => ControlStructureType.IfElse;
    public SequentialBlock Header { get; set; } = null!;
    public SequentialBlock? TrueBranch { get; set; }
    public SequentialBlock? FalseBranch { get; set; }
    public SequentialBlock? MergePoint { get; set; }
    public List<SequentialBlock> BodyBlocks { get; } = new();

    public IfElseControlStructure(SequentialBlock header, SequentialBlock? trueBranch, SequentialBlock? falseBranch, SequentialBlock? mergePoint, List<SequentialBlock> bodyBlocks)
    {
        Header = header;
        TrueBranch = trueBranch;
        FalseBranch = falseBranch;
        MergePoint = mergePoint;
        BodyBlocks.AddRange(bodyBlocks);
    }
}