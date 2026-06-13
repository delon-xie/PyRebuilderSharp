using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Models.Bytecode;

var path = "/Users/admin/codes/Tools/PyRebuild/ref/pycdc/tests/compiled/test_expressions_comprehensive.2.7.pyc";
var data = File.ReadAllBytes(path);
var reader = new PycReader();
var code = reader.Read(data);

Console.WriteLine($"Module: {code.Name}");
Console.WriteLine($"Filename: {code.Filename}");
Console.WriteLine($"Names ({code.Names.Count}): {string.Join(", ", code.Names.Select((n, i) => $"{i}='{n}'"))}");
Console.WriteLine($"Varnames ({code.Varnames.Count}): {string.Join(", ", code.Varnames.Select((n, i) => $"{i}='{n}'"))}");
Console.WriteLine($"Constants ({code.Constants.Count}):");
foreach (var kvp in code.Constants.OrderBy(k => k.Key))
{
    var val = kvp.Value;
    var desc = val switch
    {
        null => "None",
        string s => $"\"{s}\"",
        CodeObject co => $"<CodeObject: {co.Name}>",
        _ => val.ToString()
    };
    Console.WriteLine($"  [{kvp.Key}] {desc} ({val?.GetType().Name ?? "null"})");
}
