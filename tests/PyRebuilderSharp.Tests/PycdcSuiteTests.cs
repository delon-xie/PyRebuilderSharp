using Xunit;
using Xunit.Abstractions;
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Scanners;
using PyRebuilderSharp.Core.Builders;
using PyRebuilderSharp.Core.Generators;
using PyRebuilderSharp.Core.Testing;
using PyRebuilderSharp.Core.Models.AST;
using Module = PyRebuilderSharp.Core.Models.AST.Module;
using Assert = Xunit.Assert;

namespace PyRebuilderSharp.Tests;

/// <summary>
/// pycdc 完整测试集 E2E 测试。
/// 
/// 运行所有测试用例并生成通过率报告。
/// 由于当前反编译器尚不完整，大部分测试预期失败，
/// 本测试主要用于追踪进度。
/// </summary>
public class PycdcSuiteTests
{
    private readonly ITestOutputHelper _output;
    private readonly PycdcSuiteRunner _runner;

    public PycdcSuiteTests(ITestOutputHelper output)
    {
        _output = output;
        _runner = new PycdcSuiteRunner();
    }

    [Fact]
    public void Run_SmokeTest_SimpleConst()
    {
        // Build pipeline and capture source
        var testDataDir = "/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests";
        var data = File.ReadAllBytes(Path.Combine(testDataDir, "compiled", "simple_const.3.8.pyc"));
        var reader = new PycReader();
        var code = reader.Read(data);
        var scanner = new BlockScanner();
        var blocks = scanner.Scan(code);
        var cfScanner = new ControlFlowScanner();
        var cfg = cfScanner.Analyze(blocks);
        var builder = new AstBuilder(code);
        var ast = builder.Build(cfg);
        var gen = new PythonCodeGenerator();
        var src = gen.Generate(ast);
        
        _output.WriteLine("=== DECOMPILED SOURCE ===");
        _output.WriteLine(src.Replace("\n", "\\n\n"));
        _output.WriteLine("=== END ===");
        
        // Now tokenize and compare
        var dumper = new TokenDumper();
        var actualTokens = dumper.Tokenize(src);
        _output.WriteLine($"Actual tokens: {actualTokens.Count}");
        foreach (var t in actualTokens.Take(20))
            _output.WriteLine($"  {t}");
        
        var result = _runner.RunSingle("simple_const", "3.8");
        _output.WriteLine($"Test: {result.TestName} | v{result.PythonVersion} | " +
                          $"Passed: {result.Passed} | Tokens: {result.ActualTokens}/{result.ExpectedTokens}");
        if (result.ErrorMessage != null)
        {
            var lines = result.ErrorMessage.Split('\n');
            foreach (var line in lines.Take(10))
                _output.WriteLine($"  DIFF: {line}");
        }
    }

    [Fact]
    public void Run_SmokeTest_TestExpressions()
    {
        var result = _runner.RunSingle("test_expressions", "38");
        _output.WriteLine($"Test: {result.TestName} | v{result.PythonVersion} | " +
                          $"Passed: {result.Passed} | Tokens: {result.ActualTokens}/{result.ExpectedTokens}");
        if (!result.Passed && result.ErrorMessage != null)
            _output.WriteLine($"Error: {result.ErrorMessage}");
    }

    [Fact]
    public void DebugWhileLoop() => CheckTest("while_loops2", "38");

    [Fact]
    public void DebugForLoop()
    {
        var r = _runner.RunSingle("test_loops2", "38");
        _output.WriteLine($"test_loops2: Passed={r.Passed} | {r.ActualTokens}/{r.ExpectedTokens}");
        if (r.ErrorMessage != null) _output.WriteLine($"  Err: {r.ErrorMessage}");
        Assert.True(r.Passed, $"For-loop test failed: {r.ErrorMessage}");
    }

    [Fact]
    public void DebugLoops3() => CheckTest("test_loops3", "38");

    [Fact]
    public void DebugExceptions() => CheckTest("test_exceptions", "38");

    [Fact]
    public void DebugForLoopPy38() => CheckTest("test_for_loop_py3.8", "38");

    [Fact]
    public void DebugChainAssign() => CheckTest("chain_assignment", "38");

