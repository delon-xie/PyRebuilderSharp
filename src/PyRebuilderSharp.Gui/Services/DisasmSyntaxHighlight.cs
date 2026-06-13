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
    private static readonly SolidColorBrush
        LineNum   = new(Color.Parse("#858585")),
        Offset    = new(Color.Parse("#B5CEA8")),
        Opcode    = new(Color.Parse("#569CD6")),
        ArgNum    = new(Color.Parse("#B5CEA8")),
        StringArg = new(Color.Parse("#CE9178")),
        CodeRef   = new(Color.Parse("#DCDCAA")),
        Punct     = new(Color.Parse("#D4D4D4")),
        Default   = new(Color.Parse("#D4D4D4")),
        Header    = new(Color.Parse("#569CD6"));

    // 行首模式：可选行号 + offset + 操作码
    private static readonly Regex LinePattern = new(
        @"^(\s*)(\d+)?(\s+)(\d+)(\s+)([A-Z_]+)(\s+)(\d+)(\s*)(\(.*\))?$",
        RegexOptions.Compiled);

    // 嵌套代码头: "  Disassembly of <code xxx> at 0x..."
    private static readonly Regex HeaderPattern = new(
        @"^(Disassembly of |^\s{2,}Disassembly of )",
        RegexOptions.Compiled);

    public static InlineCollection Highlight(string source)
    {
        var inlines = new InlineCollection();
        if (string.IsNullOrEmpty(source)) return inlines;

        var lines = source.Split('\n');
        for (int li = 0; li < lines.Length; li++)
        {
            if (li > 0) inlines.Add(new Run("\n"));

            var line = lines[li];
            if (string.IsNullOrWhiteSpace(line)) continue;

            var m = LinePattern.Match(line);
            if (m.Success)
            {
                // 前缀空格
                var pre = m.Groups[1].Value;
                if (pre.Length > 0) inlines.Add(new Run(pre) { Foreground = Default });

                // 行号（有则启用，无则跳过）
                var ln = m.Groups[2].Value;
                if (ln.Length > 0)
                {
                    inlines.Add(new Run(ln) { Foreground = LineNum });
                    inlines.Add(new Run(m.Groups[3].Value) { Foreground = Default });
                }

                // offset
                inlines.Add(new Run(m.Groups[4].Value) { Foreground = Offset });

                // 空格 + opcode
                var sp1 = m.Groups[5].Value;
                var op = m.Groups[6].Value;
                inlines.Add(new Run(sp1) { Foreground = Default });
                inlines.Add(new Run(op) { Foreground = Opcode });

                // 空格 + arg index
                var sp2 = m.Groups[7].Value;
                var arg = m.Groups[8].Value;
                inlines.Add(new Run(sp2) { Foreground = Default });
                inlines.Add(new Run(arg) { Foreground = ArgNum });

                // 空格 + arg value (括号中的值)
                var sp3 = m.Groups[9].Value;
                var val = m.Groups[10].Value;
                inlines.Add(new Run(sp3) { Foreground = Default });

                if (val.Length > 0)
                {
                    ColorizeArgValue(val, inlines);
                }
            }
            else
            {
                // 非指令行：header / 代码名 / 空行
                if (HeaderPattern.IsMatch(line))
                {
                    inlines.Add(new Run(line) { Foreground = Header });
                }
                else if (line.Contains("<code") || line.Contains("Disassembly of"))
                {
                    inlines.Add(new Run(line) { Foreground = CodeRef });
                }
                else
                {
                    inlines.Add(new Run(line) { Foreground = Default });
                }
            }
        }
        return inlines;
    }

    /// <summary>
    /// 对参数值 (括号中的内容) 进行颜色化：
    ///   '字符串' → 橙色
    ///   <code xxx> → 黄色
    ///   数字/None/True/False → 青色
    /// </summary>
    private static void ColorizeArgValue(string val, InlineCollection inlines)
    {
        // 括号本身
        inlines.Add(new Run(val[0].ToString()) { Foreground = Punct });

        var inner = val[1..^1];  // 去掉首尾括号
        if (inner.Length == 0)
        {
            inlines.Add(new Run(")") { Foreground = Punct });
            return;
        }

        if (inner.StartsWith("'") && inner.EndsWith("'"))
        {
            // 字符串参数
            inlines.Add(new Run(inner) { Foreground = StringArg });
        }
        else if (inner.Contains("<code"))
        {
            // 嵌套代码引用
            inlines.Add(new Run(inner) { Foreground = CodeRef });
        }
        else if (inner is "None" or "True" or "False")
        {
            inlines.Add(new Run(inner) { Foreground = ArgNum });
        }
        else
        {
            inlines.Add(new Run(inner) { Foreground = ArgNum });
        }

        inlines.Add(new Run(")") { Foreground = Punct });
    }
}
