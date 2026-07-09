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
    // 惰性初始化 — 避免在后台线程静态度量时 Avalonia Color.Parse 崩溃
    private static readonly Lazy<SolidColorBrush> _controlKeyword = new(() => new(Color.Parse("#C586C0")));
    private static readonly Lazy<SolidColorBrush> _blueKeyword = new(() => new(Color.Parse("#569CD6")));
    private static readonly Lazy<SolidColorBrush> _stringCol = new(() => new(Color.Parse("#CE9178")));
    private static readonly Lazy<SolidColorBrush> _numberCol = new(() => new(Color.Parse("#B5CEA8")));
    private static readonly Lazy<SolidColorBrush> _commentCol = new(() => new(Color.Parse("#6A9955")));
    private static readonly Lazy<SolidColorBrush> _functionCol = new(() => new(Color.Parse("#DCDCAA")));
    private static readonly Lazy<SolidColorBrush> _classCol = new(() => new(Color.Parse("#4EC9B0")));
    private static readonly Lazy<SolidColorBrush> _constantCol = new(() => new(Color.Parse("#4EC9B0")));
    private static readonly Lazy<SolidColorBrush> _builtinCol = new(() => new(Color.Parse("#DCDCAA")));
    private static readonly Lazy<SolidColorBrush> _decoratorCol = new(() => new(Color.Parse("#DCDCAA")));
    private static readonly Lazy<SolidColorBrush> _defaultCol = new(() => new(Color.Parse("#D4D4D4")));

    // 缩写属性
    private static SolidColorBrush ControlKeyword => _controlKeyword.Value;
    private static SolidColorBrush BlueKeyword => _blueKeyword.Value;
    private static SolidColorBrush StringCol => _stringCol.Value;
    private static SolidColorBrush NumberCol => _numberCol.Value;
    private static SolidColorBrush CommentCol => _commentCol.Value;
    private static SolidColorBrush FunctionCol => _functionCol.Value;
    private static SolidColorBrush ClassCol => _classCol.Value;
    private static SolidColorBrush ConstantCol => _constantCol.Value;
    private static SolidColorBrush BuiltinCol => _builtinCol.Value;
    private static SolidColorBrush DecoratorCol => _decoratorCol.Value;
    private static SolidColorBrush DefaultCol => _defaultCol.Value;

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

    /// <summary>
    /// 返回颜色化后的文本段列表（不创建 Avalonia 对象，安全地从后台线程调用）
    /// </summary>
    public static List<(string Text, string Color)> Highlight(string source)
    {
        var result = new List<(string Text, string Color)>();
        if (string.IsNullOrEmpty(source)) return result;

        var lines = source.Split('\n');
        for (int li = 0; li < lines.Length; li++)
        {
            if (li > 0) result.Add(("\n", "#D4D4D4"));
            ParseLine(lines[li], result);
        }
        return result;
    }

    private static void ParseLine(string line, List<(string Text, string Color)> result)
    {
        int i = 0;
        while (i < line.Length)
        {
            if (line[i] == '#')
            {
                result.Add((line[i..], "#6A9955"));
                return;
            }

            if (line[i] == '\'' || line[i] == '"')
            {
                int end = FindStringEnd(line, i, line[i]);
                var s = end > 0 ? line[i..(end + 1)] : line[i..];
                result.Add((s, "#CE9178"));
                i = end > 0 ? end + 1 : line.Length;
                continue;
            }

            if (char.IsDigit(line[i]) || (line[i] == '.' && i + 1 < line.Length && char.IsDigit(line[i + 1])))
            {
                int s = i; i++;
                while (i < line.Length && IsDigitPart(line[i]) && line[i] != '#' && line[i] != '\'' && line[i] != '"')
                    i++;
                result.Add((line[s..i], "#B5CEA8"));
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
                    result.Add((word, "#DCDCAA"));
                }
                else if (ControlKeywords.Contains(word))
                {
                    result.Add((word, "#C586C0"));
                }
                else if (BlueKeywords.Contains(word))
                {
                    var color = word is "True" or "False" or "None" ? "#4EC9B0" : "#569CD6";
                    result.Add((word, color));
                }
                else if (Builtins.Contains(word))
                {
                    result.Add((word, "#DCDCAA"));
                }
                else
                {
                    result.Add((word, "#D4D4D4"));
                }
                continue;
            }

            result.Add((line[i].ToString(), "#D4D4D4"));
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
