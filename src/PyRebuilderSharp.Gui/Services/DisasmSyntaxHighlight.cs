using Avalonia.Controls.Documents;
using Avalonia.Media;
using System.Text.RegularExpressions;

namespace PyRebuilderSharp.Gui.Services;

/// <summary>
/// Python 字节码（dis）语法高亮器。
/// 
/// 配色与 VS Code 编辑器语义一致：
///   LineNumber → #858585（VS Code 行号）
///   Offset/Arg → #B5CEA8（number 色）
///   Opcode     → #569CD6（keyword 蓝色）
///   StringArg  → #CE9178（string 色）
///   CodeRef    → #DCDCAA（function 黄）
///   Punct      → #D4D4D4（default）
/// </summary>
public static class DisasmSyntaxHighlight
{
    private static readonly Lazy<SolidColorBrush> _lineNum = new(() => new(Color.Parse("#858585")));
    private static readonly Lazy<SolidColorBrush> _offset = new(() => new(Color.Parse("#B5CEA8")));
    private static readonly Lazy<SolidColorBrush> _opcode = new(() => new(Color.Parse("#569CD6")));
    private static readonly Lazy<SolidColorBrush> _argNum = new(() => new(Color.Parse("#B5CEA8")));
    private static readonly Lazy<SolidColorBrush> _stringArg = new(() => new(Color.Parse("#CE9178")));
    private static readonly Lazy<SolidColorBrush> _codeRef = new(() => new(Color.Parse("#DCDCAA")));
    private static readonly Lazy<SolidColorBrush> _punct = new(() => new(Color.Parse("#D4D4D4")));
    private static readonly Lazy<SolidColorBrush> _default = new(() => new(Color.Parse("#D4D4D4")));
    private static readonly Lazy<SolidColorBrush> _header = new(() => new(Color.Parse("#569CD6")));

    private static SolidColorBrush LineNum => _lineNum.Value;
    private static SolidColorBrush Offset => _offset.Value;
    private static SolidColorBrush Opcode => _opcode.Value;
    private static SolidColorBrush ArgNum => _argNum.Value;
    private static SolidColorBrush StringArg => _stringArg.Value;
    private static SolidColorBrush CodeRef => _codeRef.Value;
    private static SolidColorBrush Punct => _punct.Value;
    private static SolidColorBrush Default => _default.Value;
    private static SolidColorBrush Header => _header.Value;

    // 行首模式：可选行号 + offset + 操作码
    private static readonly Regex LinePattern = new(
        @"^(\s*)(\d+)?(\s+)(\d+)(\s+)([A-Z_]+)(\s+)(\d+)(\s*)(\(.*\))?$",
        RegexOptions.Compiled);

    // 嵌套代码头: "  Disassembly of <code xxx> at 0x..."
    private static readonly Regex HeaderPattern = new(
        @"^(Disassembly of |^\s{2,}Disassembly of )",
        RegexOptions.Compiled);

    public static List<(string Text, string Color)> Highlight(string source)
    {
        var result = new List<(string Text, string Color)>();
        if (string.IsNullOrEmpty(source)) return result;

        var lines = source.Split('\n');
        for (int li = 0; li < lines.Length; li++)
        {
            if (li > 0) result.Add(("\n", "#D4D4D4"));

            var line = lines[li];
            if (string.IsNullOrWhiteSpace(line)) continue;

            var m = LinePattern.Match(line);
            if (m.Success)
            {
                ColorizeLine(line, m, result);
            }
            else
            {
                if (HeaderPattern.IsMatch(line))
                    result.Add((line, "#569CD6"));
                else if (line.Contains("<code") || line.Contains("Disassembly of"))
                    result.Add((line, "#DCDCAA"));
                else
                    result.Add((line, "#D4D4D4"));
            }
        }
        return result;
    }

    private static void ColorizeLine(string line, Match m, List<(string Text, string Color)> result)
    {
        var pre = m.Groups[1].Value;
        if (pre.Length > 0) result.Add((pre, "#D4D4D4"));

        var ln = m.Groups[2].Value;
        if (ln.Length > 0)
        {
            result.Add((ln, "#858585"));
            result.Add((m.Groups[3].Value, "#D4D4D4"));
        }

        result.Add((m.Groups[4].Value, "#B5CEA8"));  // offset

        var sp1 = m.Groups[5].Value;
        var op = m.Groups[6].Value;
        result.Add((sp1, "#D4D4D4"));
        result.Add((op, "#569CD6"));  // opcode

        var sp2 = m.Groups[7].Value;
        var arg = m.Groups[8].Value;
        result.Add((sp2, "#D4D4D4"));
        result.Add((arg, "#B5CEA8"));  // arg number

        var sp3 = m.Groups[9].Value;
        var val = m.Groups[10].Value;
        result.Add((sp3, "#D4D4D4"));

        if (val.Length > 0)
        {
            // 括号
            result.Add((val[0].ToString(), "#D4D4D4"));
            var inner = val[1..^1];
            if (inner.Length == 0)
            {
                result.Add((")", "#D4D4D4"));
                return;
            }

            if (inner.StartsWith("'") && inner.EndsWith("'"))
                result.Add((inner, "#CE9178"));  // string
            else if (inner.Contains("<code"))
                result.Add((inner, "#DCDCAA"));  // code ref
            else
                result.Add((inner, "#B5CEA8"));  // other arg

            result.Add((")", "#D4D4D4"));
        }
    }
}
