using Xunit;
using FluentAssertions;
using PyRebuilderSharp.Core.Builders;
using PyRebuilderSharp.Core.Models.AST;
using PyRebuilderSharp.Core.Models.Bytecode;

namespace PyRebuilderSharp.Tests;

public class StackMachineTests
{
    [Fact]
    public void Execute_LoadConst_ReturnsNull()
    {
        var code = new CodeObject
        {
            Constants = new() { [0] = 42 }
        };
        var sm = new StackMachine(code);
        var result = sm.Execute(new Instruction(0, Opcode.LOAD_CONST, 0));
        result.Should().BeNull();
    }

    [Fact]
    public void Execute_LoadConstStoreName_ReturnsAssign()
    {
        var code = new CodeObject
        {
            Constants = new() { [0] = 42 },
            Names = new() { "a" }
        };
        var sm = new StackMachine(code);
        sm.Execute(new Instruction(0, Opcode.LOAD_CONST, 0));
        var result = sm.Execute(new Instruction(2, Opcode.STORE_NAME, 0));

        result.Should().BeOfType<Assign>();
        var assign = (Assign)result!;
        assign.Targets[0].Should().BeOfType<Name>().Which.Id.Should().Be("a");
    }

    [Fact]
    public void Execute_BinaryAdd_ReturnsBinOpOnPop()
    {
        var code = new CodeObject
        {
            Constants = new() { [0] = 1, [1] = 2 }
        };
        var sm = new StackMachine(code);
        sm.Execute(new Instruction(0, Opcode.LOAD_CONST, 0));
        sm.Execute(new Instruction(2, Opcode.LOAD_CONST, 1));
        sm.Execute(new Instruction(4, Opcode.BINARY_ADD));

        // BINARY_ADD pushes BinOp onto expression stack (not results list)
        sm.ExprStackCount.Should().Be(1);
        var binOp = sm.PopExpr();
        binOp.Should().BeOfType<BinOp>();
        ((BinOp)binOp).Op.Should().Be(Operator.Add);
    }

    [Fact]
    public void Execute_ReturnValue_PopsAndReturns()
    {
        var code = new CodeObject
        {
            Constants = new() { [0] = 42 }
        };
        var sm = new StackMachine(code);
        sm.Execute(new Instruction(0, Opcode.LOAD_CONST, 0));
        var result = sm.Execute(new Instruction(2, Opcode.RETURN_VALUE));

        result.Should().BeOfType<Return>();
        ((Return)result!).Value.Should().BeOfType<Constant>();
    }

    [Fact]
    public void Execute_UnknownOpcode_SilentlyIgnored()
    {
        var code = new CodeObject();
        var sm = new StackMachine(code);
        var result = sm.Execute(new Instruction(0, (Opcode)255));
        // Unknown opcodes are silently ignored (block-level fault tolerance)
        result.Should().BeNull();
    }
}
