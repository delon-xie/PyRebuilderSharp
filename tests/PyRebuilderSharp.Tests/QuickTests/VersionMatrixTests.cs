using Xunit;
using Xunit.Abstractions;
using PyRebuilderSharp.Core.Testing;

namespace PyRebuilderSharp.Tests;

/// <summary>
/// 版本矩阵测试 — 每个 .py 测试用所有可用 Python 版本编译的 .pyc 进行测试。
/// 按层级递进：表达式 → 顺序代码 → 控制块 → 嵌套控制块 → 函数 → 模块
/// </summary>
public class VersionMatrixTests
{
    private readonly ITestOutputHelper _output;
    private readonly PycdcSuiteRunner _runner;

    public VersionMatrixTests(ITestOutputHelper output)
    {
        _output = output;
        _runner = new PycdcSuiteRunner();
    }

    public static IEnumerable<object[]> GetAllVersionTests()
    {
        var runner = new PycdcSuiteRunner();
        var tests = runner.GetAvailableTests();
        foreach (var t in tests)
            yield return new object[] { t.TestName, t.PycFile, t.PythonVersion };
    }

    /// <summary>
    /// Lv0: 表达式级别 — test_expressions_comprehensive
    /// </summary>
    [Theory]
    [MemberData(nameof(GetExpressionsVersionData))]
    public void Lv0_Expressions(string testName, string pycFile, string pyVersion)
    {
        var r = _runner.RunSingleFile(testName, pycFile);
        if (!r.Passed)
        {
            _output.WriteLine($"❌ {testName} v{pyVersion}: {r.ErrorMessage}");
            if (r.ErrorMessage?.Contains("AST parse failed") == true)
            {
                // AST 解析失败时输出源码供调试
                _output.WriteLine($"  Error: {r.ErrorMessage}");
            }
        }
        else
        {
            _output.WriteLine($"✅ {testName} v{pyVersion}");
        }
        Assert.True(r.Passed, $"{testName} v{pyVersion}: {r.ErrorMessage}");
    }

    public static IEnumerable<object[]> GetExpressionsVersionData()
    {
        var runner = new PycdcSuiteRunner();
        return runner.GetAvailableTests("test_expr_basic", onlyModernPython: false)
            .Where(t => {
                var v = t.PythonVersion;
                return v == "2.7" || v == "3.5" || v == "3.6" || v == "3.7" || v == "3.8" || v == "3.9" || v == "3.10";
            })
            .Select(t => new object[] { t.TestName, t.PycFile, t.PythonVersion });
    }

    /// <summary>
    /// Lv1: 顺序代码块 — test_seq_clean
    /// </summary>
    [Theory]
    [MemberData(nameof(GetSequentialVersionData))]
    public void Lv1_Sequential(string testName, string pycFile, string pyVersion)
    {
        var r = _runner.RunSingleFile(testName, pycFile);
        if (!r.Passed)
        {
            _output.WriteLine($"❌ {testName} v{pyVersion}: {r.ErrorMessage}");
        }
        else
        {
            _output.WriteLine($"✅ {testName} v{pyVersion}");
        }
        Assert.True(r.Passed, $"{testName} v{pyVersion}: {r.ErrorMessage}");
    }

    public static IEnumerable<object[]> GetSequentialVersionData()
    {
        var runner = new PycdcSuiteRunner();
        return runner.GetAvailableTests("test_seq_clean", onlyModernPython: false)
            .Where(t => {
                var v = t.PythonVersion;
                return v == "2.7" || v == "3.5" || v == "3.6" || v == "3.7" || v == "3.8" || v == "3.9" || v == "3.10";
            })
            .Select(t => new object[] { t.TestName, t.PycFile, t.PythonVersion });
    }

    /// <summary>
    /// Lv2: 控制流 — test_control_flow
    /// </summary>
    [Theory]
    [MemberData(nameof(GetControlFlowVersionData))]
    public void Lv2_ControlFlow(string testName, string pycFile, string pyVersion)
    {
        var r = _runner.RunSingleFile(testName, pycFile);
        if (!r.Passed)
            _output.WriteLine($"❌ {testName} v{pyVersion}: {r.ErrorMessage}");
        else
            _output.WriteLine($"✅ {testName} v{pyVersion}");
        Assert.True(r.Passed, $"{testName} v{pyVersion}: {r.ErrorMessage}");
    }

