using System;

namespace PyRebuilderSharp.Core.Diagnostics;

/// <summary>
/// 全局诊断日志门控。当 Verbose=false（默认）时，所有调试 Console.Error 输出被抑制。
/// CLI 启动时设置 Diag.Verbose = Options.VerboseErrors。
/// </summary>
internal static class Diag
{
    /// <summary>是否启用详细诊断输出。默认 false（抑制）。</summary>
    internal static bool Verbose { get; set; } = false;

    /// <summary>条件输出到 Console.Error。</summary>
    internal static void WriteLine(string message)
    {
        if (Verbose)
            Console.Error.WriteLine(message);
    }
}
