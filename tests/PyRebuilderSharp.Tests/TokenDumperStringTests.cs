using Xunit;
using FluentAssertions;
using PyRebuilderSharp.Core.Testing;

namespace PyRebuilderSharp.Tests;

public class TokenDumperStringTests
{
    [Fact]
    public void Tokenize_StringWithEscapedQuote_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = 'hello\\'world'\n";
        var tokens = dumper.Tokenize(source);
        var stringToken = tokens.FirstOrDefault(t => t is StringToken);
        stringToken.Should().NotBeNull();
        ((StringToken)stringToken!).Content.Should().Be("hello\\'world");
    }

    [Fact]
    public void Tokenize_StringWithDoubleEscapedBackslash_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = 'hello\\\\world'\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_TripleQuoteWithEscapedQuote_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = \"\"\"hello \\\"world\\\"\"\"\"\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_TripleQuoteWithUnescapedQuoteInside_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = \"\"\"hello \"world\"\"\"\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_FStringWithNestedBraces_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = f'{a}{{nested}}'\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_FStringTripleQuotesWithBraces_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = f\"\"\"{a} {{{{b}}}}\"\"\"\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_RawStringWithBackslash_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = r'hello\\world'\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_RawTripleQuoteWithBackslash_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = r\"\"\"hello\\world\"\"\"\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_StringWithNewlineEscape_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = 'hello\\nworld'\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_StringWithTabEscape_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = 'hello\\tworld'\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_StringWithOctalEscape_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = 'hello\\101world'\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_StringWithHexEscape_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = 'hello\\x41world'\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_StringWithUnicodeEscape_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = 'hello\\u0041world'\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_StringWithUnicodeEscapeSequence_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = 'hello\\U00000041world'\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_StringWithMultipleEscapes_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = '\\'\\\"\\n\\t'\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_MultilineStringWithComments_ClosesCorrectly()
    {
        var dumper = new TokenDumper();
        var source = "x = \"\"\") # comment\nline2\"\"\"\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken).Should().BeTrue();
    }
}
