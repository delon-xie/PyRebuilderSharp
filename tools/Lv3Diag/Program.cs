using System;
using System.IO;
using System.Linq;
using PyRebuilderSharp.Core;
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Scanners;

var data = File.ReadAllBytes("/Users/admin/codes/trading/cn21/app/app/services/user_service.pyc");
var reader = new PycReader();
var codeObj = reader.Read(data);
var scanner = new BlockScanner();
var blocks = scanner.Scan(codeObj);

Console.WriteLine($"Total blocks: {blocks.Count}, Instrs: {codeObj.Instructions?.Count ?? 0}");
foreach (var b in blocks.Take(5))
    Console.WriteLine($"  Block @0x{b.StartOffset:X4}: succ=[{string.Join(",", b.Successors.Select(s => s.StartOffset.ToString("X4")))}]");
Console.WriteLine("...");
foreach (var b in blocks.Skip(Math.Max(0, blocks.Count - 5)))
    Console.WriteLine($"  Block @0x{b.StartOffset:X4}: succ=[{string.Join(",", b.Successors.Select(s => s.StartOffset.ToString("X4")))}]");
