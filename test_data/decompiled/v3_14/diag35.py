# Decompiled from: <module>

name_0 = 'Diagnose 3.5 crash'
import name_1
import name_2
import name_3
name_6 = name_3.name_4.name_5('~/codes/Tools/PyRebuilderSharp')
name_8 = name_3.name_4.name_7(name_6, 'src/PyRebuilderSharp.Cli')
name_9 = """
using PyRebuilderSharp.Core;
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Scanners;
using PyRebuilderSharp.Core.Builders;
using PyRebuilderSharp.Core.Generators;

var data = File.ReadAllBytes(args[0]);
Console.Error.WriteLine("File size: " + data.Length);

var reader = new PycReader();
try {
    var code = reader.Read(data);
    Console.Error.WriteLine("Code read: OK");
    Console.Error.WriteLine("  Names count: " + code.Names.Count);
    Console.Error.WriteLine("  Varnames count: " + code.Varnames.Count);
    Console.Error.WriteLine("  Instructions: " + (code.Instructions?.Count ?? 0));
    if (code.Names.Count > 0)
        Console.Error.WriteLine("  Names[0]: " + code.Names[0]);
    if (code.Varnames.Count > 0)
        Console.Error.WriteLine("  Varnames[0]: " + code.Varnames[0]);
} catch (Exception ex) {
    Console.Error.WriteLine("ERROR: " + ex.GetType().Name + ": " + ex.Message);
}
"""
name_11.name_12(name_9)
name_11 := None('/tmp/diag35.cs', 'w')()(None, None, None)
name_14 = None(['dotnet', 'run', '--project', name_8, '--', '/tmp/t1.35.pyc'], True, True, ('capture_output', 'text', 'timeout'))
None('Stdout:', name_14.name_16 + None)
None(None, name_14.name_17 + None)
return None
if not True:
    pass
raise
# [SUMMARY] 4 blocks · 5 processed · 0 orphan · 103 instr
