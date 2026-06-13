namespace PyRebuilderSharp.Core.Models.Bytecode;

/// <summary>
/// Python 3.10+ 异常表条目。
/// 定义了 try/except/finally 的字节码范围。
/// </summary>
public class ExceptionTableEntry
{
    /// <summary>try body 起始偏移（字节）</summary>
    public int StartOffset { get; set; }
    
    /// <summary>try body 结束偏移（字节，不包含）</summary>
    public int EndOffset { get; set; }
    
    /// <summary>handler 入口偏移（字节）</summary>
    public int TargetOffset { get; set; }
    
    /// <summary>handler 深度：0=except, 1=finally, 2=except(with type match)</summary>
    public int Depth { get; set; }
    
    /// <summary>lasti 标记</summary>
    public bool Lasti { get; set; }

    /// <summary>
    /// 是否为 except handler（非 finally）。
    /// depth=0: bare except, depth=2: except with type
    /// </summary>
    public bool IsExcept => Depth == 0 || Depth == 2;

    /// <summary>
    /// 是否为 finally handler。
    /// </summary>
    public bool IsFinally => Depth == 1;

    public override string ToString()
        => $"ExcTbl[{StartOffset}..{EndOffset}) → {TargetOffset} depth={Depth}";
}
