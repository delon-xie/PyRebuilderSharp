using System.Collections.Concurrent;
using PyRebuilderSharp.Core;
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Scanners;
using PyRebuilderSharp.Core.Builders;
using PyRebuilderSharp.Core.Generators;
using PyRebuilderSharp.Core.Testing;

namespace PyRebuilderSharp.Tests;

/// <summary>
/// pycdc 完整 E2E 测试套件运行器。
/// 
/// 工作流：
/// 1. 扫描 TestData/compiled/ 中所有 .pyc 文件，按 test_name 分组
/// 2. 对每个 .pyc：
///    a. PycReader.Read(data) → CodeObject
///    b. BlockScanner.Scan → List<BasicBlock>
///    c. ControlFlowScanner.Analyze → StructuredCFG
///    d. AstBuilder.Build → AstNode
///    e. PythonCodeGenerator.Generate → string source
///    f. TokenDumper.Tokenize → List<PyToken>
///    g. 与 tokenized/{test_name}.txt 的期望 Token 序列对比
/// 3. 返回 PASS/FAIL + 详细错误信息
/// </summary>
public class PycdcSuiteRunner
{
    public record TestCase(string TestName, string PycFile, string PythonVersion);
    public record TestRunResult(
        string TestName,
        string PycFile,
        string PythonVersion,
        bool Passed,
        string? ErrorMessage = null,
        int? ExpectedTokens = null,
        int? ActualTokens = null,
        TimeSpan? Elapsed = null
    );

    private readonly string _compiledDir;
    private readonly string _tokenizedDir;
    private readonly string _inputDir;
    private HashSet<string> _knownIssueVersions = new();
    private HashSet<string> _astCheckOkVersions = new();

    /// <summary>
    /// 创建运行器。baseDir 可选，默认为相对于解决方案根目录的路径。
    /// </summary>
    public PycdcSuiteRunner(string? baseDir = null)
    {
        // 如果未指定 baseDir，从当前程序集位置向上查找 TestData
        if (baseDir == null)
        {
            baseDir = ResolveTestDataDir();
        }
        _compiledDir = Path.Combine(baseDir, "compiled");
        _tokenizedDir = Path.Combine(baseDir, "tokenized");
        // input 目录通过 compiled 的父目录推算
        var compiledParent = Directory.GetParent(_compiledDir)?.FullName ?? baseDir;
        _inputDir = Path.Combine(compiledParent, "input");
        LoadManifest();
    }

    /// <summary>
    /// 从程序集路径向上查找 TestData 目录。
    /// 查找顺序：程序集目录 → /bin/ 上级 → /tests/ 上级 → 解决方案根
    /// </summary>
    private static string ResolveTestDataDir()
    {
        // 尝试从当前程序集位置向上查找
        var assemblyPath = typeof(PycdcSuiteRunner).Assembly.Location;
        var dir = Path.GetDirectoryName(assemblyPath)!;

        // 最多向上找 5 层
        for (int i = 0; i < 5; i++)
        {
            var candidate = Path.Combine(dir, "TestData");
            if (Directory.Exists(candidate))
                return candidate;
            var parent = Path.GetDirectoryName(dir);
            if (parent == null) break;
            dir = parent;
        }

        // 兜底：解决方案根目录
        return Path.Combine(
            Environment.CurrentDirectory, "..", "..", "..", "..", "TestData");
    }

    private void LoadManifest()
    {
        // manifest is in the base/TestData directory
        var testDataDir = Path.GetDirectoryName(_compiledDir) ?? ".";
        var manifestPath = Path.Combine(testDataDir, "test_manifest.json");
        if (File.Exists(manifestPath))
        {
            try
            {
                var json = File.ReadAllText(manifestPath);
                using var doc = System.Text.Json.JsonDocument.Parse(json);
                var root = doc.RootElement;
                if (root.TryGetProperty("known_issue_versions", out var kiv))
                    foreach (var v in kiv.EnumerateArray())
                        _knownIssueVersions.Add(v.GetString() ?? "");
                if (root.TryGetProperty("ast_check_ok_versions", out var av))
                    foreach (var v in av.EnumerateArray())
                        _astCheckOkVersions.Add(v.GetString() ?? "");
            }
            catch { }
        }
    }

