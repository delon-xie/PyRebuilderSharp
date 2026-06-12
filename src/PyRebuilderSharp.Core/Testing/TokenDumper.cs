using System.Globalization;
using System.Text;
using System.Text.RegularExpressions;

namespace PyRebuilderSharp.Core.Testing;

/// <summary>
/// Python tokenizer matching pycdc's token_dump behavior.
/// Tokenizes Python source code with indentation tracking, bracket context,
/// and semantic token types for diff-based comparison.
/// </summary>
public partial class TokenDumper
{
    // Regex for whitespace
    [GeneratedRegex(@"\s+")]
    private static partial Regex WhitespaceRegex();

    // Identifier tokens: [A-Za-z_][A-Za-z0-9_]*
    [GeneratedRegex(@"[A-Za-z_][A-Za-z0-9_]*")]
    private static partial Regex WordRegex();

    // Integer literals: decimal, hex, binary, octal
    // Hex/binary/octal alternatives listed BEFORE decimal to avoid 0xFF matching as "0" + "xFF"
    [GeneratedRegex(@"0[Xx][0-9A-Fa-f_]+|0[Bb][0-1_]+|0[Oo][0-7_]+|[0-9][0-9_]*")]
    private static partial Regex IntRegex();

    // Float literals
    [GeneratedRegex(@"(([0-9][0-9_]*)?\.[0-9][0-9_]*|[0-9][0-9_]*\.)([eE][+-]?[0-9][0-9_]*)?")]
    private static partial Regex FloatRegex();

