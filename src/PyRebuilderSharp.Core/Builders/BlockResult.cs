using System.Text;
using PyRebuilderSharp.Core.Models.AST;
using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Core.Builders;

/// <summary>
/// 块级反编译结果。
/// 成功时包含 Statements，失败时包含 CommentFallback 字符串。
/// </summary>
public class BlockResult
{
    public bool IsSuccess { get; init; }
    public List<Stmt> Statements { get; init; } = new();
    public string CommentFallback { get; init; } = "";
    public string? ErrorMessage { get; init; }

    public static BlockResult Success(List<Stmt> stmts)
        => new() { IsSuccess = true, Statements = stmts };

    /// <summary>
    /// 创建注释兜底结果。
    /// 输出格式：
    ///   # ════════════════════════════════════════
    ///   # [Block #{id} Decompilation Failed]
    ///   # Offsets: 0x{start:X4} - 0x{end:X4}
    ///   # Engine: StackMachine
    ///   # Error: {message}
    ///   # Raw bytes: {hex}
    ///   # ════════════════════════════════════════
    /// </summary>
    public static BlockResult FallbackAsComment(
        List<Instruction> instructions,
        Exception exception,
        int blockId)
    {
        var first = instructions.FirstOrDefault();
        var last = instructions.LastOrDefault();
        var hex = string.Join(" ", instructions.Select(i => $"{(byte)i.Opcode:X2}"));

        var comment = new StringBuilder();
        comment.AppendLine($"# ════════════════════════════════════════");
        comment.AppendLine($"# [Block #{blockId} Decompilation Failed]");
        if (first != default)
            comment.AppendLine($"# Offsets: 0x{first.Offset:X4} - 0x{last.Offset:X4}");
        comment.AppendLine($"# Engine: StackMachine");
        comment.AppendLine($"# Error: {exception.Message}");
        if (hex.Length > 200)
            hex = hex[..197] + "...";
        comment.AppendLine($"# Raw bytes: {hex}");
        comment.AppendLine($"# ════════════════════════════════════════");

        return new BlockResult
        {
            CommentFallback = comment.ToString(),
            ErrorMessage = exception.Message
        };
    }
}
