using Xunit;
using Xunit.Abstractions;
using PyRebuilderSharp.Core.Testing;

namespace PyRebuilderSharp.Tests;

public class QuickPopJumpTest
{
    private readonly ITestOutputHelper _output;
    private readonly PycdcSuiteRunner _runner = new();

    public QuickPopJumpTest(ITestOutputHelper output) => _output = output;

    [Fact]
    public void Verify_PopJump_Result()
    {
        var result = _runner.RunSingle("test_pop_jump_forward_if_false", "38");
        _output.WriteLine($"Passed: {result.Passed} | {result.ActualTokens}/{result.ExpectedTokens}");
        _output.WriteLine($"Error: {result.ErrorMessage ?? "(none)"}");
        
        var result2 = _runner.RunSingle("simple_const", "38");
        _output.WriteLine($"simple_const: Passed={result2.Passed} | {result2.ActualTokens}/{result2.ExpectedTokens}");
    }
}