    // String start: optional prefix followed by quotes
    [GeneratedRegex(@"([rR][fFbB]?|[uU]|[fF][rR]?|[bB][rR]?)?('''|'|""""""|"")")]
    private static partial Regex StringStartRegex();

    /// <summary>
    /// Symbolic tokens ordered longest first to avoid partial mismatches.
    /// Must match pycdc's SYMBOLIC_TOKENS tuple order exactly.
    /// </summary>
    private static readonly string[] SymbolicTokens =
    [
        "<<=", ">>=", "**=", "//=", "...", ".",
        "+=", "-=", "*=", "@=", "/=", "%=", "&=", "|=", "^=",
        "<>", "<<", "<=", "<", ">>", ">=", ">", "!=", "==", "=",
        ",", ";", ":=", ":", "->", "~", "`",
        "+", "-", "**", "*", "@", "//", "/", "%", "&", "|", "^",
        "(", ")", "{", "}", "[", "]",
    ];

    /// <summary>
    /// Tokenize the given Python source code into a list of tokens.
    /// </summary>
    /// <param name="sourceCode">Python source code as a string.</param>
    /// <returns>List of tokens in order.</returns>
    /// <exception cref="InvalidOperationException">On parse errors.</exception>
    public List<PyToken> Tokenize(string sourceCode)
    {
        var tokens = new List<PyToken>();
        var lines = sourceCode.Split('\n');
        var indentStack = new List<int> { 0 };
        var contextStack = new List<string>();
        var nLine = 0;

        while (nLine < lines.Length)
        {
            var line = lines[nLine];
            nLine++;

            // Skip empty lines and comment-only lines
            if (string.IsNullOrWhiteSpace(line) || line.TrimStart().StartsWith('#'))
                continue;

            // Track indentation changes (only when not inside brackets)
            if (contextStack.Count == 0)
            {
                var indent = line.Length - line.TrimStart().Length;
                if (indent > indentStack[^1])
                {
                    indentStack.Add(indent);
                    tokens.Add(new StructuralEndlineToken(TokenType.INDENT, nLine));
                }
                while (indent < indentStack[^1])
                {
                    indentStack.RemoveAt(indentStack.Count - 1);
                    tokens.Add(new StructuralEndlineToken(TokenType.OUTDENT, nLine));
                }
                if (indent != indentStack[^1])
                    throw new InvalidOperationException($"Incorrect indentation on line {nLine}");
            }

            // Tokenize the current line
            var remaining = line;
            while (true)
            {
                remaining = remaining.TrimStart();
                if (string.IsNullOrEmpty(remaining))
                    break;
                if (remaining[0] == '#')
                    break; // Rest of line is a comment

                // Try symbolic tokens first (longest match)
                var symbolToken = MatchSymbolicToken(remaining, nLine);
                if (symbolToken != null)
                {
                    if (symbolToken.IsOpeningBracket)
                        contextStack.Add(symbolToken.Symbol);
                    else if (symbolToken.IsClosingBracket)
                    {
                        if (contextStack.Count == 0 || contextStack[^1] != symbolToken.MatchingOpeningBracket)
                            throw new InvalidOperationException(
                                $"Mismatched bracket '{symbolToken.Symbol}' at line {nLine}");
                        contextStack.RemoveAt(contextStack.Count - 1);
                    }
                    tokens.Add(symbolToken);
                    remaining = remaining[symbolToken.Symbol.Length..];
                    continue;
                }

                // Try float
                var floatMatch = FloatRegex().Match(remaining);
                if (floatMatch.Success && floatMatch.Index == 0)
                {
                    tokens.Add(new FloatToken(floatMatch.Value, nLine));
                    remaining = remaining[floatMatch.Length..];
                    continue;
                }

                // Try int
                var intMatch = IntRegex().Match(remaining);
                if (intMatch.Success && intMatch.Index == 0)
                {
                    tokens.Add(new IntToken(intMatch.Value, nLine));
                    remaining = remaining[intMatch.Length..];
                    continue;
                }

                // Try string
                var stringToken = MatchStringToken(remaining, lines, ref nLine, ref remaining);
                if (stringToken != null)
                {
                    tokens.Add(stringToken);
                    continue;
                }

                // Try word
                var wordMatch = WordRegex().Match(remaining);
                if (wordMatch.Success && wordMatch.Index == 0)
                {
                    tokens.Add(new WordToken(wordMatch.Value, nLine));
                    remaining = remaining[wordMatch.Length..];
                    continue;
                }

                throw new InvalidOperationException(
                    $"Unrecognized tokens: \"{remaining}\" at line {nLine}");
            }

            // Emit ENDLINE only when not inside brackets
            if (contextStack.Count == 0)
                tokens.Add(new StructuralEndlineToken(TokenType.ENDLINE, nLine));
        }

        // Emit any remaining OUTDENTs at end-of-file (matches pycdc behavior)
        while (indentStack.Count > 1)
        {
            indentStack.RemoveAt(indentStack.Count - 1);
            tokens.Add(new StructuralEndlineToken(TokenType.OUTDENT, nLine));
        }

        return tokens;
    }

    /// <summary>
    /// Format a list of tokens into the pycdc token_dump output format.
    /// ENDLINE/INDENT/OUTDENT each get their own line; other tokens are
    /// space-separated within a line.
    /// </summary>
    public string Dump(List<PyToken> tokens)
    {
        var sb = new StringBuilder();
        foreach (var token in tokens)
        {
            if (token.Type is TokenType.ENDLINE or TokenType.INDENT or TokenType.OUTDENT)
                sb.AppendLine(token.ToString());
            else
                sb.Append(token).Append(' ');
        }
        return sb.ToString();
    }

    /// <summary>
    /// Try to match a symbolic token at the start of the remaining text.
    /// Checks tokens in order (longest first) to avoid partial matches.
    /// </summary>
    private static SymbolToken? MatchSymbolicToken(string text, int lineNumber)
    {
        foreach (var sym in SymbolicTokens)
        {
            if (text.StartsWith(sym, StringComparison.Ordinal))
                return new SymbolToken(sym, lineNumber);
        }
        return null;
    }

    /// <summary>
    /// Try to match a string token at the start of the remaining text.
    /// Handles multi-line strings by reading additional lines from the source.
    /// </summary>
    private static StringToken? MatchStringToken(
        string remaining, string[] lines, ref int nLine, ref string lineRemaining)
    {
        var match = StringStartRegex().Match(remaining);
        if (!match.Success || match.Index != 0)
            return null;

        var prefix = match.Groups[1].Value;
        var quotes = match.Groups[2].Value;
        var start = prefix.Length + quotes.Length;
        var content = new StringBuilder();
        var currentLine = remaining;

        while (true)
        {
            var end = currentLine.IndexOf(quotes, start, StringComparison.Ordinal);
            if (end > 0 && currentLine[end - 1] == '\\')
            {
                content.Append(currentLine.AsSpan(start, end + 1 - start));
                start = end + 1;
                continue;
            }
            if (end >= 0)
            {
                content.Append(currentLine.AsSpan(start, end - start));
                // Remaining part after the closing quotes
                lineRemaining = currentLine[(end + quotes.Length)..];
                break;
            }

            // Need to read next line
            content.Append(currentLine.AsSpan(start));
            nLine++;
            if (nLine >= lines.Length)
                throw new InvalidOperationException(
                    $"Reached end of file while looking for closing {quotes}");
            currentLine = lines[nLine];
            start = 0;
        }

        return new StringToken(prefix, content.ToString(), nLine);
    }
}

/// <summary>
/// Internal token type for structural tokens (INDENT, OUTDENT, ENDLINE)
/// that don't carry value content.
/// </summary>
file sealed class StructuralEndlineToken : PyToken
{
    public StructuralEndlineToken(TokenType type, int lineNumber) : base(type, lineNumber)
    {
        if (type is not (TokenType.INDENT or TokenType.OUTDENT or TokenType.ENDLINE))
            throw new ArgumentException($"StructuralEndlineToken cannot be of type {type}", nameof(type));
    }

    public override string ToString() => Type switch
    {
        TokenType.INDENT => "<INDENT>",
        TokenType.OUTDENT => "<OUTDENT>",
        TokenType.ENDLINE => "<EOL>",
        _ => $"<{Type}>"
    };
}
