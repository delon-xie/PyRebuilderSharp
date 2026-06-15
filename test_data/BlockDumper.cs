/// <summary>将异常表条目序列化为可读字符串。</summary>
public static string Format(ExceptionTableEntry e)
    => $"try[{e.StartOffset:X4}-{e.EndOffset:X4}]→handler@{e.TargetOffset:X4} depth={e.Depth}";

/// <summary>将基本块 cfg 图打印到 stderr。</summary>
public static void PrintBlocks(CodeObject code)
{
    Console.Error.WriteLine($"=== Block Graph ({code.Blocks.Count} blocks) ===");
    foreach (var b in code.Blocks)
    {
        var start = b.Instructions.Count > 0 ? b.Instructions[0].Offset : -1;
        var end = b.Instructions.Count > 0 ? b.Instructions.Last().Offset : -1;
        var succ = string.Join(", ", b.Successors.Select(s => s.Instructions.Count > 0 ? s.Instructions[0].Offset.ToString("X4") : "?"));
        var firstOp = b.Instructions.Count > 0 ? b.Instructions[0].Opcode + "" : "?";
        Console.Error.WriteLine($"  B@{start:X4}-{end:X4} [{firstOp}] succ=[{succ}] preds={b.Predecessors.Count}");
    }
    Console.Error.WriteLine($"=== ExceptionTable ({code.ExceptionTable.Count} entries) ===");
    foreach (var e in code.ExceptionTable)
        Console.Error.WriteLine($"  {Format(e)}");
}
