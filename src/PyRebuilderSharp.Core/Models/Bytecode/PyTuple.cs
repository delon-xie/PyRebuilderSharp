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