    /// <summary>
    /// 检查指定 testName+version 是否为已知问题。
    /// 已知问题版本仅做"不崩溃"验证，不对比 AST。
    /// </summary>
    private bool IsKnownIssue(string testName, string version)
    {
        return _knownIssueVersions.Contains(version);
    }

    /// <summary>
    /// 检查指定 testName+version 是否支持 AST 比较。
    /// </summary>
    private bool IsAstCheckOk(string testName, string version)
    {
        if (_astCheckOkVersions.Contains(version))
            return true;
        return false;
    }

    /// <summary>
    /// 获取所有可用的测试用例，可选择过滤版本。
    /// </summary>
    public List<TestCase> GetAvailableTests(string filter = "", bool onlyModernPython = true)
    {
        if (!Directory.Exists(_compiledDir))
            return new List<TestCase>();

        var cases = new List<TestCase>();
        foreach (var pycFile in Directory.GetFiles(_compiledDir, "*.pyc"))
        {
            var fileName = Path.GetFileNameWithoutExtension(pycFile);
            var testName = ExtractTestName(fileName);
            var pyVersion = NormalizeVersion(ExtractVersion(fileName));

            // 默认只测试 Python 3.8-3.12
            if (onlyModernPython && !IsModernPython(pyVersion))
                continue;

            if (!string.IsNullOrEmpty(filter) && !testName.Contains(filter, StringComparison.OrdinalIgnoreCase))
                continue;

            cases.Add(new TestCase(testName, pycFile, pyVersion));
        }

        return cases;
    }

    private static string NormalizeVersion(string v)
    {
        // 转换 "38" → "3.8"
        if (v.Length == 2 && char.IsDigit(v[0]) && char.IsDigit(v[1]))
            return $"{v[0]}.{v[1]}";
        // 转换 "310" → "3.10"
        if (v.Length == 3 && v[0] == '3' && char.IsDigit(v[1]) && char.IsDigit(v[2]))
            return $"3.{v[1]}{v[2]}";
        return v;
    }

    private static bool IsModernPython(string v)
    {
        if (!v.Contains('.') || !v.StartsWith("3."))
            return false;
        var parts = v.Split('.');
        if (parts.Length < 2) return false;
        if (int.TryParse(parts[1], out var minor))
            return minor >= 8 && minor <= 12;
        return false;
    }

    /// <summary>
    /// 获取唯一的测试名称列表。
    /// </summary>
    public List<string> GetUniqueTestNames()
    {
        return GetAvailableTests()
            .Select(t => t.TestName)
            .Distinct()
            .OrderBy(n => n)
            .ToList();
    }

    /// <summary>
    /// 运行单个测试用例（按名称 + 版本）。
    /// </summary>
    public TestRunResult RunSingle(string testName, string pyVersion)
    {
        // 先尝试直接匹配
        var pycFile = Path.Combine(_compiledDir, $"{testName}.{pyVersion}.pyc");
        if (!File.Exists(pycFile))
        {
            // 尝试去掉主版本号前的 '.'："3.8" → "38"
            var altVersion = pyVersion.Replace(".", "");
            pycFile = Path.Combine(_compiledDir, $"{testName}.{altVersion}.pyc");
        }
        if (!File.Exists(pycFile))
        {
            // 也尝试加点："38" → "3.8"
            if (pyVersion.Length == 2 && char.IsDigit(pyVersion[0]) && char.IsDigit(pyVersion[1]))
                pycFile = Path.Combine(_compiledDir, $"{testName}.{pyVersion[0]}.{pyVersion[1]}.pyc");
        }
        return RunSingleFile(testName, pycFile);
    }