    private void CheckTest(string name, string ver)
    {
        var r = _runner.RunSingle(name, ver);
        _output.WriteLine($"{name}: Passed={r.Passed} | {r.ActualTokens}/{r.ExpectedTokens}");
        if (r.ErrorMessage != null) _output.WriteLine($"  Err: {r.ErrorMessage}");
    }

    [Fact]
    public void Run_SmokeTest_WhileLoop()
    {
        var result = _runner.RunSingle("while_loops2", "38");
        _output.WriteLine($"Test: {result.TestName} | v{result.PythonVersion} | " +
                          $"Passed: {result.Passed} | Tokens: {result.ActualTokens}/{result.ExpectedTokens}");
        if (result.ErrorMessage != null)
            _output.WriteLine($"Error: {result.ErrorMessage}");
        Assert.True(result.Passed, $"While loop test failed: {result.ErrorMessage}");
    }

    [Fact]
    public void RunComprehensive_Baseline_AllTests()
    {
        SuiteReport report;
        try
        {
            report = _runner.RunAll(maxParallelism: 2);
        }
        catch (Exception ex)
        {
            _output.WriteLine($"FATAL: RunAll threw exception: {ex}");
            throw;
        }

        _output.WriteLine("");
        _output.WriteLine("═══════════════════════════════════════════");
        _output.WriteLine("  PyRebuilderSharp 测试基线报告");
        _output.WriteLine($"  日期: {DateTime.UtcNow:yyyy-MM-dd HH:mm:ss} UTC");
        _output.WriteLine("═══════════════════════════════════════════");
        _output.WriteLine($"  总测试: {report.Total}");
        _output.WriteLine($"  ✅ 通过: {report.Passed}");
        _output.WriteLine($"  ❌ 失败: {report.Failed}");
        _output.WriteLine($"  通过率: {report.PassRate:F1}%");
        _output.WriteLine($"  耗时: {report.Elapsed.TotalSeconds:F1}s");
        _output.WriteLine("───────────────────────────────────────────");

        _output.WriteLine("  分类统计:");
        foreach (var (cat, (p, f, rate)) in report.GetCategorySummary()
                         .Where(x => x.Value.Item1 + x.Value.Item2 > 0)
                         .OrderByDescending(x => x.Value.Item2))
        {
            var totalCat = p + f;
            _output.WriteLine($"    {cat,-15} {totalCat,3} 测试  ✅{p,3}  ❌{f,3}  {rate,5:F1}%");
        }

        _output.WriteLine("───────────────────────────────────────────");

        _output.WriteLine("  Top 失败原因:");
        foreach (var reason in report.GetTopFailureReasons(5))
            _output.WriteLine($"    {reason}");

        _output.WriteLine("  FAIL 具体测试:");
        foreach (var (name, err) in report.GetDetailedFailures(10))
        {
            var shortName = name.Length > 30 ? name[..27] + "..." : name;
            var shortErr = err.Replace("\n", " ").Length > 60
                ? err.Replace("\n", " ")[..57] + "..."
                : err.Replace("\n", " ");
            _output.WriteLine($"    ❌ {shortName,-30} {shortErr}");
        }

        _output.WriteLine("═══════════════════════════════════════════");

        // 基线测试不 assert 通过率，仅记录
    }

    [Fact]
    public void RunComprehensive_AllVersions_FullReport()
    {
        var report = _runner.RunAllVersions(maxParallelism: 2);

        _output.WriteLine("");
        _output.WriteLine("═══ 全版本基线报告 ═══");
        _output.WriteLine($"  总测试: {report.Total}");
        _output.WriteLine($"  ✅ 通过: {report.Passed}");
        _output.WriteLine($"  ❌ 失败: {report.Failed}");
        _output.WriteLine($"  通过率: {report.PassRate:F1}%");
        _output.WriteLine($"  耗时: {report.Elapsed.TotalSeconds:F1}s");

        var byVersion = report.Results
            .GroupBy(r => r.PythonVersion)
            .OrderBy(g => g.Key)
            .ToList();
        _output.WriteLine("  版本分布:");
        foreach (var g in byVersion)
        {
            var p = g.Count(r => r.Passed);
            var f = g.Count(r => !r.Passed);
            var rate = (double)p / (p + f) * 100;
            _output.WriteLine($"    Python {g.Key}: {p}/{p + f} ({rate:F1}%)");
        }
    }
}
