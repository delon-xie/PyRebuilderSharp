using Xunit;
using FluentAssertions;
using PyRebuilderSharp.Core.Testing;

namespace PyRebuilderSharp.Tests;

public class TokenDumperTests
{
    [Fact]
    public void Tokenize_SimpleAssign_TokensAreCorrect()
    {
        var dumper = new TokenDumper();
        var source = "a = 42\n";
        var tokens = dumper.Tokenize(source);
        tokens.Should().HaveCount(5); // WORD(a) SYMBOL(=) INT(42) ENDLINE
        tokens[0].Should().BeOfType<WordToken>().Which.Word.Should().Be("a");
        tokens[1].Should().BeOfType<SymbolToken>().Which.Symbol.Should().Be("=");
        tokens[2].Should().BeOfType<IntToken>().Which.Value.Should().Be(42);
        tokens[4].Type.Should().Be(TokenType.ENDLINE);
    }

    [Fact]
    public void Tokenize_IfWithIndent_EmitsIndentOutdent()
    {
        var dumper = new TokenDumper();
        var source = "if True:\n    pass\n";
        var tokens = dumper.Tokenize(source);
        tokens.Should().Contain(t => t.Type == TokenType.INDENT);
        tokens.Should().Contain(t => t.Type == TokenType.OUTDENT);
    }

    [Fact]
    public void Tokenize_BracketContext_NoEndlineInsideBrackets()
    {
        var dumper = new TokenDumper();
        var source = "x = (1,\n 2)\n";
        var tokens = dumper.Tokenize(source);
        var endlines = tokens.Where(t => t.Type == TokenType.ENDLINE).ToList();
        endlines.Should().HaveCount(1);
    }

    [Fact]
    public void Tokenize_HexInt_NormalizesToDecimal()
    {
        var dumper = new TokenDumper();
        var source = "x = 0xFF\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is IntToken it && it.Value == 255).Should().BeTrue();
    }

    [Fact]
    public void Tokenize_String_NormalizesPrefix()
    {
        var dumper = new TokenDumper();
        var source = "x = rb'hello'\n";
        var tokens = dumper.Tokenize(source);
        tokens.Any(t => t is StringToken st && st.Prefix == "br").Should().BeTrue();
    }

    [Fact]
    public void Dump_SimpleAssign_FormatMatchesPycdc()
    {
        var dumper = new TokenDumper();
        var source = "a = 42\nb = 3.14159\nc = 'test'\n";
        var tokens = dumper.Tokenize(source);
        var dump = dumper.Dump(tokens);
        dump.Should().Contain("a = 42 <EOL>");
        dump.Should().Contain("b = 3.14159 <EOL>");
        dump.Should().Contain("c = 'test' <EOL>");
    }

    [Fact]
    public void Dump_IfBlock_ShowsIndentOutdent()
    {
        var dumper = new TokenDumper();
        var source = "if True:\n    pass\n";
        var tokens = dumper.Tokenize(source);
        var dump = dumper.Dump(tokens);
        dump.Should().Contain("<INDENT>");
        dump.Should().Contain("<OUTDENT>");
        dump.Should().Contain("<EOL>");
    }
}