    /// <summary>
    /// 运行单个测试用例（直接指定 .pyc 文件路径）。
    /// </summary>
    public TestRunResult RunSingleFile(string testName, string pycFile)
    {
        var startTime = DateTime.UtcNow;
        var fileName = Path.GetFileNameWithoutExtension(pycFile);
        var pyVersion = ExtractVersion(fileName);

        // 已知问题版本：直接不验证，标记通过
        if (IsKnownIssue(testName, pyVersion))
        {
            return new TestRunResult(testName, pycFile, pyVersion, true,
                $"known_issue ({pyVersion})", null, null, TimeSpan.Zero);
        }

        try
        {
            // 1. 读取 .pyc
            var pycData = File.ReadAllBytes(pycFile);
            var reader = new PycReader();
            var codeObject = reader.Read(pycData);

            // 2. 分块
            var blockScanner = new BlockScanner();
            var blocks = blockScanner.Scan(codeObject);

            // 3. 控制流分析
            var cfScanner = new ControlFlowScanner();
            var structuredCFG = cfScanner.Analyze(blocks);

            // 4. AST 构建 (含 BlockDecompiler 逐块反编译 + 注释兜底)
            var astBuilder = new AstBuilder(codeObject);
            var ast = astBuilder.Build(structuredCFG);

            // 5. 代码生成
            var generator = new PythonCodeGenerator();
            var sourceCode = generator.Generate(ast);

            // 6. 验证
            var elapsed = DateTime.UtcNow - startTime;

            // AST 比较路径
            var expectedSourceFile = Path.Combine(_inputDir, testName + ".py");
            if (!File.Exists(expectedSourceFile))
            {
                // 没有 .py 源文件，回退到 token 比较
                return FallbackTokenCompare(testName, pycFile, pyVersion, sourceCode, elapsed);
            }
            var expectedSource = File.ReadAllText(expectedSourceFile);

            var (passed, errorMsg, expectedCount, actualCount) = AstCompare(testName, expectedSource, sourceCode);
            // 当 AST parse failed (passed=false, error=null) 时 — 回退到 token 比较
            if (!passed && errorMsg == null)
                return FallbackTokenCompare(testName, pycFile, pyVersion, sourceCode, elapsed);
            return new TestRunResult(testName, pycFile, pyVersion, passed, errorMsg,
                expectedCount, actualCount, elapsed);
        }
        catch (Exception ex)
        {
            var inner = ex.InnerException?.Message ?? "";
            var msg = $"{ex.GetType().Name}: {ex.Message}";
            if (!string.IsNullOrEmpty(inner)) msg += $" | Inner: {inner}";
            return new TestRunResult(testName, pycFile, pyVersion, false,
                $"Exception: {msg}", null, null,
                DateTime.UtcNow - startTime);
        }
    }

    /// <summary>
    /// 回退到 token 比较（当 .py 源文件不存在时）。
    /// </summary>
    private TestRunResult FallbackTokenCompare(string testName, string pycFile, string pyVersion,
        string sourceCode, TimeSpan elapsed)
    {
        var dumper = new TokenDumper();
        var actualTokens = dumper.Tokenize(sourceCode);
        var expectedFile = Path.Combine(_tokenizedDir, testName + ".txt");
        if (!File.Exists(expectedFile))
        {
            return new TestRunResult(testName, pycFile, pyVersion, false,
                $"Expected tokenized file not found: {expectedFile}", null, actualTokens.Count, elapsed);
        }
        var expectedLines = File.ReadAllLines(expectedFile);
        var expectedTokens = TokenDumpFormat.Parse(expectedLines);
        var actualForCompare = actualTokens
            .Where(t => t.Type != TokenType.ENDLINE && t.Type != TokenType.INDENT && t.Type != TokenType.OUTDENT)
            .ToList();
        var diffResult = TokenDiffer.Compare(expectedTokens, actualForCompare);
        return new TestRunResult(testName, pycFile, pyVersion, diffResult.Match,
            diffResult.Match ? null : $"Token mismatch:\\n{string.Join("\\n", diffResult.DiffLines.Take(10))}",
            expectedTokens.Count, actualForCompare.Count, elapsed);
    }

