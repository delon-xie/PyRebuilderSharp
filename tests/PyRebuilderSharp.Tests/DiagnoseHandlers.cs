// Quick diagnostic: prints handler block info for test_try_except
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Scanners;

var data = File.ReadAllBytes(args[0]);
var reader = new PycReader();
var code = reader.Read(data);

foreach (var child in code.ChildCodes)
{
    if (child.Name == "test_try_except")
    {
        Console.WriteLine($"Function: {child.Name}");
        Console.WriteLine($"Instructions:");
        foreach (var ins in child.Instructions)
            Console.WriteLine($"  {ins.Offset,3}: Opcode={ins.Opcode} Arg={ins.Argument}");
        
        var scanner = new BlockScanner();
        var blocks = scanner.Scan(child);
        Console.WriteLine($"\nBlocks ({blocks.Count}):");
        foreach (var b in blocks)
        {
            Console.Write($"  BB#{b.Id} @0x{b.StartOffset:X4}:");
            foreach (var ins in b.Instructions)
                Console.Write($" [{ins.Offset}]{(byte)ins.Opcode:X2}({ins.Argument})");
            Console.Write(" -> successors:");
            foreach (var s in b.Successors)
                Console.Write($" BB#{s.Id}@0x{s.StartOffset:X4}");
            Console.WriteLine();
        }
    }
}
