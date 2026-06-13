using Avalonia.Controls.Documents;
using Avalonia.Media;

namespace PyRebuilderSharp.Gui.Services;

/// <summary>
/// VS Code Dark+ (default) 精确配色的 Python 语法高亮器。
/// 
/// 参考 VS Code 的 Python TextMate 语义着色：
///   keyword.control      → #C586C0  紫色 — def, class, async, await
///   keyword.declaration   → #569CD6  蓝色 — if, for, while, import
///   entity.name.function  → #DCDCAA  黄色 — 函数名
///   entity.name.class     → #4EC9B0  青色 — 类名
///   support.function      → #DCDCAA  黄色 — print, len 等内置调用
///   constant.language     → #4EC9B0  青色 — True, False, None
///   string                → #CE9178  橙色
///   number                → #B5CEA8  浅绿
///   comment               → #6A9955  绿色
///   storage.type          → #569CD6  蓝色 — int, str, list, dict
/// </summary>
public static class PythonSyntaxHighlight
{
    private static readonly SolidColorBrush
        ControlKeyword = new(Color.Parse("#C586C0")),  // def, class, async, await
        BlueKeyword    = new(Color.Parse("#569CD6")),  // if, for, import, return
        StringCol      = new(Color.Parse("#CE9178")),
        NumberCol      = new(Color.Parse("#B5CEA8")),
        CommentCol     = new(Color.Parse("#6A9955")),
        FunctionCol    = new(Color.Parse("#DCDCAA")),  // 函数名
        ClassCol       = new(Color.Parse("#4EC9B0")),  // 类名
        ConstantCol    = new(Color.Parse("#4EC9B0")),  // True/False/None
        BuiltinCol     = new(Color.Parse("#DCDCAA")),  // print, len 等
        DecoratorCol   = new(Color.Parse("#DCDCAA")),
        DefaultCol     = new(Color.Parse("#D4D4D4"));

    // 紫色控制关键字
    private static readonly HashSet<string> ControlKeywords = new()
    { "def", "class", "async", "await" };

    // 蓝色声明关键字
    private static readonly HashSet<string> BlueKeywords = new()
    { "False", "None", "True", "and", "as", "assert", "break", "continue",
      "del", "elif", "else", "except", "finally", "for", "from", "global",
      "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass",
      "raise", "return", "try", "while", "with", "yield" };

    // 内置函数（黄色，同函数调用）
    private static readonly HashSet<string> Builtins = new()
    { "abs", "all", "any", "bin", "bool", "bytearray", "bytes", "callable",
      "chr", "classmethod", "complex", "dict", "dir", "enumerate", "eval",
      "exec", "filter", "float", "format", "frozenset", "getattr", "globals",
      "hasattr", "hash", "hex", "id", "input", "int", "isinstance", "issubclass",
      "iter", "len", "list", "locals", "map", "max", "min", "next", "object",
      "oct", "open", "ord", "pow", "print", "property", "range", "repr",
      "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod",
      "str", "sum", "super", "tuple", "type", "vars", "zip", "__import__" };

    public static InlineCollection Highlight(string source)
    {
        var inlines = new InlineCollection();
        if (string.IsNullOrEmpty(source)) return inlines;

        var lines = source.Split('\n');
        for (int li = 0; li < lines.Length; li++)
        {
            if (li > 0) inlines.Add(new Run("\n"));
            ParseLine(lines[li], inlines);
        }
        return inlines;
    }

    private static void ParseLine(string line, InlineCollection inlines)
    {
        int i = 0;
        while (i < line.Length)
        {
            if (line[i] == '#')
            {
                inlines.Add(new Run(line[i..]) { Foreground = CommentCol });
                return;
            }

            if (line[i] == '\'' || line[i] == '"')
            {
                int end = FindStringEnd(line, i, line[i]);
                var s = end > 0 ? line[i..(end + 1)] : line[i..];
                inlines.Add(new Run(s) { Foreground = StringCol });
                i = end > 0 ? end + 1 : line.Length;
                continue;
            }

            if (char.IsDigit(line[i]) || (line[i] == '.' && i + 1 < line.Length && char.IsDigit(line[i + 1])))
            {
                int s = i; i++;
                while (i < line.Length && IsDigitPart(line[i]) && line[i] != '#' && line[i] != '\'' && line[i] != '"')
                    i++;
                inlines.Add(new Run(line[s..i]) { Foreground = NumberCol });
                continue;
            }

            if (char.IsLetter(line[i]) || line[i] == '_')
            {
                int s = i;
                while (i < line.Length && (char.IsLetterOrDigit(line[i]) || line[i] == '_'))
                    i++;
                var word = line[s..i];

                if (s > 0 && line[s - 1] == '@')
                {
                    inlines.Add(new Run(word) { Foreground = DecoratorCol });
                }
                else if (ControlKeywords.Contains(word))
                {
                    inlines.Add(new Run(word) { Foreground = ControlKeyword, FontWeight = FontWeight.Bold });
                }
                else if (BlueKeywords.Contains(word))
                {
                    var color = ("TrueFalseNone".Contains(word) && word.Length > 2)
                        ? ConstantCol : BlueKeyword;
                    // True/False/None → 青色, 其他关键字 → 蓝色
                    color = word is "True" or "False" or "None" ? ConstantCol : BlueKeyword;
                    var fw = word is "True" or "False" or "None" ? FontWeight.Normal : FontWeight.Normal;
                    inlines.Add(new Run(word) { Foreground = color, FontWeight = fw });
                }
                else if (Builtins.Contains(word))
                {
                    inlines.Add(new Run(word) { Foreground = BuiltinCol });
                }
                else
                {
                    inlines.Add(new Run(word) { Foreground = DefaultCol });
                }
                continue;
            }

            inlines.Add(new Run(line[i].ToString()) { Foreground = DefaultCol });
            i++;
        }
    }

    private static bool IsDigitPart(char c) =>
        "0123456789abcdefABCDEF.xXoObBeEjJ_".Contains(c);

    private static int FindStringEnd(string line, int start, char quote)
    {
        for (int i = start + 1; i < line.Length; i++)
        {
            if (line[i] == '\\') { i++; continue; }
            if (line[i] == quote) return i;
        }
        return -1;
    }
}