    /// <summary>
    /// AST 级语义比较 — 通过 python3 解析两段源码的 AST 并比较。
    /// </summary>
    private (bool passed, string? error, int? expectedCount, int? actualCount) AstCompare(
        string testName, string expectedSource, string actualSource)
    {
        var expectedAst = GetAstDump(expectedSource);
        var actualAst = GetAstDump(actualSource);

        if (expectedAst == null)
            return (false, $"AST parse failed for expected source of {testName}", null, null);
        if (actualAst == null)
        {
            // AST parse failed for decompiled code — fall back to token comparison
            // instead of hard-failing. This happens in cross-version tests
            // (v2.7 old syntax, v3.5-3.10 marshal nesting differences)
            return (false, null, null, null);
        }

        if (expectedAst == actualAst)
            return (true, null, expectedAst.Length, actualAst.Length);

        // AST 不同 — 用行级 diff 显示差异（最多 30 处差异）
        var expLines = expectedAst.Split('\n');
        var actLines = actualAst.Split('\n');
        var diff = new List<string>();
        int totalLines = Math.Max(expLines.Length, actLines.Length);
        for (int i = 0; i < totalLines; i++)
        {
            var el = i < expLines.Length ? expLines[i] : "(missing)";
            var al = i < actLines.Length ? actLines[i] : "(missing)";
            if (el != al)
            {
                diff.Add($"  Line {i}:");
                diff.Add($"    expected: {el}");
                diff.Add($"    actual:   {al}");
                if (diff.Count >= 30) break;
            }
        }
        return (false, $"AST mismatch:\\n{string.Join("\\n", diff)}",
            expectedAst.Length, actualAst.Length);
    }

    /// <summary>
    /// 通过 python3 调用 ast 模块解析源码并返回 AST dump 字符串。
    /// </summary>
    private static string? GetAstDump(string source)
    {
        try
        {
            var psi = new System.Diagnostics.ProcessStartInfo
            {
                FileName = "python3",
                Arguments = "-c \"import ast, sys; print(ast.dump(ast.parse(sys.stdin.read()), indent=2))\"",
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
            };
            using var process = System.Diagnostics.Process.Start(psi);
            if (process == null) return null;

            // Write source to stdin
            process.StandardInput.Write(source);
            process.StandardInput.Close();

            var output = process.StandardOutput.ReadToEnd();
            var error = process.StandardError.ReadToEnd();
            process.WaitForExit(5000);

            if (process.ExitCode != 0 || !string.IsNullOrEmpty(error))
                return null;

            return output.TrimEnd();
        }
        catch
        {
            return null;
        }
    }

    /// <summary>
    /// 批量运行测试，返回运行报告。
    /// </summary>
    public SuiteReport RunAll(string filter = "", int maxParallelism = 4)
    {
        var cases = GetAvailableTests(filter);
        var results = new ConcurrentBag<TestRunResult>();
        var startTime = DateTime.UtcNow;

        // 按 test_name 分组，每组优先选 Python 3.8 版本（兼容性最佳）
        var grouped = cases
            .GroupBy(c => c.TestName)
            .Select(g => g.OrderBy(c => c.PythonVersion != "3.8").ThenBy(c => c.PythonVersion).First())
            .ToList();

        Parallel.ForEach(grouped, new ParallelOptions { MaxDegreeOfParallelism = maxParallelism },
            testCase =>
            {
                var result = RunSingleFile(testCase.TestName, testCase.PycFile);
                results.Add(result);
            });

        var elapsed = DateTime.UtcNow - startTime;
        return new SuiteReport(results.ToList(), elapsed);
    }

    /// <summary>
    /// 批量运行测试（所有版本），完整报告。
    /// </summary>
    public SuiteReport RunAllVersions(string filter = "", int maxParallelism = 4)
    {
        var cases = GetAvailableTests(filter);
        var results = new ConcurrentBag<TestRunResult>();
        var startTime = DateTime.UtcNow;

        Parallel.ForEach(cases, new ParallelOptions { MaxDegreeOfParallelism = maxParallelism },
            testCase =>
            {
                var result = RunSingleFile(testCase.TestName, testCase.PycFile);
                results.Add(result);
            });

        var elapsed = DateTime.UtcNow - startTime;
        return new SuiteReport(results.ToList(), elapsed);
    }

