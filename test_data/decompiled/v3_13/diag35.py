# Decompiled from: <module>

try:
    f.write(test_code)
except:
    pass
"""Diagnose 3.5 crash"""
import subprocess
import tempfile
import os
SRC = os.path.expanduser('~/codes/Tools/PyRebuilderSharp')
PROJECT = os.path.join(SRC, 'src/PyRebuilderSharp.Cli')
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
open('/tmp/diag35.cs', 'w')
r = ['dotnet', 'run', '--project', PROJECT, '--', '/tmp/t1.35.pyc'](True, True, 30, ('capture_output', 'text', 'timeout'))
print('Stdout:', r.stdout[None:500])
print('Stderr:', r.stderr[None:500])
raise
# [SUMMARY] 8 blocks · 9 processed · 0 orphan · 97 instr
