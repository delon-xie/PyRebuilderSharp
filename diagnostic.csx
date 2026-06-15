// diagnostic.cs - run with: dotnet script diagnostic.cs
#r "../src/PyRebuilderSharp.Core/bin/Debug/net10.0/PyRebuilderSharp.Core.dll"
using PyRebuilderSharp.Core;
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Scanners;
using PyRebuilderSharp.Core.Builders;
using PyRebuilderSharp.Core.Generators;

var path = args.Length > 0 ? args[0] : "test_data/compiled/abc.3.11.pyc";
Console.Error.WriteLine($"=== Diagnosing: {path} ===");

var data = File.ReadAllBytes(path);
Console.Error.WriteLine($"File size: {data.Length} bytes");

// Phase 1: Reader
Console.Error.Write("Phase 1: PycReader.Read()... ");
var sw = System.Diagnostics.Stopwatch.StartNew();
var reader = new PycReader();
CodeObject? codeObj = null;
try { codeObj = reader.Read(data); sw.Stop(); Console.Error.WriteLine($"OK ({sw.Elapsed.TotalMilliseconds:F0}ms)"); }
catch (Exception ex) { sw.Stop(); Console.Error.WriteLine($"FAIL: {ex.GetType().Name}: {ex.Message}"); return; }

Console.Error.WriteLine($"  Instructions: {codeObj.Instructions?.Count}, ChildCodes: {codeObj.ChildCodes?.Count}");

// Phase 2: BlockScanner
Console.Error.Write("Phase 2: BlockScanner.Scan()... ");
sw.Restart();
List<BasicBlock> blocks;
try { blocks = new BlockScanner().Scan(codeObj); sw.Stop(); Console.Error.WriteLine($"OK ({sw.Elapsed.TotalMilliseconds:F0}ms)"); }
catch (Exception ex) { sw.Stop(); Console.Error.WriteLine($"FAIL: {ex.GetType().Name}: {ex.Message}"); return; }
Console.Error.WriteLine($"  Blocks: {blocks.Count}");

// Phase 3: ControlFlowScanner
Console.Error.Write("Phase 3: ControlFlowScanner.Analyze()... ");
sw.Restart();
StructuredCFG? cfg = null;
try { cfg = new ControlFlowScanner().Analyze(blocks); sw.Stop(); Console.Error.WriteLine($"OK ({sw.Elapsed.TotalMilliseconds:F0}ms)"); }
catch (Exception ex) { sw.Stop(); Console.Error.WriteLine($"FAIL: {ex.GetType().Name}: {ex.Message}"); return; }

// Phase 4: AstBuilder.Build()
Console.Error.Write("Phase 4: AstBuilder.Build()... ");
sw.Restart();
AstNode? ast = null;
try { 
    var builder = new AstBuilder(codeObj); 
    ast = builder.Build(cfg); 
    sw.Stop(); 
    Console.Error.WriteLine($"OK ({sw.Elapsed.TotalMilliseconds:F0}ms)"); 
    Console.Error.WriteLine($"  TotalBlocks={builder.TotalBlockCount}, Failed={builder.FailedBlockCount}");
}
catch (Exception ex) { sw.Stop(); Console.Error.WriteLine($"FAIL: {ex.GetType().Name}: {ex.Message}"); return; }

// Phase 5: Code generation
Console.Error.Write("Phase 5: PythonCodeGenerator.Generate()... ");
sw.Restart();
string source;
try { 
    source = new PythonCodeGenerator().Generate(ast); 
    sw.Stop(); 
    Console.Error.WriteLine($"OK ({sw.Elapsed.TotalMilliseconds:F0}ms)"); 
}
catch (Exception ex) { sw.Stop(); Console.Error.WriteLine($"FAIL: {ex.GetType().Name}: {ex.Message}"); return; }

Console.Error.WriteLine($"\nOutput: {source.Length} chars");
Console.WriteLine(source);