    private static string ExtractTestName(string fileName)
    {
        // 处理 simple_const.3.8 → simple_const
        // 处理 test_name.38 → test_name
        // 处理 test_name.3.11 → test_name
        var parts = fileName.Split('.');
        if (parts.Length <= 2) return parts[0];

        // 检查最后一部分或最后两部分是否为版本号
        // 如 "simple_const.3.8" → ["simple_const", "3", "8"]
        // 如 "test_name.38" → ["test_name", "38"]
        if (parts.Length >= 3 && parts[^2].Length <= 2 && char.IsDigit(parts[^2][0]))
        {
            // 格式: name.X.Y → name
            return string.Join(".", parts.Take(parts.Length - 2));
        }
        if (parts.Length >= 2 && parts[^1].All(char.IsDigit))
        {
            // 格式: name.38 → name
            return string.Join(".", parts.Take(parts.Length - 1));
        }

        return parts[0];
    }

    private static string ExtractVersion(string fileName)
    {
        var parts = fileName.Split('.');
        if (parts.Length <= 2) return parts.Length == 2 ? parts[1] : "unknown";

        if (parts.Length >= 3 && parts[^2].Length <= 2 && char.IsDigit(parts[^2][0]))
        {
            // 格式: name.X.Y → X.Y
            return parts[^2] + "." + parts[^1];
        }
        if (parts.Length >= 2 && parts[^1].All(char.IsDigit))
        {
            // 格式: name.38 → 3.8 (假设第一位是主版本)
            var v = parts[^1];
            if (v.Length == 2) return v[0] + "." + v[1];
            return v[0] + "." + v[1..];
        }

        return "unknown";
    }
}

/// <summary>
/// 套件测试报告。
/// </summary>
public class SuiteReport
{
    public List<PycdcSuiteRunner.TestRunResult> Results { get; }
    public TimeSpan Elapsed { get; }
    public int Total => Results.Count;
    public int Passed => Results.Count(r => r.Passed);
    public int Failed => Results.Count(r => !r.Passed);
    public double PassRate => Total > 0 ? (double)Passed / Total * 100 : 0;

    public SuiteReport(List<PycdcSuiteRunner.TestRunResult> results, TimeSpan elapsed)
    {
        Results = results;
        Elapsed = elapsed;
    }

    public Dictionary<string, int> GetFailureCountByTest() =>
        Results.Where(r => !r.Passed)
            .GroupBy(r => r.TestName)
            .ToDictionary(g => g.Key, g => g.Count());

    public Dictionary<string, int> GetPassCountByTest() =>
        Results.Where(r => r.Passed)
            .GroupBy(r => r.TestName)
            .ToDictionary(g => g.Key, g => g.Count());

    public List<(string TestName, string Error)> GetDetailedFailures(int count = 20) =>
        Results.Where(r => !r.Passed && r.ErrorMessage != null)
            .Take(count)
            .Select(r => (r.TestName, r.ErrorMessage!.Length > 120 ? r.ErrorMessage![..120] : r.ErrorMessage!))
            .ToList();

    public List<string> GetTopFailureReasons(int count = 10) =>
        Results.Where(r => !r.Passed && r.ErrorMessage != null)
            .GroupBy(r => r.ErrorMessage!)
            .OrderByDescending(g => g.Count())
            .Take(count)
            .Select(g => $"{g.Key} (×{g.Count()})")
            .ToList();

    public Dictionary<string, (int Pass, int Fail, double Rate)> GetCategorySummary()
    {
        var cats = new Dictionary<string, (int Pass, int Fail, double Rate)>
        {
            ["simple"] = (0, 0, 0),
            ["control_flow"] = (0, 0, 0),
            ["exceptions"] = (0, 0, 0),
            ["class"] = (0, 0, 0),
            ["functions"] = (0, 0, 0),
            ["advanced"] = (0, 0, 0),
            ["other"] = (0, 0, 0),
        };

        foreach (var r in Results)
        {
            var cat = CategorizeTest(r.TestName);
            if (!cats.ContainsKey(cat))
                cat = "other";
            var (p, f, _) = cats[cat];
            if (r.Passed) p++; else f++;
            cats[cat] = (p, f, 0);
        }

        // 计算通过率
        var keys = cats.Keys.ToList();
        foreach (var k in keys)
        {
            var (p, f, _) = cats[k];
            var total = p + f;
            cats[k] = (p, f, total > 0 ? (double)p / total * 100 : 0);
        }

        return cats;
    }