    public static IEnumerable<object[]> GetControlFlowVersionData()
    {
        var runner = new PycdcSuiteRunner();
        return runner.GetAvailableTests("test_control_flow", onlyModernPython: false)
            .Where(t => {
                var v = t.PythonVersion;
                return v == "2.7" || v == "3.5" || v == "3.6" || v == "3.7" || v == "3.8" || v == "3.9" || v == "3.10";
            })
            .Select(t => new object[] { t.TestName, t.PycFile, t.PythonVersion });
    }

    // ==================== Lv3: Nested Control Blocks ====================

    /// <summary>
    /// Lv3a: 5 层同类型嵌套压力 — test_nested_depth_5
    /// </summary>
    [Theory]
    [MemberData(nameof(GetNestedDepthVersionData))]
    public void Lv3_NestedDepth(string testName, string pycFile, string pyVersion)
    {
        var r = _runner.RunSingleFile(testName, pycFile);
        if (!r.Passed)
            _output.WriteLine($"❌ {testName} v{pyVersion}: {r.ErrorMessage}");
        else
            _output.WriteLine($"✅ {testName} v{pyVersion}");
        Assert.True(r.Passed, $"{testName} v{pyVersion}: {r.ErrorMessage}");
    }

    public static IEnumerable<object[]> GetNestedDepthVersionData()
    {
        var runner = new PycdcSuiteRunner();
        return runner.GetAvailableTests("test_nested_depth_5", onlyModernPython: false)
            .Where(t => {
                var v = t.PythonVersion;
                return v == "2.7" || v == "3.5" || v == "3.6" || v == "3.7" || v == "3.8" || v == "3.9" || v == "3.10";
            })
            .Select(t => new object[] { t.TestName, t.PycFile, t.PythonVersion });
    }

    /// <summary>
    /// Lv3b: 5 层混合类型嵌套 — test_nested_mixed_5
    /// </summary>
    [Theory]
    [MemberData(nameof(GetNestedMixedVersionData))]
    public void Lv3_NestedMixed(string testName, string pycFile, string pyVersion)
    {
        var r = _runner.RunSingleFile(testName, pycFile);
        if (!r.Passed)
            _output.WriteLine($"❌ {testName} v{pyVersion}: {r.ErrorMessage}");
        else
            _output.WriteLine($"✅ {testName} v{pyVersion}");
        Assert.True(r.Passed, $"{testName} v{pyVersion}: {r.ErrorMessage}");
    }

    public static IEnumerable<object[]> GetNestedMixedVersionData()
    {
        var runner = new PycdcSuiteRunner();
        return runner.GetAvailableTests("test_nested_mixed_5", onlyModernPython: false)
            .Where(t => {
                var v = t.PythonVersion;
                return v == "2.7" || v == "3.5" || v == "3.6" || v == "3.7" || v == "3.8" || v == "3.9" || v == "3.10";
            })
            .Select(t => new object[] { t.TestName, t.PycFile, t.PythonVersion });
    }

    /// <summary>
    /// Lv3c: 12 对偶 + 8 三重 + 2 四重组合 — test_nested_matrix
    /// </summary>
    [Theory]
    [MemberData(nameof(GetNestedMatrixVersionData))]
    public void Lv3_NestedMatrix(string testName, string pycFile, string pyVersion)
    {
        var r = _runner.RunSingleFile(testName, pycFile);
        if (!r.Passed)
            _output.WriteLine($"❌ {testName} v{pyVersion}: {r.ErrorMessage}");
        else
            _output.WriteLine($"✅ {testName} v{pyVersion}");
        Assert.True(r.Passed, $"{testName} v{pyVersion}: {r.ErrorMessage}");
    }

    public static IEnumerable<object[]> GetNestedMatrixVersionData()
    {
        var runner = new PycdcSuiteRunner();
        return runner.GetAvailableTests("test_nested_matrix", onlyModernPython: false)
            .Where(t => {
                var v = t.PythonVersion;
                return v == "2.7" || v == "3.5" || v == "3.6" || v == "3.7" || v == "3.8" || v == "3.9" || v == "3.10";
            })
            .Select(t => new object[] { t.TestName, t.PycFile, t.PythonVersion });
    }
}
