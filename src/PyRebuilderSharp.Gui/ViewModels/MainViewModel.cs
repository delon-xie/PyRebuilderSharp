using System;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Reactive;
using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Platform.Storage;
using PyRebuilderSharp.Core;
using ReactiveUI;

namespace PyRebuilderSharp.Gui.ViewModels;

/// <summary>
/// 反编译统计信息模型。
/// </summary>
public class DecompileStats
{
    public int TotalBlocks { get; set; }
    public int FailedBlocks { get; set; }
    public int TotalFunctions { get; set; }
    public double SuccessRate => TotalBlocks > 0
        ? (double)(TotalBlocks - FailedBlocks) / TotalBlocks * 100
        : 0;
    public TimeSpan Elapsed { get; set; }
    public string Summary => $"块: {TotalBlocks} | ❌失败: {FailedBlocks} ({SuccessRate:F1}%) | 耗时: {Elapsed.TotalMilliseconds:F0}ms";
}

/// <summary>
/// 文件项。
/// </summary>
public class FileItem
{
    public string Name { get; set; } = "";
    public string FullPath { get; set; } = "";
    public string PythonVersion { get; set; } = "";
    public string Size 
    {
        get
        {
            try
            {
                var len = new FileInfo(FullPath).Length;
                return len switch
                {
                    < 1024 => $"{len} B",
                    < 1024 * 1024 => $"{len / 1024} KB",
                    var b => $"{b / (1024.0 * 1024):F1} MB"
                };
            }
            catch { return "?"; }
        }
    }
}

/// <summary>
/// 主窗口ViewModel。
/// </summary>
public class MainViewModel : ViewModelBase
{
    private static readonly byte[][] KnownMagics = {
        [0x03, 0xF3, 0x0D, 0x0A],  // 2.7
        [0x17, 0x0D, 0x0D, 0x0A],  // 3.5
        [0x33, 0x0D, 0x0D, 0x0A],  // 3.6
        [0x42, 0x0D, 0x0D, 0x0A],  // 3.7
        [0x55, 0x0D, 0x0D, 0x0A],  // 3.8
        [0x61, 0x0D, 0x0D, 0x0A],  // 3.9
        [0x6F, 0x0D, 0x0D, 0x0A],  // 3.10
        [0xA0, 0x0D, 0x0D, 0x0A],  // 3.11
        [0xC0, 0x0D, 0x0D, 0x0A],  // 3.12
    };

    private static readonly string[] VersionNames = {
        "2.7", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12"
    };

    private static string DetectPythonVersion(string filePath)
    {
        try
        {
            using var fs = new FileStream(filePath, FileMode.Open, FileAccess.Read);
            var magic = new byte[4];
            if (fs.Read(magic, 0, 4) < 4) return "?";
            for (int i = 0; i < KnownMagics.Length; i++)
                if (magic.SequenceEqual(KnownMagics[i]))
                    return VersionNames[i];
            return $"0x{magic[0]:X2}{magic[1]:X2}{magic[2]:X2}{magic[3]:X2}";
        }
        catch { return "?"; }
    }

    // -- 文件管理 --
    public ObservableCollection<FileItem> Files { get; } = new();

    private FileItem? _selectedFile;
    public FileItem? SelectedFile
    {
        get => _selectedFile;
        set
        {
            SetProperty(ref _selectedFile, value);
            if (value != null)
                _ = DecompileFile(value.FullPath);
        }
    }

    // -- 当前文件信息 --
    private string _currentFileName = "";
    public string CurrentFileName
    {
        get => _currentFileName;
        set => SetProperty(ref _currentFileName, value);
    }

    private string _blockSummary = "";
    public string BlockSummary
    {
        get => _blockSummary;
        set => SetProperty(ref _blockSummary, value);
    }

    // -- 反编译控制 --
    private string _pythonVersion = "就绪";
    public string PythonVersion
    {
        get => _pythonVersion;
        set => SetProperty(ref _pythonVersion, value);
    }

    private bool _isDecompiling;
    public bool IsDecompiling
    {
        get => _isDecompiling;
        set => SetProperty(ref _isDecompiling, value);
    }

    // -- 结果 --
    private string _decompiledCode = "";
    public string DecompiledCode
    {
        get => _decompiledCode;
        set => SetProperty(ref _decompiledCode, value);
    }

    private string _formattedCode = "";
    public string FormattedCode
    {
        get => _formattedCode;
        set => SetProperty(ref _formattedCode, value);
    }

    private string _statsText = "";
    public string StatsText
    {
        get => _statsText;
        set => SetProperty(ref _statsText, value);
    }

    private string _statusText = "就绪";
    public string StatusText
    {
        get => _statusText;
        set => SetProperty(ref _statusText, value);
    }

    // -- 命令 --
    public ReactiveCommand<Unit, Unit> OpenFileCommand { get; }
    public ReactiveCommand<Unit, Unit> SaveResultCommand { get; }

    // -- 顶层窗口引用（由View设置） --
    public Window? TopLevel { get; set; }

    public MainViewModel()
    {
        OpenFileCommand = ReactiveCommand.CreateFromTask(OpenFileAsync);
        SaveResultCommand = ReactiveCommand.CreateFromTask(SaveResultAsync);
        PythonVersion = "🔍 选择 .pyc 文件开始反编译";
    }

