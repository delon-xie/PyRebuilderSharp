using Xunit;
using Xunit.Abstractions;
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Scanners;
using PyRebuilderSharp.Core.Builders;
using PyRebuilderSharp.Core.Generators;
using PyRebuilderSharp.Core.Testing;
using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.CFG;

namespace PyRebuilderSharp.Tests;

public class DiagnoseExpressions
{
    private readonly ITestOutputHelper _output;

    public DiagnoseExpressions(ITestOutputHelper output)
    {
        _output = output;
    }

    [Fact]
    public void Dump_Expressions_Diag()
    {
        var testDir = "/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled";
        var data = File.ReadAllBytes(Path.Combine(testDir, "test_expressions_comprehensive.3.10.pyc"));

        var reader = new PycReader();
        var code = reader.Read(data);
        
        // Dump instructions
        var log = new List<string>();
        log.Add($"Instructions: {code.Instructions.Count}");
        foreach (var instr in code.Instructions)
            if (instr.Opcode == Opcode.POP_JUMP_IF_FALSE || instr.Opcode == Opcode.POP_JUMP_IF_TRUE
                || instr.Opcode == Opcode.JUMP_ABSOLUTE || instr.Opcode == Opcode.JUMP_FORWARD
                || instr.Opcode == Opcode.JUMP_BACKWARD || instr.Opcode == Opcode.FOR_ITER
                || instr.Opcode == Opcode.SETUP_FINALLY || instr.Offset == 0xD2 || instr.Offset == 0x156)
                log.Add($"  {instr.Offset:X4}: op={instr.Opcode} arg={instr.Argument}");

        // Blocks
        var scanner = new BlockScanner();
        var blocks = scanner.Scan(code);
        log.Add($"\nBlocks: {blocks.Count}");
        foreach (var b in blocks.OrderBy(b => b.StartOffset))
            log.Add($"  BLOCK {b.StartOffset:X4}-{b.EndOffset:X4} insts={b.Instructions.Count} succ=[{string.Join(",", b.Successors.Select(s => $"#{s.StartOffset:X4}"))}]");

        // CFG
        var cfScanner = new ControlFlowScanner();
        var cfg = cfScanner.Analyze(blocks);
        log.Add($"\nBlock Flags:");
        foreach (var b in cfg.RawCFG.Blocks.OrderBy(b => b.StartOffset))
            log.Add($"  {b.StartOffset:X4}: {b.Flags}");

        // Block decompilation
        var blockDecompiler = new BlockDecompiler();
        var blockResults = blockDecompiler.DecompileBlocks(cfg.RawCFG.Blocks, code);
        log.Add($"\nBlock Results:");
        foreach (var kv in blockResults.OrderBy(k => k.Key))
        {
            var br = kv.Value;
            log.Add($"  Block {kv.Key}: Success={br.IsSuccess}, Stmts={br.Statements?.Count ?? 0}");
            foreach (var s in br.Statements ?? new())
                log.Add($"    STMT: {s.GetType().Name}: {s}");
        }

        // Final output
        var builder = new AstBuilder(code);
        var ast = builder.Build(cfg);
        var gen = new PythonCodeGenerator();
        var src = gen.Generate(ast);
        
        log.Add($"\n=== DECOMPILED SOURCE ===");
        foreach (var line in src.Split('\n'))
            log.Add($"  |{line}");
        log.Add("=== END ===");

        File.WriteAllLines("/tmp/expressions_diag.txt", log);
        _output.WriteLine("Wrote to /tmp/expressions_diag.txt");
    }
}
