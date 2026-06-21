using System;
using System.IO;
using System.Linq;
using PyRebuilderSharp.Core;
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Scanners;
using PyRebuilderSharp.Core.Builders;
using PyRebuilderSharp.Core.Generators;

namespace PyRebuilderSharp.Cli;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length < 1)
        {
            ShowUsage();
            return;
        }

        var inputFiles = new List<string>();
        string? outputDir = null;
        bool batchMode = false;
        bool statsOnly = false;
        bool noHeader = false;
        bool noSummary = false;
        bool noOrphans = false;

        for (int i = 0; i < args.Length; i++)
        {
            if (args[i] is "-o" or "--output" && i + 1 < args.Length)
            {
                outputDir = args[++i];
                continue;
            }
            if (args[i] is "--stats")
            {
                statsOnly = true;
                continue;
            }
            if (args[i] is "-d" or "--dir" && i + 1 < args.Length)
            {
                batchMode = true;
                var dir = args[++i];
                if (Directory.Exists(dir))
                    inputFiles.AddRange(Directory.GetFiles(dir, "*.pyc", SearchOption.AllDirectories));
                else
                    Console.Error.WriteLine($"Warning: Directory not found: {dir}");
                continue;
            }
            // Options
            if (args[i] is "--no-header") { noHeader = true; continue; }
            if (args[i] is "--no-summary") { noSummary = true; continue; }
            if (args[i] is "--no-orphans") { noOrphans = true; continue; }
            // Treat as input file
            if (File.Exists(args[i]))
                inputFiles.Add(args[i]);
            else if (Directory.Exists(args[i]))
            {
                batchMode = true;
                inputFiles.AddRange(Directory.GetFiles(args[i], "*.pyc", SearchOption.AllDirectories));
            }
            else
                Console.Error.WriteLine($"Warning: Not found: {args[i]}");
        }

        if (inputFiles.Count == 0)
        {
            Console.Error.WriteLine("Error: No .pyc files found.");
            ShowUsage();
            return;
        }

        if (args.Contains("--diagnose"))
        {
            DiagnosePhase(inputFiles[0]);
            return;
        }

        var opts = new DecompileOptions
        {
            ShowHeader = !noHeader,
            ShowSummary = !noSummary,
            ShowOrphanBlocks = !noOrphans
        };
        if (inputFiles.Count > 1 || batchMode)
            RunBatch(inputFiles, outputDir, statsOnly, opts);
        else
            RunSingle(inputFiles[0], outputDir, opts);
    }

    static void ShowUsage()
    {
        Console.Error.WriteLine("Usage: pyrebuilder <input.pyc> [options]");
        Console.Error.WriteLine("       pyrebuilder -d <directory> [options]  (batch mode)");
        Console.Error.WriteLine("       pyrebuilder <directory> [options]      (batch mode)");
        Console.Error.WriteLine("Options:");
        Console.Error.WriteLine("  -o, --output <path>   Output file (single) or directory (batch)");
        Console.Error.WriteLine("  -d, --dir <dir>       Input directory (batch)");
        Console.Error.WriteLine("  --stats              Show batch statistics only");
        Console.Error.WriteLine("  --no-header          Suppress '# Decompiled from:' header");
        Console.Error.WriteLine("  --no-summary         Suppress '# [SUMMARY]' footer");
        Console.Error.WriteLine("  --no-orphans         Suppress orphan block output");
    }

    static void RunSingle(string inputFile, string? outputFile, DecompileOptions opts)
    {
        try
        {
            var pycData = File.ReadAllBytes(inputFile);
            var decompiler = new Decompiler(opts);
            var result = decompiler.DecompileWithStats(pycData);

            if (outputFile != null)
            {
                File.WriteAllText(outputFile, result.SourceCode);
                Console.WriteLine($"Decompiled: {inputFile} → {outputFile}");
            }
            else
            {
                Console.WriteLine(result.SourceCode);
            }
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Error: {inputFile}: {ex.GetType().Name}: {ex.Message}");
            if (ex.InnerException != null)
                Console.Error.WriteLine($"  Inner: {ex.InnerException.Message}");
        }
    }

    static void RunBatch(List<string> files, string? outputDir, bool statsOnly, DecompileOptions opts)
    {
        int success = 0, failed = 0;
        double totalMs = 0;
        var decompiler = new Decompiler(opts);

        foreach (var file in files)
        {
            try
            {
                var pycData = File.ReadAllBytes(file);
                var sw = System.Diagnostics.Stopwatch.StartNew();
                var result = decompiler.DecompileWithStats(pycData);
                sw.Stop();
                totalMs += sw.Elapsed.TotalMilliseconds;

                success++;
                if (!statsOnly)
                {
                    var relPath = Path.GetRelativePath(
                        Directory.GetCurrentDirectory(), file);
                    Console.Error.WriteLine($"✅ {relPath} ({sw.Elapsed.TotalMilliseconds:F0}ms)");

                    if (outputDir != null)
                    {
                        var outPath = Path.Combine(outputDir,
                            Path.ChangeExtension(relPath, ".py"));
                        Directory.CreateDirectory(Path.GetDirectoryName(outPath)!);
                        File.WriteAllText(outPath, result.SourceCode);
                    }
                }
            }
            catch (Exception ex)
            {
                failed++;
                Console.Error.WriteLine($"❌ {file}: {ex.GetType().Name}");
            }
        }

        Console.Error.WriteLine($"\nBatch complete: {success} succeeded, {failed} failed, " +
            $"{success + failed} total, {totalMs / Math.Max(1, success + failed):F1}ms avg");
    }

    /// <summary>分阶段诊断反编译挂死位置。</summary>
    static void DiagnosePhase(string inputFile)
    {
        try
        {
            var data = File.ReadAllBytes(inputFile);
            Console.Error.WriteLine($"=== 分阶段诊断: {inputFile} ({data.Length} bytes) ===");

            // Phase 1: Reader
            Console.Error.Write("[Phase 1/5] PycReader.Read()... ");
            Console.Error.Flush();
            var sw = System.Diagnostics.Stopwatch.StartNew();
            var reader = new PycReader();
            var codeObj = reader.Read(data);
            sw.Stop();
            Console.Error.WriteLine($"OK ({sw.Elapsed.TotalMilliseconds:F0}ms)  Instr={codeObj.Instructions?.Count} ChildCodes={codeObj.ChildCodes?.Count}");

            // Phase 2: BlockScanner
            Console.Error.Write("[Phase 2/5] BlockScanner.Scan()... ");
            sw.Restart();
            var blocks = new BlockScanner().Scan(codeObj);
            sw.Stop();
            Console.Error.WriteLine($"OK ({sw.Elapsed.TotalMilliseconds:F0}ms)  Blocks={blocks.Count}");

            // Phase 3: ControlFlowScanner
            Console.Error.Write("[Phase 3/5] ControlFlowScanner.Analyze()... ");
            sw.Restart();
            var cfg = new ControlFlowScanner().Analyze(blocks);
            sw.Stop();
            Console.Error.WriteLine($"OK ({sw.Elapsed.TotalMilliseconds:F0}ms)");

            // Phase 4: AstBuilder.Build()
            Console.Error.Write("[Phase 4/5] AstBuilder.Build()... ");
            sw.Restart();
            var builder = new AstBuilder(codeObj);
            var ast = builder.Build(cfg);
            sw.Stop();
            Console.Error.WriteLine($"OK ({sw.Elapsed.TotalMilliseconds:F0}ms)  TotalBlocks={builder.TotalBlockCount} Failed={builder.FailedBlockCount}");

            // Phase 5: Code generation
            Console.Error.Write("[Phase 5/5] PythonCodeGenerator.Generate()... ");
            sw.Restart();
            var source = new PythonCodeGenerator().Generate(ast);
            sw.Stop();
            Console.Error.WriteLine($"OK ({sw.Elapsed.TotalMilliseconds:F0}ms)  Output={source.Length} chars");

            Console.Error.WriteLine($"\n✅ 全部通过! 总耗时: {(sw.Elapsed.TotalMilliseconds):F0}ms");
            Console.WriteLine(source);
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"❌ 失败: {ex.GetType().Name}: {ex.Message}");
            if (ex.InnerException != null)
                Console.Error.WriteLine($"  Inner: {ex.InnerException.GetType().Name}: {ex.InnerException.Message}");
            Console.Error.WriteLine($"  Stack: {ex.StackTrace}");
        }
    }
}
