using Xunit;
using FluentAssertions;
using PyRebuilderSharp.Core.Testing;

namespace PyRebuilderSharp.Tests;

public class TokenDiffResultTests
{
    [Fact]
    public void Compare_IdenticalTokenLists_ReturnsMatch()
    {
        var dumper = new TokenDumper();
        var source = "a = 42\n";
        var tokens1 = dumper.Tokenize(source);
        var tokens2 = dumper.Tokenize(source);
        var result = TokenDiffer.Compare(tokens1, tokens2);
        result.Match.Should().BeTrue();
    }

    [Fact]
    public void Compare_DifferentTokenLists_ReturnsNoMatch()
    {
        var dumper = new TokenDumper();
        var t1 = dumper.Tokenize("a = 42\n");
        var t2 = dumper.Tokenize("b = 99\n");
        var result = TokenDiffer.Compare(t1, t2);
        result.Match.Should().BeFalse();
    }
}
