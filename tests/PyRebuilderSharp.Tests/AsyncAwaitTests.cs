using Xunit;
using Xunit.Abstractions;
using FluentAssertions;
using PyRebuilderSharp.Core.Builders;
using PyRebuilderSharp.Core.Models.AST;
using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Scanners;
using PyRebuilderSharp.Core.Generators;
using PyRebuilderSharp.Core.Versioning;

namespace PyRebuilderSharp.Tests;

public class AsyncAwaitTests
{
    private readonly ITestOutputHelper _output;

    public AsyncAwaitTests(ITestOutputHelper output)
    {
        _output = output;
    }

    [Fact]
    public void Python311_AsyncAwait_Simple()
    {
        var pycPath = "/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/test_async.3.11.pyc";
        var result = DecompileAndCheck(pycPath);
        
        _output.WriteLine($"Decompiled:\n{result.DecompiledSource}");
        
        result.DecompiledSource.Should().Contain("await asyncio.sleep(1)");
        result.DecompiledSource.Should().Contain("await test_async()");
        result.DecompiledSource.Should().NotContain("asyncio.sleep(1)()");
        result.DecompiledSource.Should().NotContain("test_async()()");
    }

    

    [Fact]
    public void Python311_Send_InCoroutine()
    {
        var code = new CodeObject
        {
            IsCoroutine = true,
            Version = PythonVersion.Py311,
            Constants = new() { [0] = null, [1] = 1 },
            Names = new() { "asyncio", "sleep" }
        };

        var sm = new StackMachine(code);
        
        sm.Execute(new Instruction(0, Opcode.LOAD_GLOBAL, 0));
        sm.Execute(new Instruction(2, Opcode.LOAD_ATTR, 1));
        sm.Execute(new Instruction(4, Opcode.LOAD_CONST, 1));
        sm.Execute(new Instruction(6, Opcode.PRECALL_311, 1));
        sm.Execute(new Instruction(8, Opcode.CALL_311, 1));
        sm.Execute(new Instruction(10, Opcode.CALL_FUNCTION, 0));
        sm.Execute(new Instruction(12, Opcode.LOAD_CONST, 0));
        sm.Execute(new Instruction(14, Opcode.SEND, 0));
        
        sm.ExprStackCount.Should().Be(1);
        var result = sm.PopExpr();
        result.Should().BeOfType<Await>();
        
        var awaitExpr = (Await)result;
        awaitExpr.Value.Should().BeOfType<Call>();
        var call = (Call)awaitExpr.Value;
        call.Args.Count.Should().Be(1);
    }

    [Fact]
    public void Python311_YieldValue_InCoroutine()
    {
        var code = new CodeObject
        {
            IsCoroutine = true,
            Version = PythonVersion.Py311,
            Constants = new() { [0] = null, [1] = 1 },
            Names = new() { "asyncio", "sleep" }
        };

        var sm = new StackMachine(code);
        
        sm.Execute(new Instruction(0, Opcode.LOAD_GLOBAL, 0));
        sm.Execute(new Instruction(2, Opcode.LOAD_ATTR, 1));
        sm.Execute(new Instruction(4, Opcode.LOAD_CONST, 1));
        sm.Execute(new Instruction(6, Opcode.PRECALL_311, 1));
        sm.Execute(new Instruction(8, Opcode.CALL_311, 1));
        sm.Execute(new Instruction(10, Opcode.CALL_FUNCTION, 0));
        sm.Execute(new Instruction(12, Opcode.LOAD_CONST, 0));
        sm.Execute(new Instruction(14, Opcode.SEND, 0));
        sm.Execute(new Instruction(16, Opcode.YIELD_VALUE, null));
        
        sm.ExprStackCount.Should().Be(1);
        var result = sm.PopExpr();
        result.Should().BeOfType<Await>();
    }

    [Fact]
    public void Python312_AsyncAwait_GetAwaitable()
    {
        var pycPath = "/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/test_async.3.12.pyc";
        var result = DecompileAndCheck(pycPath);
        
        _output.WriteLine($"Decompiled 3.12:\n{result.DecompiledSource}");
        
        result.DecompiledSource.Should().Contain("await asyncio.sleep(1)");
        result.DecompiledSource.Should().Contain("await test_async()");
    }

    [Fact]
    public void Python313_AsyncAwait()
    {
        var pycPath = "/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/test_async.3.13.pyc";
        var result = DecompileAndCheck(pycPath);
        
        _output.WriteLine($"Decompiled 3.13:\n{result.DecompiledSource}");
        
        result.DecompiledSource.Should().Contain("await asyncio.sleep(1)");
        result.DecompiledSource.Should().Contain("await test_async()");
    }

    [Fact]
    public void Python314_AsyncAwait()
    {
        var pycPath = "/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/test_async.3.14.pyc";
        var result = DecompileAndCheck(pycPath);
        
        _output.WriteLine($"Decompiled 3.14:\n{result.DecompiledSource}");
        
        result.DecompiledSource.Should().Contain("await asyncio.sleep(1)");
        result.DecompiledSource.Should().Contain("await test_async()");
    }

    [Fact]
    public void Python310_AsyncAwait()
    {
        var pycPath = "/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/test_async.3.10.pyc";
        var result = DecompileAndCheck(pycPath);
        
        _output.WriteLine($"Decompiled 3.10:\n{result.DecompiledSource}");
        
        result.DecompiledSource.Should().Contain("await asyncio.sleep(1)");
        result.DecompiledSource.Should().Contain("await test_async()");
    }

    private (string DecompiledSource, bool Success) DecompileAndCheck(string pycPath)
    {
        if (!File.Exists(pycPath))
        {
            _output.WriteLine($"File not found: {pycPath}");
            return ("", false);
        }

        var data = File.ReadAllBytes(pycPath);
        var reader = new PycReader();
        var code = reader.Read(data);
        
        var scanner = new BlockScanner();
        var blocks = scanner.Scan(code);
        
        var cfScanner = new ControlFlowScanner();
        var cfg = cfScanner.Analyze(blocks);
        
        var builder = new AstBuilder(code);
        var ast = builder.Build(cfg);
        
        var gen = new PythonCodeGenerator();
        var src = gen.Generate(ast);
        
        return (src, true);
    }
}