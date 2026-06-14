using System;
using System.IO;
using PyRebuilderSharp.Core;
using PyRebuilderSharp.Core.Generators;

var files = new[] {
    "/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_class_simple.3.12.pyc",
};

foreach (var file in files)
{
    Console.WriteLine($"\n=== {Path.GetFileName(file)} ===");
    if (!File.Exists(file)) { Console.WriteLine("  NOT FOUND"); continue; }
    try
    {
        var data = File.ReadAllBytes(file);
        var dc = new Decompiler();
        var result = dc.DecompileWithStats(data);
        var code = result.SourceCode;
        Console.WriteLine($"SourceCode ({code.Length} chars):");
        var lines = code.Split('\n');
        for (int i = 0; i < Math.Min(lines.Length, 30); i++)
            Console.WriteLine($"  {lines[i]}");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"ERROR: {ex.GetType().Name}: {ex.Message}");
    }
}
