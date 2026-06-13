using Avalonia.Media;
using System.Text.RegularExpressions;

namespace PyRebuilderSharp.Gui.Services;

/// <summary>
/// Python 语法高亮器 — 将源代码转换为带颜色的 Inline 元素。
/// 轻量级实现，无需额外依赖。
/// </summary>
public static class PythonSyntaxHighlighter
{
    private static readonly Color CommentColor = Color.Parse("#6A9955");
    private static readonly Color StringColor = Color.Parse("#CE9178");
    private static readonly Color NumberColor = Color.Parse("#B5CEA8");
    private static readonly Color KeywordColor = Color.Parse("#569CD6");
    private static readonly Color DecoratorColor = Color.Parse("#DCDCAA");
    private static readonly Color BuiltinColor = Color.Parse("#4FC1FF");
    private static readonly Color DefaultColor = Color.Parse("#D4D4D4");

    private static readonly HashSet<string> Keywords = new()
    {
        "False", "None", "True", "and", "as", "assert", "async", "await",
        "break", "class", "continue", "def", "del", "elif", "else", "except",
        "finally", "for", "from", "global", "if", "import", "in", "is",
        "lambda", "nonlocal", "not", "or", "pass", "raise", "return",
        "try", "while", "with", "yield"
    };

    private static readonly HashSet<string> Builtins = new()
    {
        "abs", "all", "any", "bin", "bool", "bytearray", "bytes", "callable",
        "chr", "classmethod", "complex", "dict", "dir", "enumerate", "eval",
        "exec", "filter", "float", "format", "frozenset", "getattr", "globals",
        "hasattr", "hash", "hex", "id", "input", "int", "isinstance", "issubclass",
        "iter", "len", "list", "locals", "map", "max", "min", "next", "object",
        "oct", "open", "ord", "pow", "print", "property", "range", "repr",
        "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod",
        "str", "sum", "super", "tuple", "type", "vars", "zip", "__import__"
    };

    /// <summary>
    /// 将 Python 源码转换为带行号和颜色的格式化字符串。
    /// 颜色使用 ANSI 风格标记（简化版，供 TextBlock 使用）。
    /// </summary>
    public static string FormatWithLineNumbers(string source)
    {
        if (string.IsNullOrEmpty(source)) return "(空)";

        var lines = source.Split('\n');
        var padWidth = lines.Length.ToString().Length;
        var result = new System.Text.StringBuilder();

        for (int i = 0; i < lines.Length; i++)
        {
            var lineNum = (i + 1).ToString().PadLeft(padWidth);
            var line = lines[i];
            result.AppendLine($"  {lineNum}│{line}");
        }

        return result.ToString();
    }
}
