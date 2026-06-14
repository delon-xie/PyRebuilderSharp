using System;
using System.IO;
using System.Linq;
using PyRebuilderSharp.Core;

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

        if (inputFiles.Count > 1 || batchMode)
            RunBatch(inputFiles, outputDir, statsOnly);
        else
            RunSingle(inputFiles[0], outputDir);
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
    }

    static void RunSingle(string inputFile, string? outputFile)
    {
        try
        {
            var pycData = File.ReadAllBytes(inputFile);
            var decompiler = new Decompiler();
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

    static void RunBatch(List<string> files, string? outputDir, bool statsOnly)
    {
        int success = 0, failed = 0;
        double totalMs = 0;
        var decompiler = new Decompiler();

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
}
