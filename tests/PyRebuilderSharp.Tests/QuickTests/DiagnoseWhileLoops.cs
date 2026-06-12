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

public class DiagnoseWhileLoops
{
    private readonly ITestOutputHelper _output;

    public DiagnoseWhileLoops(ITestOutputHelper output)
    {
        _output = output;
    }

    [Fact]
    public void Dump_WhileLoops2_Diagnostics()
    {
        var testDataDir = "/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled";
        var data = File.ReadAllBytes(Path.Combine(testDataDir, "while_loops2.3.10.pyc"));

        var reader = new PycReader();
        var code = reader.Read(data);
        var log = new List<string>
        {
            $"=== Code: {code.Name} ({code.ArgCount} args, {code.Instructions.Count} instrs) ==="
        };
        
        log.Add("=== Instruction Dump (first 200) ===");
        foreach (var instr in code.Instructions.Take(200))
            log.Add($"  {instr.Offset:X4}: op={instr.Opcode} ({(byte)instr.Opcode}) arg={instr.Argument}");
        
        // Dump raw bytecodes for verification
        var rawBc = new List<string>();
        var bc = code.Instructions;
        for (int i = 0; i < Math.Min(200, bc.Count); i++)
        {
            var instr = bc[i];
            rawBc.Add($"{instr.Offset:X4}: {instr.Opcode} ({(byte)instr.Opcode}) arg={instr.Argument}");
        }
        File.WriteAllLines("/tmp/raw_instrs.txt", rawBc);
        log.Add("Wrote raw instructions to /tmp/raw_instrs.txt");
        
        var scanner = new BlockScanner();
        var blocks = scanner.Scan(code);
        log.Add($"\n=== Basic Blocks ({blocks.Count}) ===");
        foreach (var b in blocks.OrderBy(b => b.StartOffset))
        {
            log.Add($"  BLOCK {b.StartOffset:X4}-{b.EndOffset:X4} fl={b.Flags}" +
                $" succ=[{string.Join(",", b.Successors.Select(s => $"#{s.StartOffset:X4}"))}]" +
                $" pred=[{string.Join(",", b.Predecessors.Select(s => $"#{s.StartOffset:X4}"))}]" +
                $"  insts: {b.Instructions.Count}");
        }

        // Step 2: CFG with loop detection
        var cfScanner = new ControlFlowScanner();
        var cfg = cfScanner.Analyze(blocks);
        var rawCFG = cfg.RawCFG;
        log.Add("\n=== CFG Loop Detection ===");
        
        log.Add("Block Flags:");
        foreach (var b in rawCFG.Blocks.OrderBy(b => b.StartOffset))
            log.Add($"  {b.StartOffset:X4}: {b.Flags}");

        // Step 3: Block decompilation
        var blockDecompiler = new BlockDecompiler();
        var blockResults = blockDecompiler.DecompileBlocks(rawCFG.Blocks, code);
        log.Add($"\n=== Block Results ({blockResults.Count}) ===");
        foreach (var kv in blockResults.OrderBy(k => k.Key))
        {
            var br = kv.Value;
            log.Add($"  Block {kv.Key}: Success={br.IsSuccess}, Stmts={br.Statements?.Count ?? 0}, Comment='{br.CommentFallback?.Length > 0}'");
        }

        // Step 4: Build AST and generate source
        var builder = new AstBuilder(code);
        var ast = builder.Build(cfg);
        var gen = new PythonCodeGenerator();
        var src = gen.Generate(ast);
        
        // Write output to file for debugging
        log.Add($"\n=== DECOMPILED SOURCE ({src.Split('\n').Length} lines) ===");
        foreach (var line in src.Split('\n'))
            log.Add($"  |{line}");
        log.Add("=== END ===");

        // Tokenize
        var dumper = new TokenDumper();
        var actualTokens = dumper.Tokenize(src);
        log.Add($"\n=== Token Count: {actualTokens.Count} ===");
        foreach (var t in actualTokens.Take(30))
            log.Add($"  TOKEN: {t}");
        if (actualTokens.Count > 30)
            log.Add($"  ... ({actualTokens.Count - 30} more)");

        File.WriteAllLines("/tmp/while_loops2_diag.txt", log);
        
        // Compare with reference
        var runner = new PycdcSuiteRunner();
        var result = runner.RunSingle("while_loops2", "3.10");
        log.Add($"\n=== Compare: {result.Passed} | {result.ActualTokens}/{result.ExpectedTokens} ===");
        if (!result.Passed && result.ErrorMessage != null)
        {
            var lines = result.ErrorMessage.Split('\n');
            foreach (var line in lines.Take(40))
                log.Add($"  DIFF> {line}");
        }
        
        File.WriteAllLines("/tmp/while_loops2_diag.txt", log);
        _output.WriteLine("Diagnostics written to /tmp/while_loops2_diag.txt");
    }
}
