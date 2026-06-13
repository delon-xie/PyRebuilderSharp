using PyRebuilderSharp.Core;

namespace PyRebuilderSharp.Cli;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length < 1)
        {
            Console.Error.WriteLine("Usage: pyrebuilder <input.pyc> [-o output.py]");
            Console.Error.WriteLine("Options:");
            Console.Error.WriteLine("  -o, --output <file>   Output file (default: stdout)");
            return;
        }

        var inputFile = args[0];
        string? outputFile = null;

        for (int i = 1; i < args.Length; i++)
        {
            if (args[i] is "-o" or "--output" && i + 1 < args.Length)
                outputFile = args[i + 1];
        }

        if (!File.Exists(inputFile))
        {
            Console.Error.WriteLine($"Error: File not found: {inputFile}");
            return;
        }

        try
        {
            var pycData = File.ReadAllBytes(inputFile);
            var decompiler = new Decompiler();
            var result = decompiler.DecompileWithStats(pycData);

            if (outputFile != null)
            {
                File.WriteAllText(outputFile, result.SourceCode);
                Console.WriteLine($"Decompiled: {inputFile} → {outputFile}");
                Console.WriteLine($"Elapsed: {result.Elapsed.TotalMilliseconds:F0}ms");
            }
            else
            {
                Console.WriteLine(result.SourceCode);
            }
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Error: {ex.GetType().Name}: {ex.Message}");
            Console.Error.WriteLine($"Stack: {ex.StackTrace}");
            if (ex.InnerException != null)
            {
                Console.Error.WriteLine($"Inner: {ex.InnerException.GetType().Name}: {ex.InnerException.Message}");
                Console.Error.WriteLine($"Inner Stack: {ex.InnerException.StackTrace}");
            }
        }
    }
}
