using System;
using System.IO;
using System.Text.Json;

namespace PyRebuilderSharp.Core.Services;

/// <summary>
/// 崩溃收集器 — 在反编译器未捕获的异常发生时记录到 JSON。
/// 输出路径：~/.pyrebuilder/crashes/xxx.json
/// </summary>
public static class CrashCollector
{
    private static readonly string CrashDir;
    private static readonly object Lock = new();

    static CrashCollector()
    {
        CrashDir = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
            ".pyrebuilder", "crashes");
        try { Directory.CreateDirectory(CrashDir); } catch { }
    }

    /// <summary>
    /// 记录一次崩溃。
    /// </summary>
    /// <param name="context">反编译上下文（如文件名、版本）</param>
    /// <param name="ex">异常</param>
    /// <param name="pycSize">原始 .pyc 文件大小</param>
    /// <returns>JSON 文件路径，写入失败时返回 null</returns>
    public static string? RecordCrash(CrashContext context, Exception ex, int pycSize = 0)
    {
        try
        {
            var entry = new CrashEntry
            {
                Timestamp = DateTime.UtcNow,
                PythonVersion = context.PythonVersion ?? "unknown",
                FileName = context.FileName ?? "unknown",
                PycSize = pycSize,
                ExceptionType = ex.GetType().FullName ?? "?",
                ExceptionMessage = ex.Message,
                StackTrace = ex.StackTrace ?? "",
                InnerException = ex.InnerException != null
                    ? $"{ex.InnerException.GetType().Name}: {ex.InnerException.Message}"
                    : null
            };

            var timestamp = DateTime.UtcNow.ToString("yyyyMMdd_HHmmss_fff");
            var fileName = $"crash_{timestamp}.json";
            var filePath = Path.Combine(CrashDir, fileName);

            lock (Lock)
            {
                var json = JsonSerializer.Serialize(entry, new JsonSerializerOptions
                {
                    WriteIndented = true
                });
                File.WriteAllText(filePath, json);
            }

            return filePath;
        }
        catch
        {
            return null;
        }
    }

    /// <summary>
    /// 获取所有崩溃记录（按时间倒序）。
    /// </summary>
    public static CrashEntry[] GetCrashHistory(int maxCount = 10)
    {
        try
        {
            if (!Directory.Exists(CrashDir))
                return Array.Empty<CrashEntry>();

            var files = Directory.GetFiles(CrashDir, "crash_*.json")
                .OrderByDescending(f => f)
                .Take(maxCount)
                .ToArray();

            var results = new List<CrashEntry>();
            foreach (var file in files)
            {
                try
                {
                    var json = File.ReadAllText(file);
                    var entry = JsonSerializer.Deserialize<CrashEntry>(json);
                    if (entry != null) results.Add(entry);
                }
                catch { }
            }
            return results.ToArray();
        }
        catch
        {
            return Array.Empty<CrashEntry>();
        }
    }

    /// <summary>
    /// 清除所有崩溃记录。
    /// </summary>
    public static void ClearAll()
    {
        try
        {
            if (!Directory.Exists(CrashDir)) return;
            foreach (var file in Directory.GetFiles(CrashDir, "crash_*.json"))
                File.Delete(file);
        }
        catch { }
    }
}

/// <summary>
/// 崩溃上下文 — 调用方提供的信息。
/// </summary>
public class CrashContext
{
    public string? FileName { get; set; }
    public string? PythonVersion { get; set; }
    public string? SourceSnippet { get; set; }
}

/// <summary>
/// 崩溃记录条目。
/// </summary>
public class CrashEntry
{
    public DateTime Timestamp { get; set; }
    public string PythonVersion { get; set; } = "";
    public string FileName { get; set; } = "";
    public int PycSize { get; set; }
    public string ExceptionType { get; set; } = "";
    public string ExceptionMessage { get; set; } = "";
    public string StackTrace { get; set; } = "";
    public string? InnerException { get; set; }
}
