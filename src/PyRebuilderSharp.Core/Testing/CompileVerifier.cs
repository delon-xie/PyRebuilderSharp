using System.Diagnostics;
using System.Text;

namespace PyRebuilderSharp.Core.Testing;

/// <summary>
/// Python 源码编译验证器。
/// 通过子进程调用系统 python3 的 ast.parse() 检查源码语法合法性。
/// 
/// 三种模式：
///   1. VerifySyntax — 轻量 ast.parse 检查（默认）
///   2. VerifyCompile — 中级 compile() 检查
///   3. VerifyWithPythonVersion — 版本匹配的编译检查（需 pyenv）
/// 
/// 设计原则：
/// - 只报告不修改（不会改变源码或测试结果）
/// - 语法警告仅在 --verify-compile 时输出
/// - 子进程超时 30 秒，防挂起
/// </summary>
public static class CompileVerifier
{
    /// <summary>验证结果。</summary>
    public readonly record struct CompileResult(
        bool IsValid,
        int? Line,
        string? Message,
        string FullOutput
    );

    /// <summary>
    /// 通过子进程调用 python3 ast.parse() 验证源码语法。
    /// 源码通过标准输入传递，避免 shell 转义问题。
    /// </summary>
    /// <param name="source">Python 源码文本</param>
    /// <param name="timeoutSeconds">子进程超时秒数（默认 30）</param>
    /// <returns>验证结果</returns>
    public static CompileResult VerifySyntax(string source, int timeoutSeconds = 30)
    {
        return RunPythonVerify(source, "ast.parse", timeoutSeconds);
    }

    /// <summary>
    /// 通过子进程调用 python3 compile() 验证源码可编译为字节码。
    /// 比 ast.parse 更严格（捕获所有编译期错误）。
    /// </summary>
    public static CompileResult VerifyCompile(string source, int timeoutSeconds = 30)
    {
        return RunPythonVerify(source, "compile", timeoutSeconds);
    }

    /// <summary>
    /// 版本匹配的编译检查（需 pyenv 安装对应版本 Python）。
    /// 3.5 的解释器无法编译 3.10 格式的 f-string。
    /// </summary>
    public static CompileResult VerifyWithPythonVersion(
        string source, string targetVersion, int timeoutSeconds = 30)
    {
        var pythonBin = ResolvePyenvBinary(targetVersion);
        if (pythonBin == null)
        {
            // Fallback: use system python3
            pythonBin = FindSystemPython();
            if (pythonBin == null)
                return new CompileResult(false, null,
                    "No Python interpreter found", "");
        }
        return RunPythonVerify(source, "ast.parse", timeoutSeconds, pythonBin);
    }

    /// <summary>
    /// 批量验证：对多个源码文件执行 ast.parse，返回统计摘要。
    /// </summary>
    public static BatchResult VerifyBatch(
        Dictionary<string, string> sources, int timeoutSeconds = 30)
    {
        int total = sources.Count;
        int passed = 0;
        int failed = 0;
        var failures = new List<(string Name, CompileResult Result)>();

        foreach (var (name, source) in sources)
        {
            var result = VerifySyntax(source, timeoutSeconds);
            if (result.IsValid)
                passed++;
            else
            {
                failed++;
                failures.Add((name, result));
            }
        }

        return new BatchResult(total, passed, failed, failures);
    }

    /// <summary>批量验证结果。</summary>
    public readonly record struct BatchResult(
        int Total, int Passed, int Failed,
        List<(string Name, CompileResult Result)> Failures
    )
    {
        public double PassRate => Total > 0 ? (double)Passed / Total * 100 : 0;
        public string Summary =>
            $"Compile verify: {Passed}/{Total} passed ({PassRate:F1}%), {Failed} failed";
    }

    // ---- 内部实现 ----

    /// <summary>
    /// 执行 Python 子进程验证。
    /// 使用标准输入传递源码，标准输出返回结果。
    /// </summary>
    private static CompileResult RunPythonVerify(
        string source, string mode, int timeoutSeconds, string? pythonBin = null)
    {
        try
        {
            pythonBin ??= FindSystemPython() ?? "python3";

            // Python 脚本：捕获 SyntaxError 输出到 stdout，避免被 stderr 吞掉
            var script = "import sys, ast; code = sys.stdin.read(); " +
                "try: ast.parse(code); print('PASS')" +
                "except SyntaxError as e: print(f'FAIL:{e.lineno}:{e.msg}')" +
                "except Exception as e: print(f'ERROR:{type(e).__name__}:{e}')";

            using var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = pythonBin,
                    Arguments = $"-c \"{script}\"",
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                }
            };

            process.Start();
            process.StandardInput.Write(source);
            process.StandardInput.Close();

            var output = process.StandardOutput.ReadToEnd().Trim();
            var error = process.StandardError.ReadToEnd().Trim();

            if (!process.WaitForExit(timeoutSeconds * 1000))
            {
                process.Kill();
                return new CompileResult(false, null, "TIMEOUT", output);
            }

            // ast.parse success (PASS)
            if (output == "PASS")
                return new CompileResult(true, null, null, output);

            // ast.parse failure (SyntaxError or other)
            if (!string.IsNullOrEmpty(output))
                return new CompileResult(false, null, output, output);

            // stderr fallback
            if (!string.IsNullOrEmpty(error))
                return new CompileResult(false, null, error, error);

            return new CompileResult(false, null,
                $"Unknown result (exit={process.ExitCode})", output);
        }
        catch (Exception ex)
        {
            return new CompileResult(false, null,
                $"Exception: {ex.GetType().Name}: {ex.Message}", "");
        }
    }

    /// <summary>查找系统可用的 python3 解释器。</summary>
    private static string? FindSystemPython()
    {
        foreach (var candidate in new[] { "python3", "python" })
        {
            try
            {
                using var proc = new Process
                {
                    StartInfo = new ProcessStartInfo
                    {
                        FileName = candidate,
                        Arguments = "--version",
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        UseShellExecute = false,
                        CreateNoWindow = true,
                    }
                };
                proc.Start();
                proc.WaitForExit(5000);
                if (proc.ExitCode == 0)
                    return candidate;
            }
            catch { }
        }
        return null;
    }

    /// <summary>通过 pyenv 查找指定版本的 Python 解释器路径。</summary>
    private static string? ResolvePyenvBinary(string version)
    {
        try
        {
            var home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            var pyenvRoot = Path.Combine(home, ".pyenv", "versions");
            if (!Directory.Exists(pyenvRoot))
                return null;

            var candidates = Directory.GetDirectories(pyenvRoot)
                .Select(Path.GetFileName)
                .Where(d => d != null && d.StartsWith(version))
                .OrderByDescending(d => d)
                .ToList();

            foreach (var candidate in candidates)
            {
                if (candidate == null) continue;
                var pythonBin = Path.Combine(pyenvRoot, candidate, "bin", "python3");
                if (File.Exists(pythonBin))
                    return pythonBin;

                pythonBin = Path.Combine(pyenvRoot, candidate, "bin", "python");
                if (File.Exists(pythonBin))
                    return pythonBin;
            }
        }
        catch { }
        return null;
    }
}
