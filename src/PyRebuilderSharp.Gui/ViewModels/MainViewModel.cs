using System;
using System.Collections.ObjectModel;
using System.IO;
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
    public string Summary => $"块: {TotalBlocks} | 失败: {FailedBlocks} ({SuccessRate:F1}%) | 耗时: {Elapsed.TotalMilliseconds:F0}ms";
}

/// <summary>
/// 文件项。
/// </summary>
public class FileItem
{
    public string Name { get; set; } = "";
    public string FullPath { get; set; } = "";
    public string Size => new FileInfo(FullPath).Length switch
    {
        < 1024 => $"{new FileInfo(FullPath).Length} B",
        < 1024 * 1024 => $"{new FileInfo(FullPath).Length / 1024} KB",
        var b => $"{b / (1024 * 1024):F1} MB"
    };
}

/// <summary>
/// 主窗口ViewModel。
/// </summary>
public class MainViewModel : ViewModelBase
{
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

    // -- 反编译控制 --
    private string _pythonVersion = "3.10";
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

    private string _statsText = "就绪";
    public string StatsText
    {
        get => _statsText;
        set => SetProperty(ref _statsText, value);
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
            Files.Add(new FileItem
            {
                Name = Path.GetFileName(file.Name),
                FullPath = file.Path.LocalPath
            });
        }

        if (files.Count > 0)
            SelectedFile = Files.Last();
    }

    private async Task DecompileFile(string filePath)
    {
        if (!File.Exists(filePath)) return;

        IsDecompiling = true;
        StatsText = "反编译中...";

        try
        {
            var pycData = await File.ReadAllBytesAsync(filePath);
            var decompiler = new Decompiler();
            var result = await Task.Run(() => decompiler.DecompileWithStats(pycData));

            DecompiledCode = result.SourceCode;
            var successRate = result.TotalBlocks > 0
                ? (double)(result.TotalBlocks - result.FailedBlocks) / result.TotalBlocks * 100
                : 0;
            StatsText = $"完成 | 块: {result.TotalBlocks} 失败: {result.FailedBlocks} ({successRate:F1}%) | 耗时: {result.Elapsed.TotalMilliseconds:F0}ms";
        }
        catch (Exception ex)
        {
            DecompiledCode = $"# 反编译失败\n# {ex.Message}";
            StatsText = "失败";
        }
        finally
        {
            IsDecompiling = false;
        }
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
        }
    }
}
