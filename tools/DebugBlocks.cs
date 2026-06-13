// debug tool: dump blocks + loop detection for a .pyc file
using PyRebuilderSharp.Core;
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Scanners;
using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.CFG;

if (args.Length < 1) { Console.Error.WriteLine("Usage: DebugBlocks <pycfile>"); return; }

var data = File.ReadAllBytes(args[0]);
var reader = new PycReader();
var code = reader.Read(data);
DumpCode(code, "");

static void DumpCode(CodeObject code, string indent)
{
    Console.WriteLine($"{indent}Code: {code.Name} (argc={code.ArgCount}, vn={code.Varnames.Count}, ins={code.Instructions.Count})");
    Console.WriteLine($"{indent}  Varnames: [{string.Join(",", code.Varnames)}]");
    Console.WriteLine($"{indent}  Instrs:");
    foreach (var ins in code.Instructions)
    {
        var a = ins.Argument.HasValue ? ins.Argument.Value.ToString() : "-";
        Console.WriteLine($"{indent}    {ins.Offset,4} {ins.Opcode,-25} {a}");
    }

    // 异常表
    if (code.ExceptionTable.Count > 0)
    {
        Console.WriteLine($"{indent}  ExceptionTable:");
        foreach (var e in code.ExceptionTable)
            Console.WriteLine($"{indent}    [{e.StartOffset},{e.EndOffset}) → {e.TargetOffset} depth={e.Depth} isExcept={e.IsExcept}");
    }

    var scanner = new BlockScanner();
    var blocks = scanner.Scan(code);
    Console.WriteLine($"{indent}  Blocks ({blocks.Count}):");
    foreach (var b in blocks.OrderBy(b => b.StartOffset))
    {
        Console.WriteLine($"{indent}    B{b.Id}[{b.StartOffset},{b.EndOffset}] op={b.Instructions.LastOrDefault().Opcode} f={b.Flags}");
        Console.WriteLine($"{indent}      pred=[{string.Join(",", b.Predecessors.Select(p => p.Id))}] succ=[{string.Join(",", b.Successors.Select(s => s.Id))}]");
        Console.WriteLine($"{indent}      ins=[{string.Join(" ", b.Instructions.Select(i => i.Opcode))}]");
    }

    var cfScanner = new ControlFlowScanner();
    var cfg = cfScanner.Analyze(blocks);
    try
    {
        Console.WriteLine($"{indent}  Loops ({cfg.Structures.OfType<LoopStructure>().Count()}):");
        foreach (var loop in cfg.Structures.OfType<LoopStructure>())
        {
            var beId = loop.BodyEntry?.Id.ToString() ?? "null";
            var beStart = loop.BodyEntry?.StartOffset.ToString() ?? "null";
            var beEnd = loop.BodyEntry?.EndOffset.ToString() ?? "null";
            var baId = loop.BackEdge?.Id.ToString() ?? "null";
            Console.WriteLine($"{indent}    Header=B{loop.Header.Id}[{loop.Header.StartOffset},{loop.Header.EndOffset}] type={loop.Type}");
            Console.WriteLine($"{indent}      BodyEntry=B{beId}[{beStart},{beEnd}] BE=B{baId}");
            Console.WriteLine($"{indent}      BodyBlocks=[{string.Join(" ", loop.BodyBlocks.Select(b => $"B{b.Id}"))}]");
        }
    }
    catch (Exception ex) 
    {
        Console.WriteLine($"{indent}  Loop analysis error: {ex.Message}");
    }

    Console.WriteLine($"{indent}  LoopHeader blocks: [{string.Join(" ", blocks.Where(b => b.Flags.HasFlag(BlockFlags.LoopHeader)).Select(b => $"B{b.Id}"))}]");

    // Decompile
    Console.WriteLine($"{indent}  === OUTPUT ===");
    var decompiler = new Decompiler();
    try
    {
        // Use the full file's output
    }
    catch {}

    foreach (var child in code.ChildCodes)
    {
        Console.WriteLine();
        DumpCode(child, indent + "  ");
    }
}
