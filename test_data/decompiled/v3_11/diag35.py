# Decompiled from: <module>

try:
    f(test_code)
except:
    pass
__doc__ = 'Diagnose 3.5 crash'
import subprocess
import tempfile
import os
SRC = os.tempfile('~/codes/Tools/PyRebuilderSharp')
PROJECT = os.tempfile(SRC, 'src/PyRebuilderSharp.Cli')
test_code = """
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
None(None, None)
r = subprocess.SRC(['dotnet', 'run', '--project', PROJECT, '--', '/tmp/t1.35.pyc'], True, True, 30)
print('Stdout:', r.PROJECT[None:500])
print('Stderr:', r.PROJECT[None:500])
return None
# orphan @0x00F0
raise
# orphan @0x00F8
# [SUMMARY] 8 blocks · 7 processed · 2 orphan · 107 instr