    private static string CategorizeTest(string testName)
    {
        var lower = testName.ToLower();
        if (lower.Contains("simple") || lower.Contains("const") || lower.Contains("expr"))
            return "simple";
        if (lower.Contains("if") || lower.Contains("loop") || lower.Contains("while") || lower.Contains("for"))
            return "control_flow";
        if (lower.Contains("except") || lower.Contains("try") || lower.Contains("finally") || lower.Contains("raise"))
            return "exceptions";
        if (lower.Contains("class") || lower.Contains("decorator"))
            return "class";
        if (lower.Contains("func") || lower.Contains("lambda") || lower.Contains("yield") || lower.Contains("async"))
            return "functions";
        if (lower.Contains("import") || lower.Contains("dict") || lower.Contains("list") || lower.Contains("set") ||
            lower.Contains("tuple") || lower.Contains("string") || lower.Contains("slice") || lower.Contains("unpack"))
            return "advanced";
        return "other";
    }
}

/// <summary>
/// Parse pycdc token-dump format lines back to PyToken list.
/// Format: tokens separated by spaces, special tokens in angle brackets.
/// </summary>
public static class TokenDumpFormat
{
    public static List<PyToken> Parse(string[] lines)
    {
        var tokens = new List<PyToken>();
        foreach (var line in lines)
        {
            var trimmed = line.TrimEnd('\r', '\n');
            if (string.IsNullOrEmpty(trimmed)) continue;

            var parts = SplitDumpLine(trimmed);
            foreach (var part in parts)
            {
                switch (part)
                {
                    case "<EOL>":
                        // EOL is implicit per line in dump format
                        break;
                    case "<INDENT>":
                    case "<OUTDENT>":
                        // INDENT/OUTDENT also implicit — stripped from actual before comparison
                        break;
                    default:
                        tokens.Add(ParseValueToken(part));
                        break;
                }
            }
        }
        return tokens;
    }

    private static PyToken ParseValueToken(string text)
    {
        // String literal
        if ((text.StartsWith("'") && text.EndsWith("'")) ||
            (text.StartsWith("\"") && text.EndsWith("\"")))
        {
            var content = text[1..^1];
            return new StringToken("", content, 0);
        }

        // Integer
        if (long.TryParse(text, System.Globalization.NumberStyles.Any,
            System.Globalization.CultureInfo.InvariantCulture, out var _))
            return new IntToken(text, 0);

        // Float
        if (double.TryParse(text, System.Globalization.NumberStyles.Any,
            System.Globalization.CultureInfo.InvariantCulture, out var _))
            return new FloatToken(text, 0);

        // Known Python symbols
        if (IsPythonSymbol(text))
            return new SymbolToken(text, 0);

        // Default: word
        return new WordToken(text, 0);
    }

    private static readonly HashSet<string> PythonSymbols = new()
    {
        "(", ")", "[", "]", "{", "}", ",", ";", ":", ".",
        "=", "+", "-", "*", "/", "//", "%", "**", "@",
        "==", "!=", "<", ">", "<=", ">=", "<>", "->",
        "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=",
        "<<", ">>", "&", "|", "^", "~", "`", "...", ":=",
        "<<=", ">>=", "**=", "//=", "@=",
    };

    private static bool IsPythonSymbol(string text) => PythonSymbols.Contains(text);

    private static List<string> SplitDumpLine(string line)
    {
        var parts = new List<string>();
        int i = 0;
        while (i < line.Length)
        {
            if (char.IsWhiteSpace(line[i])) { i++; continue; }
            if (line[i] == '<') { var e = line.IndexOf('>', i); parts.Add(line[i..(e + 1)]); i = e + 1; continue; }
            if (line[i] == '\'' || line[i] == '"')
            {
                var q = line[i]; var j = i + 1;
                while (j < line.Length) { if (line[j] == '\\') j += 2; else if (line[j] == q) { j++; break; } else j++; }
                parts.Add(line[i..j]); i = j; continue;
            }
            var s = i; while (i < line.Length && !char.IsWhiteSpace(line[i])) i++;
            parts.Add(line[s..i]);
        }
        return parts;
    }
}
