using PyRebuilderSharp.Core;
using System.Diagnostics;

// Capture stderr
var oldError = Console.Error;
var errorWriter = new StringWriter();
Console.SetError(errorWriter);

try
{
    var file = "/Users/admin/codes/Tools/PyRebuilderSharp/test_data/compiled/abc.3.12.pyc";
    var data = File.ReadAllBytes(file);
    var decompiler = new Decompiler();
    var sw = Stopwatch.StartNew();
    var result = decompiler.DecompileWithStats(data);
    sw.Stop();
    
    Console.WriteLine($"Blocks: {result.TotalBlocks}, Failed: {result.FailedBlocks}, {sw.ElapsedMilliseconds}ms");
    Console.WriteLine($"Code ({result.SourceCode.Length} chars)");
}
catch (Exception ex)
{
    Console.WriteLine($"Error: {ex.Message}");
}
finally
{
    Console.SetError(oldError);
}

// Print only TRACE and WARNING lines
var trace = errorWriter.ToString();
var lines = trace.Split('\n', StringSplitOptions.RemoveEmptyEntries);
foreach (var line in lines)
{
    if (line.StartsWith("TRACE") || line.StartsWith("WARNING"))
        Console.Error.WriteLine(line);
}
