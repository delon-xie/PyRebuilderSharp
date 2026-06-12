using Xunit;
using FluentAssertions;
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Tests;

public class PycReaderTests
{
    private static readonly string TestDataDir = "TestData";

    [Fact]
    public void Read_SimpleConst38_ReturnsValidCodeObject()
    {
        var reader = new PycReader();
        var pycPath = Path.Combine(TestDataDir, "compiled", "simple_const.3.8.pyc");
        var data = File.ReadAllBytes(pycPath);
        var code = reader.Read(data);

        code.Should().NotBeNull();
        code.Name.Should().Be("<module>");
        code.Instructions.Count.Should().BeGreaterThan(0);
    }

    [Fact]
    public void Read_SimpleConst38_InstructionsHaveValidOpcodes()
    {
        var reader = new PycReader();
        var data = File.ReadAllBytes(
            Path.Combine(TestDataDir, "compiled", "simple_const.3.8.pyc"));
        var code = reader.Read(data);

        code.Instructions.Should().AllSatisfy(i =>
        {
            ((int)i.Opcode).Should().BeInRange(0, 255);
        });
    }

    [Fact]
    public void Read_SimpleConst38_HasConstants()
    {
        var reader = new PycReader();
        var data = File.ReadAllBytes(
            Path.Combine(TestDataDir, "compiled", "simple_const.3.8.pyc"));
        var code = reader.Read(data);

        code.Constants.Should().NotBeEmpty();
    }

    [Fact]
    public void Read_TestFunctionsPy3_HasFunctions()
    {
        var reader = new PycReader();
        var data = File.ReadAllBytes(
            Path.Combine(TestDataDir, "compiled", "test_functions_py3.38.pyc"));
        var code = reader.Read(data);

        code.Should().NotBeNull();
        code.Instructions.Count.Should().BeGreaterThan(1);
    }
}
