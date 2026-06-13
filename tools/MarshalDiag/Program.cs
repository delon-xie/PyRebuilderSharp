// Quick per-file warning scanner
using PyRebuilderSharp.Core;
using System.Diagnostics;

var root = args.Length > 0 ? args[0] : "/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled";
var files = Directory.GetFiles(root, "*.pyc");

int warnFiles = 0, warnCount = 0;
foreach (var file in files.OrderBy(f => Path.GetFileName(f)))
{
    var data = File.ReadAllBytes(file);
    
    // Capture stderr for this file
    var oldError = Console.Error;
    var capture = new StringWriter();
    Console.SetError(capture);
    
    try
    {
        var decompiler = new Decompiler();
        var result = decompiler.DecompileWithStats(data);
    }
    finally
    {
        Console.SetError(oldError);
    }
    
    var warns = capture.ToString();
    if (warns.Contains("WARNING:"))
    {
        warnFiles++;
        var count = warns.Split('\n').Count(l => l.Contains("WARNING:"));
        warnCount += count;
        Console.WriteLine($"{Path.GetFileName(file),-50} {count} warnings - {warns.Split('\n').First(l => l.Contains("WARNING:"))}");
    }
}

Console.WriteLine($"\n{warnFiles} files with warnings, {warnCount} total warnings (out of {files.Length} files)");
