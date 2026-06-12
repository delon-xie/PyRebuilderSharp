namespace PyRebuilderSharp.Core.Testing;

/// <summary>
/// Token types matching pycdc's token_dump categories.
/// INDENT/OUTDENT/ENDLINE are special structural tokens.
/// WORD/INT/FLOAT/STRING/SYMBOL are content tokens with value comparison.
/// </summary>
public enum TokenType
{
    INDENT,
    OUTDENT,
    ENDLINE,
    WORD,
    INT,
    FLOAT,
    STRING,
    SYMBOL
}
