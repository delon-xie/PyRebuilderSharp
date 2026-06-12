using System.Globalization;
using System.Text.RegularExpressions;

namespace PyRebuilderSharp.Core.Testing;

/// <summary>
/// Abstract base class for all Python tokens, matching pycdc's PyToken hierarchy.
/// </summary>
public abstract class PyToken
{
    public TokenType Type { get; }
    public int LineNumber { get; }

    protected PyToken(TokenType type, int lineNumber)
    {
        Type = type;
        LineNumber = lineNumber;
    }

    public override bool Equals(object? obj)
    {
        if (obj is not PyToken other) return false;
        return Type == other.Type;
    }

    public override int GetHashCode() => Type.GetHashCode();

    public abstract override string ToString();
}

/// <summary>
/// Token for identifiers and keywords: [A-Za-z_][A-Za-z0-9_]*
/// Semantically compared by string equality of the word.
/// </summary>
public class WordToken : PyToken
{
    public string Word { get; }

    public WordToken(string word, int lineNumber) : base(TokenType.WORD, lineNumber)
    {
        Word = word;
    }

    public override bool Equals(object? obj)
    {
        if (!base.Equals(obj)) return false;
        if (obj is not WordToken other) return false;
        return Word == other.Word;
    }

    public override int GetHashCode() => HashCode.Combine(Type, Word);

    public override string ToString() => Word;
}

/// <summary>
/// Token for integer literals: decimal, hex (0x), binary (0b), octal (0o).
/// Supports underscore separators. Semantically compared by numeric value.
/// </summary>
public class IntToken : PyToken
{
    public long Value { get; }
    public string RawText { get; }

    public IntToken(string rawText, int lineNumber) : base(TokenType.INT, lineNumber)
    {
        RawText = rawText;
        Value = ParseInt(rawText);
    }

    private static long ParseInt(string text)
    {
        var cleaned = text.Replace("_", "");
        try
        {
            // int(text, 0) in Python — auto-detect base via prefix (0x, 0b, 0o)
            if (cleaned.StartsWith("0x", StringComparison.OrdinalIgnoreCase))
                return long.Parse(cleaned[2..], NumberStyles.HexNumber, CultureInfo.InvariantCulture);
            if (cleaned.StartsWith("0b", StringComparison.OrdinalIgnoreCase))
                return Convert.ToInt64(cleaned[2..], 2);
            if (cleaned.StartsWith("0o", StringComparison.OrdinalIgnoreCase))
                return Convert.ToInt64(cleaned[2..], 8);
            // Python 2.x octal: leading 0 but not 0x/0b/0o
            if (cleaned.Length > 1 && cleaned[0] == '0' && cleaned.All(c => c >= '0' && c <= '7'))
                return Convert.ToInt64(cleaned, 8);
            return long.Parse(cleaned, CultureInfo.InvariantCulture);
        }
        catch
        {
            return long.Parse(cleaned, CultureInfo.InvariantCulture);
        }
    }

    public override bool Equals(object? obj)
    {
        if (!base.Equals(obj)) return false;
        if (obj is not IntToken other) return false;
        return Value == other.Value;
    }

    public override int GetHashCode() => HashCode.Combine(Type, Value);

    public override string ToString() => Value.ToString(CultureInfo.InvariantCulture);
}

/// <summary>
/// Token for float literals. Semantically compared by approximate float value.
/// </summary>
public class FloatToken : PyToken
{
    public double Value { get; }

    public FloatToken(string rawText, int lineNumber) : base(TokenType.FLOAT, lineNumber)
    {
        Value = double.Parse(rawText.Replace("_", ""), NumberStyles.Float | NumberStyles.AllowExponent, CultureInfo.InvariantCulture);
    }

    public override bool Equals(object? obj)
    {
        if (!base.Equals(obj)) return false;
        if (obj is not FloatToken other) return false;
        return Math.Abs(Value - other.Value) < 1e-12;
    }

    public override int GetHashCode() => HashCode.Combine(Type, Value);

    public override string ToString() => Value.ToString("G", CultureInfo.InvariantCulture);
}

/// <summary>
/// Token for string literals with optional prefix (r, f, b, u, rb, br, etc.).
/// Prefix is normalized: lowercased and sorted (e.g., "rb" → "br").
/// Content has escape sequences normalized for semantic comparison.
/// </summary>
public class StringToken : PyToken
{
    public string Prefix { get; }
    public string Content { get; }
    public string RemainingLine { get; set; } = string.Empty;
    public int EndLine { get; set; }

    public StringToken(string prefix, string content, int lineNumber)
        : base(TokenType.STRING, lineNumber)
    {
        // Normalize prefix: lowercase and sort characters
        Prefix = string.Concat(prefix.ToLowerInvariant().OrderBy(c => c));
        // Normalize content for comparison (matching pycdc behavior)
        Content = NormalizeContent(content);
    }

    private static string NormalizeContent(string content)
    {
        return content
            .Replace("\\'", "'")
            .Replace("'", "\\'")
            .Replace("\\\"", "\"")
            .Replace("\t", "\\t")
            .Replace("\n", "\\n")
            .Replace("\r", "\\r");
    }

    public override bool Equals(object? obj)
    {
        if (!base.Equals(obj)) return false;
        if (obj is not StringToken other) return false;
        return Prefix == other.Prefix && Content == other.Content;
    }

    public override int GetHashCode() => HashCode.Combine(Type, Prefix, Content);

    public override string ToString() => $"{Prefix}'{Content}'";
}

/// <summary>
/// Token for operators, delimiters, and punctuation symbols.
/// Compared by the symbol string (e.g., "+=", "(", "{").
/// </summary>
public class SymbolToken : PyToken
{
    public string Symbol { get; }

    public SymbolToken(string symbol, int lineNumber) : base(TokenType.SYMBOL, lineNumber)
    {
        Symbol = symbol;
    }

    public override bool Equals(object? obj)
    {
        if (!base.Equals(obj)) return false;
        if (obj is not SymbolToken other) return false;
        return Symbol == other.Symbol;
    }

    public override int GetHashCode() => HashCode.Combine(Type, Symbol);

    public override string ToString() => Symbol;

    /// <summary>
    /// Check if this token is an opening bracket for context tracking.
    /// </summary>
    public bool IsOpeningBracket => Symbol is "(" or "{" or "[";

    /// <summary>
    /// Check if this token is a closing bracket for context tracking.
    /// </summary>
    public bool IsClosingBracket => Symbol is ")" or "}" or "]";

    /// <summary>
    /// Get the matching opening bracket for a closing bracket.
    /// </summary>
    public string MatchingOpeningBracket => Symbol switch
    {
        ")" => "(",
        "}" => "{",
        "]" => "[",
        _ => throw new InvalidOperationException($"Not a closing bracket: {Symbol}")
    };
}
