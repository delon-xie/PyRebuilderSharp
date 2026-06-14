using System;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Reactive;
using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Platform.Storage;
using PyRebuilderSharp.Core;
using PyRebuilderSharp.Core.Generators;
using PyRebuilderSharp.Core.Readers;
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
    // 反编译代码变更通知（供View绑定到AvaloniaEdit）
    public event Action<string>? OnCodeChanged;
    /// <summary>
    /// 字节码（dis）变更通知。
    /// </summary>
    public event Action<string>? OnDisasmChanged;
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

    // Public wrapper for drag-drop support in View
    public static string DetectPythonVersionPublic(string filePath)
        => DetectPythonVersion(filePath);

    // -- 文件管理 --
    public ObservableCollection<FileTreeNode> FileTree { get; } = new();

    private FileTreeNode? _selectedNode;
    public FileTreeNode? SelectedNode
    {
        get => _selectedNode;
        set
        {
            System.Console.Error.WriteLine($"[DEBUG] SelectedNode: {value?.Name} path={value?.FullPath}");
            SetProperty(ref _selectedNode, value);
            if (value?.FullPath != null && File.Exists(value.FullPath))
                _ = DecompileFile(value.FullPath);
        }
    }

    private bool _hasFile;
    public bool HasFile
    {
        get => _hasFile;
        set => SetProperty(ref _hasFile, value);
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
        set
        {
            SetProperty(ref _decompiledCode, value);
            // 通知 AvaloniaEdit 更新内容（语法高亮由 View 加载）
            OnCodeChanged?.Invoke(value);
        }
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

    private string _dropHighlightBackground = "#252526";
    public string DropHighlightBackground
    {
        get => _dropHighlightBackground;
        set => SetProperty(ref _dropHighlightBackground, value);
    }

    // -- 崩溃日志 --
    public ObservableCollection<PyRebuilderSharp.Core.Services.CrashEntry> CrashEntries { get; } = new();

    private bool _showCrashLog;
    public bool ShowCrashLog
    {
        get => _showCrashLog;
        set => SetProperty(ref _showCrashLog, value);
    }

    private string _crashCountText = "";
    public string CrashCountText
    {
        get => _crashCountText;
        set => SetProperty(ref _crashCountText, value);
    }

    // -- 显示选项 --
    private bool _showOrphanBlocks = true;
    public bool ShowOrphanBlocks
    {
        get => _showOrphanBlocks;
        set
        {
            if (SetProperty(ref _showOrphanBlocks, value))
                ApplyDisplayFilters();
        }
    }

    private bool _showSummary = true;
    public bool ShowSummary
    {
        get => _showSummary;
        set
        {
            if (SetProperty(ref _showSummary, value))
                ApplyDisplayFilters();
        }
    }

    /// <summary>存储完整的反编译结果（含孤儿块和摘要），用于复选框切换时过滤。</summary>
    private string _fullDecompiledCode = "";

    // -- 命令 --
    public ReactiveCommand<Unit, Unit> OpenFileCommand { get; }
    public ReactiveCommand<Unit, Unit> SaveResultCommand { get; }
    public ReactiveCommand<Unit, Unit> DecompileCommand { get; }
    public ReactiveCommand<Unit, Unit> ShowCrashLogCommand { get; }
    public ReactiveCommand<Unit, Unit> ClearCrashLogCommand { get; }
    public ReactiveCommand<Unit, Unit> CloseCrashLogCommand { get; }

    // -- 顶层窗口引用（由View设置） --
    public Window? TopLevel { get; set; }

    public MainViewModel()
    {
        OpenFileCommand = ReactiveCommand.CreateFromTask(OpenFileAsync);
        SaveResultCommand = ReactiveCommand.CreateFromTask(SaveResultAsync);
        DecompileCommand = ReactiveCommand.CreateFromTask(DecompileCurrentAsync);
        ShowCrashLogCommand = ReactiveCommand.Create(() => { LoadCrashLog(); return System.Reactive.Unit.Default; });
        ClearCrashLogCommand = ReactiveCommand.Create(() => { ClearCrashLog(); return System.Reactive.Unit.Default; });
        CloseCrashLogCommand = ReactiveCommand.Create(() => { ShowCrashLog = false; return System.Reactive.Unit.Default; });
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
        if (TopLevel == null)
        {
            System.Console.Error.WriteLine("[DEBUG] OpenFileAsync: TopLevel is null");
            StatusText = "❌ TopLevel 未初始化，请重启应用";
            return;
        }
        if (TopLevel.StorageProvider == null)
        {
            System.Console.Error.WriteLine("[DEBUG] OpenFileAsync: StorageProvider is null");
            StatusText = "❌ StorageProvider 不可用";
            return;
        }

        // macOS fix: 确保窗口获得焦点后再打开原生对话框
        // 避免 "灰色不可点+嘟嘟声" — 对话框未获得 key window 焦点
        try
        {
            TopLevel.Activate(); // 窗口激活（macOS → bring to front）
            TopLevel.Focus();    // 确保键盘焦点
            TopLevel.BringIntoView(); // 确保窗口可见
        }
        catch { /* 非 macOS 平台忽略 */ }

        // macOS 需要两次事件循环传播：Activate→Focus→延迟→对话框才认 key window
        await System.Threading.Tasks.Task.Delay(100);

        // 使用文件选择器，允许选文件夹或 .pyc
        try
        {
            System.Console.Error.WriteLine("[DEBUG] OpenFileAsync: calling OpenFilePickerAsync");
            var files = await TopLevel.StorageProvider.OpenFilePickerAsync(new FilePickerOpenOptions
        {
            Title = "选择 .pyc 文件或文件夹",
            AllowMultiple = true,
            FileTypeFilter = new[]
            {
                new FilePickerFileType("Python字节码文件 (*.pyc)")
                {
                    Patterns = new[] { "*.pyc" }
                },
                FilePickerFileTypes.All
            }
        });

        System.Console.Error.WriteLine($"[DEBUG] OpenFileAsync: returned {files.Count} files");
        foreach (var file in files)
        {
            var localPath = file.Path.LocalPath;
            System.Console.Error.WriteLine($"[DEBUG] OpenFileAsync: {localPath}");
            if (localPath.EndsWith(".pyc"))
                AddFileToTree(localPath);
        }

        if (files.Count > 0)
        {
            var lastRoot = FileTree.LastOrDefault();
            var target = lastRoot?.Children.LastOrDefault() ?? lastRoot;
            if (target != null) SelectedNode = target;
        }
        }
        catch (Exception ex)
        {
            System.Console.Error.WriteLine($"[DEBUG] OpenFileAsync error: {ex.Message}");
            StatusText = $"❌ 打开失败: {ex.Message}";
        }
    }

    /// <summary>
    /// 添加单个 .pyc 到树根节点。
    /// </summary>
    public void AddFileToTree(string filePath)
    {
        if (!filePath.EndsWith(".pyc") || !File.Exists(filePath)) return;
        var fileName = Path.GetFileName(filePath);
        System.Console.Error.WriteLine($"[DEBUG] AddFileToTree: {fileName}");

        // 去重
        if (FileTree.Any(n => n.FullPath == filePath)) return;

        FileTree.Add(new FileTreeNode
        {
            Name = fileName,
            FullPath = filePath
        });
        HasFile = true;
        System.Console.Error.WriteLine($"[DEBUG]   added, tree now {FileTree.Count} items");
    }

    /// <summary>
    /// 遍历文件夹，将全部 .pyc 按目录层次加入树。
    /// </summary>
    public void AddFolderToTree(string folderPath)
    {
        if (!Directory.Exists(folderPath)) return;
        System.Console.Error.WriteLine($"[DEBUG] AddFolderToTree: {folderPath}");

        var pycFiles = Directory.GetFiles(folderPath, "*.pyc", SearchOption.AllDirectories);
        System.Console.Error.WriteLine($"[DEBUG]   found {pycFiles.Length} .pyc files");

        foreach (var pycPath in pycFiles)
        {
            var relativeDir = Path.GetRelativePath(folderPath, Path.GetDirectoryName(pycPath) ?? "");
            var parts = relativeDir.Split(Path.DirectorySeparatorChar);

            // 在树中查找/创建路径
            var currentLevel = FileTree;
            FileTreeNode? parentDir = null;
            string builtPath = folderPath;

            foreach (var part in parts)
            {
                if (string.IsNullOrEmpty(part) || part == ".") continue;
                builtPath = Path.Combine(builtPath, part);

                var existing = currentLevel.FirstOrDefault(n => n.IsDirectory && n.Name == part);
                if (existing == null)
                {
                    existing = new FileTreeNode { Name = part };
                    currentLevel.Add(existing);
                    // 排序：目录在前
                    var idx = currentLevel.IndexOf(existing);
                    while (idx > 0 && currentLevel[idx - 1].IsDirectory)
                        idx--;
                    if (idx != currentLevel.IndexOf(existing))
                        currentLevel.Move(currentLevel.IndexOf(existing), idx);
                }
                currentLevel = existing.Children;
                parentDir = existing;
            }

            // 添加文件节点
            var fileName = Path.GetFileName(pycPath);
            if (currentLevel.Any(n => n.FullPath == pycPath)) continue;
            currentLevel.Add(new FileTreeNode
            {
                Name = fileName,
                FullPath = pycPath
            });
        }

        // 如果没有按目录归组的文件，直接加到根
        if (pycFiles.Length > 0) HasFile = true;
    }

    // -- 崩溃日志 --
    private void LoadCrashLog()
    {
        CrashEntries.Clear();
        var entries = PyRebuilderSharp.Core.Services.CrashCollector.GetCrashHistory(50);
        foreach (var e in entries)
            CrashEntries.Add(e);
        CrashCountText = $"{entries.Length} 条记录";
        ShowCrashLog = true;
        StatusText = entries.Length > 0
            ? $"📋 加载 {entries.Length} 条崩溃记录"
            : "📋 无崩溃记录";
    }

    private void ClearCrashLog()
    {
        PyRebuilderSharp.Core.Services.CrashCollector.ClearAll();
        CrashEntries.Clear();
        CrashCountText = "0 条记录";
        StatusText = "🗑 崩溃日志已清除";
    }

    /// <summary>
    /// 根据 ShowOrphanBlocks / ShowSummary 复选框状态过滤完整源码。
    /// </summary>
    private void ApplyDisplayFilters()
    {
        if (string.IsNullOrEmpty(_fullDecompiledCode))
        {
            DecompiledCode = "";
            SourceCodeText = "";
            return;
        }

        var full = _fullDecompiledCode;
        bool hideOrphans = !_showOrphanBlocks;
        bool hideSummary = !_showSummary;

        if (!hideOrphans && !hideSummary)
        {
            // 两个都显示 → 直接使用完整源码（DecompiledCode setter 自动触发 OnCodeChanged）
            DecompiledCode = full;
            SourceCodeText = full;
            return;
        }

        // 需要过滤 → 纯内存字符串操作，同步完成
        try
        {
            var lines = full.Replace("\r\n", "\n").Split('\n');
            var result = new System.Collections.Generic.List<string>(lines.Length);
            bool inOrphanBlock = false;

            foreach (var line in lines)
            {
                var trimmed = line.TrimStart();

                // 孤儿块标记
                if (hideOrphans && (trimmed.StartsWith("# orphan @0x") || trimmed.StartsWith("# [Block @0x")))
                {
                    inOrphanBlock = true;
                    continue;
                }

                // 离开孤儿块区域（遇到新的段首或摘要行）
                if (inOrphanBlock && (trimmed.StartsWith("# [SUMMARY]") || trimmed.StartsWith("# [WARN]")))
                {
                    inOrphanBlock = false;
                }

                if (inOrphanBlock)
                {
                    // 孤儿块内的代码行（缩进）→ 跳过
                    if (string.IsNullOrWhiteSpace(line)) continue;
                    if (line.Length > 0 && char.IsWhiteSpace(line[0]))
                        continue;
                    // 非缩进行 → 孤儿块结束
                    inOrphanBlock = false;
                }

                // 摘要行
                if (hideSummary && trimmed.StartsWith("# [SUMMARY]"))
                    continue;

                result.Add(line);
            }

            var filteredCode = string.Join("\n", result);
            DecompiledCode = filteredCode;   // setter 自动触发 OnCodeChanged
            SourceCodeText = filteredCode;
        }
        catch
        {
            // 过滤失败时的安全回退
            DecompiledCode = full;
            SourceCodeText = full;
        }
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

            // 存入完整源码（含孤儿块和摘要），然后根据复选框应用过滤
            _fullDecompiledCode = result.SourceCode;
            ApplyDisplayFilters();
            System.Console.Error.WriteLine($"[DEBUG] SourceCode length={result.SourceCode.Length}");

            // 生成字节码（dis）
            try
            {
                var reader = new PyRebuilderSharp.Core.Readers.PycReader();
                var codeObj = await Task.Run(() => reader.Read(pycData));
                var disasm = PyRebuilderSharp.Core.Generators.DisassemblyGenerator.Generate(codeObj);
                DisasmText = disasm;
                OnDisasmChanged?.Invoke(disasm);  // 通知 TextEditor
                System.Console.Error.WriteLine($"[DEBUG] Disasm length={disasm.Length}");
            }
            catch (Exception disEx)
            {
                System.Console.Error.WriteLine($"[DEBUG] Disassembly failed: {disEx.Message}");
                DisasmText = $"# Disassembly error: {disEx.Message}";
            }

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
            FormattedCode = PyRebuilderSharp.Gui.Services.PythonSyntaxHighlighter.FormatWithLineNumbers(DecompiledCode);
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

    /// <summary>
    /// 显式触发反编译当前选中的文件（由"▶ 反编译"按钮调用）。
    /// </summary>
    private async Task DecompileCurrentAsync()
    {
        System.Console.Error.WriteLine($"[DEBUG] DecompileCurrentAsync called");
        if (SelectedNode?.FullPath != null && File.Exists(SelectedNode.FullPath))
        {
            System.Console.Error.WriteLine($"[DEBUG]   decompiling: {SelectedNode.FullPath}");
            await DecompileFile(SelectedNode.FullPath);
        }
        else
        {
            System.Console.Error.WriteLine($"[DEBUG]   no file selected");
            StatusText = "❌ 请先选择文件";
        }
    }

    // -- 代码显示（供 View 直接绑定） --
    private string _sourceCodeText = "";
    public string SourceCodeText
    {
        get => _sourceCodeText;
        set => SetProperty(ref _sourceCodeText, value);
    }

    private string _disasmText = "";
    public string DisasmText
    {
        get => _disasmText;
        set => SetProperty(ref _disasmText, value);
    }

    private async Task SaveResultAsync()
    {
        if (TopLevel == null || string.IsNullOrEmpty(DecompiledCode)) return;

        var file = await TopLevel.StorageProvider.SaveFilePickerAsync(new FilePickerSaveOptions
        {
            Title = "保存反编译结果",
            DefaultExtension = ".py",
            SuggestedFileName = SelectedNode != null
                ? Path.GetFileNameWithoutExtension(SelectedNode.Name) + "_decompiled.py"
                : "output.py"
        });

        if (file != null)
        {
            await File.WriteAllTextAsync(file.Path.LocalPath, DecompiledCode);
            StatusText = $"💾 已保存到 {file.Name}";
        }
    }
}
