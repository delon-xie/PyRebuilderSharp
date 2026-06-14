using System;
using System.IO;
using PyRebuilderSharp.Core;
using PyRebuilderSharp.Core.Generators;

var files = new[] {
    "/tmp/test_fncall.3.12.pyc",
    "/tmp/simple_class.3.12.pyc", 
    "/tmp/test_walrus.3.12.pyc",
};

foreach (var file in files)
{
    var data = File.ReadAllBytes(file);
    var dc = new Decompiler();
    var result = dc.DecompileWithStats(data);
    Console.WriteLine("=== " + Path.GetFileName(file) + " ===");
    Console.WriteLine(result.SourceCode);
}
