using PyRebuilderSharp.Core.Builders;
using PyRebuilderSharp.Core.Generators;
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Scanners;
using PyRebuilderSharp.Core.Services;

namespace PyRebuilderSharp.Core;

/// <summary>
/// 反编译器主入口。
/// 编排四个阶段的执行流水线（Phase 1-4）。
/// 核心特性：逐块反编译 + 注释兜底（失败块不影响其他块）。
/// </summary>
public class Decompiler
{
    private readonly DecompileOptions _options;

    public Decompiler(DecompileOptions? options = null)
    {
        _options = options ?? new DecompileOptions();
    }

    /// <summary>
    /// 反编译 .pyc 文件为 Python 源代码。
    /// </summary>
    public string Decompile(byte[] pycData)
        => DecompileWithStats(pycData).SourceCode;

    /// <summary>
    /// 反编译并返回完整统计信息。
    /// </summary>
    public DecompileResult DecompileWithStats(byte[] pycData)
    {
        var startTime = DateTime.UtcNow;
        string sourceCode;
        int totalBlocks = 0, failedBlocks = 0;

        try
        {
            // Phase 1: 读取字节码
            var reader = new PycReader();
            var codeObject = reader.Read(pycData);

            // Phase 2: 分块与控制流分析
            var blockScanner = new BlockScanner();
            var blocks = blockScanner.Scan(codeObject);
            var cfScanner = new ControlFlowScanner();
            var structuredCFG = cfScanner.Analyze(blocks);

            // Phase 3: AST构建（含BlockDecompiler逐块反编译 + 注释兜底）
            var astBuilder = new AstBuilder(codeObject, _options);
            var ast = astBuilder.Build(structuredCFG);

            // 获取块级统计
            totalBlocks = astBuilder.TotalBlockCount;
            failedBlocks = astBuilder.FailedBlockCount;

            // Phase 4: 代码生成
            var generator = new PythonCodeGenerator();
            sourceCode = generator.Generate(ast);
        }
        catch (Exception ex)
        {
            // 记录崩溃到 ~/.pyrebuilder/crashes/
            var crashPath = CrashCollector.RecordCrash(
                new CrashContext { FileName = "anonymous", PythonVersion = "?" },
                ex, pycData.Length);

            var innerMsg = ex.InnerException != null
                ? $" | Inner: {ex.InnerException.GetType().Name}: {ex.InnerException.Message}"
                : "";
            sourceCode = $"# Decompilation failed: {ex.GetType().Name}: {ex.Message}{innerMsg}\n" +
                         $"# Crash report: {crashPath ?? "(write failed)"}\n" +
                         $"# Stack: {ex.StackTrace?.Replace("\n", "\n#  ")}";
        }

        var elapsed = DateTime.UtcNow - startTime;

        return new DecompileResult
        {
            SourceCode = sourceCode,
            Elapsed = elapsed,
            TotalBlocks = totalBlocks,
            FailedBlocks = failedBlocks
        };
    }

    public class DecompileResult
    {
        public string SourceCode { get; set; } = "";
        public TimeSpan Elapsed { get; set; }
        public int TotalBlocks { get; set; }
        public int FailedBlocks { get; set; }
    }
}
