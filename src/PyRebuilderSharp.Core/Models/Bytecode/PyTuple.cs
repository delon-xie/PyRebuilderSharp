namespace PyRebuilderSharp.Core.Models.Bytecode;

/// <summary>
/// 标记 Python tuple 类型（区别于 list）。
/// Marshal 解析时用此包装 tuple 数据。
/// </summary>
public class PyTuple : List<object?>
{
    public PyTuple() { }
    public PyTuple(IEnumerable<object?> items) : base(items) { }
}

/// <summary>
/// Python slice(start, stop, step) 对象的常量表示。
/// 当 slice 作为预计算常量存储在 co_consts 中时使用。
/// </summary>
public record PySliceData(object? Start, object? Stop, object? Step);
