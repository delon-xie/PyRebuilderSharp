namespace PyRebuilderSharp.Core.Testing;

/// <summary>
/// Result of comparing two token sequences (expected vs actual).
/// Provides detailed diff output for debugging mismatches.
/// </summary>
public class TokenDiffResult
{
    /// <summary>True if the token sequences are semantically equivalent.</summary>
    public bool Match { get; init; }

    /// <summary>Human-readable diff lines showing where tokens differ.</summary>
    public List<string> DiffLines { get; init; } = new();

    /// <summary>Number of tokens in the expected sequence.</summary>
    public int ExpectedTokenCount { get; init; }

    /// <summary>Number of tokens in the actual sequence.</summary>
    public int ActualTokenCount { get; init; }
}

/// <summary>
/// Compares two lists of PyToken for semantic equivalence,
/// matching pycdc token_dump's comparison behavior.
/// </summary>
public static class TokenDiffer
{
    /// <summary>
    /// Compare expected and actual token sequences.
    /// Uses each token's semantic Equals() for comparison.
    /// </summary>
    public static TokenDiffResult Compare(List<PyToken> expected, List<PyToken> actual)
    {
        var diffLines = new List<string>();
        var match = true;
        var maxLen = Math.Max(expected.Count, actual.Count);
        var minLen = Math.Min(expected.Count, actual.Count);

        // Compare tokens one by one
        for (var i = 0; i < minLen; i++)
        {
            var exp = expected[i];
            var act = actual[i];

            if (!exp.Equals(act))
            {
                match = false;
                diffLines.Add($"Line {Math.Min(exp.LineNumber, act.LineNumber)}: " +
                              $"expected [{exp}] ({exp.Type}), got [{act}] ({act.Type})");
            }
        }

        // Handle extra tokens in expected
        if (expected.Count > actual.Count)
        {
            match = false;
            for (var i = minLen; i < expected.Count; i++)
                diffLines.Add($"Line {expected[i].LineNumber}: " +
                              $"expected [{expected[i]}] ({expected[i].Type}), got [<missing>]");
        }

        // Handle extra tokens in actual
        if (actual.Count > expected.Count)
        {
            match = false;
            for (var i = minLen; i < actual.Count; i++)
                diffLines.Add($"Line {actual[i].LineNumber}: " +
                              $"expected [<missing>], got [{actual[i]}] ({actual[i].Type})");
        }

        return new TokenDiffResult
        {
            Match = match,
            DiffLines = diffLines,
            ExpectedTokenCount = expected.Count,
            ActualTokenCount = actual.Count
        };
    }
}