    private string FormatCode(string code)
    {
        if (string.IsNullOrEmpty(code))
            return "(空)";

        // 格式化代码以增强可读性：
        // 1. 添加行号
        // 2. 保留原始缩进
        var lines = code.Split('\n');
        var padWidth = lines.Length.ToString().Length;
        var result = new System.Text.StringBuilder();

        for (int i = 0; i < lines.Length; i++)
        {
            var lineNum = (i + 1).ToString().PadLeft(padWidth);
            var line = lines[i];

            // 注释行（包括失败块兜底）— 添加行号标记
            if (line.TrimStart().StartsWith("#"))
            {
                result.AppendLine($"  {lineNum}│{line}");
            }
            else
            {
                result.AppendLine($"  {lineNum}│{line}");
            }
        }

        return result.ToString();
    }

    private string DetectAndFormatVersion(string filePath)
    {
        try
        {
            using var fs = new FileStream(filePath, FileMode.Open, FileAccess.Read);
            var magic = new byte[4];
            if (fs.Read(magic, 0, 4) < 4) return "未知版本";
            
            // Determine Python version
            int majorVer = 0;
            string verStr = "未知";
            for (int i = 0; i < KnownMagics.Length; i++)
            {
                if (magic.SequenceEqual(KnownMagics[i]))
                {
                    verStr = VersionNames[i];
                    break;
                }
            }

            var flags = 0;
            if (magic[0] >= 0x42) // 3.7+
            {
                var header = new byte[12];
                fs.Read(header, 0, 12);
                // flags is at first 4 bytes of header
            }

            return verStr;
        }
        catch { return "?"; }
    }

    private async Task OpenFileAsync()
    {
        if (TopLevel == null) return;

        var files = await TopLevel.StorageProvider.OpenFilePickerAsync(new FilePickerOpenOptions
        {
            Title = "选择 .pyc 文件",
            AllowMultiple = true,
            FileTypeFilter = new[]
            {
                new FilePickerFileType("Python字节码文件")
                {
                    Patterns = new[] { "*.pyc" }
                }
            }
        });

        foreach (var file in files)
        {
            var localPath = file.Path.LocalPath;
            var pyVersion = DetectPythonVersion(localPath);
            Files.Add(new FileItem
            {
                Name = Path.GetFileName(file.Name),
                FullPath = localPath,
                PythonVersion = $"🐍 {pyVersion}"
            });
        }

        if (files.Count > 0)
            SelectedFile = Files.Last();
    }

    private async Task DecompileFile(string filePath)
    {
        if (!File.Exists(filePath)) return;

        IsDecompiling = true;
        StatusText = "⏳ 反编译中...";
        PythonVersion = "⏳ 读取中...";

        try
        {
            var pyVersion = DetectPythonVersion(filePath);
            PythonVersion = $"🐍 {pyVersion}";
            CurrentFileName = Path.GetFileName(filePath);

            var pycData = await File.ReadAllBytesAsync(filePath);
            var decompiler = new Decompiler();
            var result = await Task.Run(() => decompiler.DecompileWithStats(pycData));

            DecompiledCode = result.SourceCode;
            FormattedCode = FormatCode(result.SourceCode);

            var successRate = result.TotalBlocks > 0
                ? (double)(result.TotalBlocks - result.FailedBlocks) / result.TotalBlocks * 100
                : 0;

            var blockEmoji = result.FailedBlocks > 0 ? "⚠️" : "✅";
            BlockSummary = $"{blockEmoji} {result.TotalBlocks} 块 | ❌{result.FailedBlocks} 失败 | {result.Elapsed.TotalMilliseconds:F0}ms";

            if (result.FailedBlocks > 0)
                StatsText = $"完成 | {result.TotalBlocks} 块, {result.FailedBlocks} 失败 ({successRate:F1}% 成功)";
            else
                StatsText = $"✅ 完全成功 | {result.TotalBlocks} 块反编译";

            var funcCount = CountFunctions(result.SourceCode);
            StatusText = $"✅ 完成 — {funcCount} 个函数, {result.TotalBlocks} 基本块, {result.Elapsed.TotalMilliseconds:F0}ms";
        }
        catch (Exception ex)
        {
            DecompiledCode = $"# 反编译失败\n# {ex.GetType().Name}: {ex.Message}";
            FormattedCode = FormatCode(DecompiledCode);
            StatusText = $"❌ 失败: {ex.Message}";
            StatsText = "失败";
        }
        finally
        {
            IsDecompiling = false;
        }
    }

    private int CountFunctions(string code)
    {
        int count = 0;
        foreach (var line in code.Split('\n'))
        {
            var trimmed = line.TrimStart();
            if (trimmed.StartsWith("def ") || trimmed.StartsWith("async def "))
                count++;
        }
        return count;
    }

    private async Task SaveResultAsync()
    {
        if (TopLevel == null || string.IsNullOrEmpty(DecompiledCode)) return;

        var file = await TopLevel.StorageProvider.SaveFilePickerAsync(new FilePickerSaveOptions
        {
            Title = "保存反编译结果",
            DefaultExtension = ".py",
            SuggestedFileName = SelectedFile != null
                ? Path.GetFileNameWithoutExtension(SelectedFile.Name) + "_decompiled.py"
                : "output.py"
        });

        if (file != null)
        {
            await File.WriteAllTextAsync(file.Path.LocalPath, DecompiledCode);
            StatusText = $"💾 已保存到 {file.Name}";
        }
    }
}
