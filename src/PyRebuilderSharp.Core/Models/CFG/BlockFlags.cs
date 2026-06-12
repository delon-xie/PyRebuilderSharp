namespace PyRebuilderSharp.Core.Models.CFG;

/// <summary>
/// 基本块属性标志。
/// </summary>
[Flags]
public enum BlockFlags
{
    None = 0,
    Entry = 1 << 0,
    Exit = 1 << 1,
    LoopHeader = 1 << 2,
    LoopBody = 1 << 3,
    LoopBackEdge = 1 << 4,
    ConditionHeader = 1 << 5,
    TrueBranch = 1 << 6,
    FalseBranch = 1 << 7,
    ExceptionHandler = 1 << 8,
    FinallyBlock = 1 << 9,
    Synthetic = 1 << 10,
    Dead = 1 << 11
}
