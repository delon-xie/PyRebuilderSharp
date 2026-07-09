using Avalonia;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Threading;
using PyRebuilderSharp.Gui.Services;
using PyRebuilderSharp.Gui.ViewModels;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace PyRebuilderSharp.Gui.Views;

public partial class MainWindow : Window
{
    /// <summary>防 Ping-Pong 锁：双向滚动同步时防止互相触发。</summary>
    private bool _isSyncingScroll;

    /// <summary>语法高亮调试日志开关（设为 true 启用）</summary>
    private static bool EnableHighlightLog => false;

    /// <summary>语法高亮调试日志路径（与 GUI 程序同目录）</summary>
    private static readonly string HighlightLogPath = Path.Combine(
        AppContext.BaseDirectory, "PyRebuilder_highlight_log.txt");

    /// <summary>写入调试日志（同步追加，线程安全）</summary>
    private static void Log(string msg)
    {
        if (!EnableHighlightLog) return;
        try
        {
            var line = $"[{DateTime.Now:HH:mm:ss.fff}] {msg}";
            System.Console.Error.WriteLine(line);
            File.AppendAllText(HighlightLogPath, line + "\n");
        }
        catch { }
    }

    public MainWindow()
    {
        InitializeComponent();

        System.Console.Error.WriteLine($"[DEBUG] InitOK SourceBlock={(SourceBlock != null)} DisasmBlock={(DisasmBlock != null)} FileTreeBorder={(FileTreeBorder != null)}");

        // 文件树拖放（Avalonia 11 需在代码中设置 AllowDrop）
        if (FileTreeBorder != null)
        {
            DragDrop.SetAllowDrop(FileTreeBorder, true);
            FileTreeBorder.AddHandler(DragDrop.DragEnterEvent, OnFileTreeDragEnter);
            FileTreeBorder.AddHandler(DragDrop.DragLeaveEvent, OnFileTreeDragLeave);
            FileTreeBorder.AddHandler(DragDrop.DropEvent, OnFileTreeDrop);
        }

        // 窗口级拖放（兜底）
        DragDrop.SetAllowDrop(this, true);
        AddHandler(DragDrop.DragEnterEvent, OnDragEnter);
        AddHandler(DragDrop.DragOverEvent, OnDragOver);
        AddHandler(DragDrop.DropEvent, OnDrop);

        // ===== 双向滚动同步 =====
        if (DisasmScroll != null && SourceScroll != null)
        {
            System.Console.Error.WriteLine("[DEBUG] Wire scroll sync: DisasmScroll <-> SourceScroll");
            DisasmScroll.ScrollChanged += OnScrollSync;
            SourceScroll.ScrollChanged += OnScrollSync;
        }
        else
        {
            System.Console.Error.WriteLine("[DEBUG] Scroll sync NOT wired — one or both ScrollViewers missing");
        }

        // DataContextChanged → TopLevel + 事件
        DataContextChanged += (_, _) =>
        {
            if (DataContext is not MainViewModel vm) return;
            System.Console.Error.WriteLine("[DEBUG] DataContextChanged: wiring VM");
            vm.TopLevel = this;

            // 源码面板：Highlight 在后台线程构建 InlineCollection，UI 线程仅赋值
            vm.OnCodeChanged += code =>
            {
                if (SourceBlock == null) { Log("[HL] SourceBlock null in OnCodeChanged"); return; }
                Log($"[HL] OnCodeChanged fired, code length={code?.Length ?? 0}");
                if (string.IsNullOrEmpty(code))
                {
                    SourceBlock.Text = "";
                    SourceBlock.Inlines = new Avalonia.Controls.Documents.InlineCollection();
                    Log("[HL] Cleared (empty code)");
                    return;
                }
                var captured = code;
                // Run 对象必须在 UI 线程创建，所以高亮在 UI 线程同步执行
                try
                {
                    Log("[HL] Starting highlight...");
                    var sw = System.Diagnostics.Stopwatch.StartNew();
                    var segments = PythonSyntaxHighlight.Highlight(captured);
                    sw.Stop();
                    Log($"[HL] Highlight parse complete: {segments.Count} segs, {sw.ElapsedMilliseconds}ms");
                    var inlines = new Avalonia.Controls.Documents.InlineCollection();
                    foreach (var (text, color) in segments)
                        inlines.Add(new Avalonia.Controls.Documents.Run(text)
                            { Foreground = new Avalonia.Media.SolidColorBrush(Avalonia.Media.Color.Parse(color)) });
                    SourceBlock.Text = "";
                    SourceBlock.Inlines = inlines;
                    Log($"[HL] Inlines set! {inlines.Count} runs");
                }
                catch (System.Exception ex)
                {
                    Log($"[HL] Error: {ex.GetType().Name}: {ex.Message}");
                    var fallback = new Avalonia.Controls.Documents.InlineCollection();
                    fallback.Add(new Avalonia.Controls.Documents.Run(captured)
                        { Foreground = new Avalonia.Media.SolidColorBrush(Avalonia.Media.Colors.White) });
                    SourceBlock.Inlines = fallback;
                }
            };

            // 字节码面板：同上
            vm.OnDisasmChanged += code =>
            {
                if (DisasmBlock == null) { Log("[HL] DisasmBlock null in OnDisasmChanged"); return; }
                Log($"[HL] OnDisasmChanged fired, code length={code?.Length ?? 0}");
                if (string.IsNullOrEmpty(code))
                {
                    DisasmBlock.Text = "";
                    DisasmBlock.Inlines = new Avalonia.Controls.Documents.InlineCollection();
                    Log("[HL] Disasm cleared (empty code)");
                    return;
                }
                var captured = code;
                try
                {
                    var sw = System.Diagnostics.Stopwatch.StartNew();
                    var segments = DisasmSyntaxHighlight.Highlight(captured);
                    sw.Stop();
                    Log($"[HL] Disasm highlight parse: {segments.Count} segs, {sw.ElapsedMilliseconds}ms");
                    var inlines = new Avalonia.Controls.Documents.InlineCollection();
                    foreach (var (text, color) in segments)
                        inlines.Add(new Avalonia.Controls.Documents.Run(text)
                            { Foreground = new Avalonia.Media.SolidColorBrush(Avalonia.Media.Color.Parse(color)) });
                    DisasmBlock.Text = "";
                    DisasmBlock.Inlines = inlines;
                    Log($"[HL] Disasm Inlines set! {inlines.Count} runs");
                }
                catch (System.Exception ex)
                {
                    Log($"[HL] Disasm error: {ex.GetType().Name}: {ex.Message}");
                    var fallback = new Avalonia.Controls.Documents.InlineCollection();
                    fallback.Add(new Avalonia.Controls.Documents.Run(captured)
                        { Foreground = new Avalonia.Media.SolidColorBrush(Avalonia.Media.Colors.White) });
                    DisasmBlock.Inlines = fallback;
                }
            };

            // 附加日志到 ViewModel 的事件
            vm.PropertyChanged += (_, e) =>
            {
                if (e.PropertyName == nameof(MainViewModel.DecompiledCode))
                    Log($"[HL] ViewModel.DecompiledCode changed");
            };
        };
    }

    // ============================================================
    // 双向滚动同步：比例跟踪（字节码 200 行 / 源码 150 行也能对齐）
    // ============================================================
    private void OnScrollSync(object? sender, ScrollChangedEventArgs e)
    {
        if (_isSyncingScroll) return;
        if (sender == null || DisasmScroll == null || SourceScroll == null) return;

        _isSyncingScroll = true;
        try
        {
            var source = (ScrollViewer)sender;
            var target = (source == DisasmScroll) ? SourceScroll : DisasmScroll;

            var sourceRange = source.Extent.Height - source.Viewport.Height;
            var targetRange = target.Extent.Height - target.Viewport.Height;

            // 任一方向不可滚动 → 不处理
            if (sourceRange <= 0 || targetRange <= 0) return;

            // 按比例映射：source 50% → target 50%
            double ratio = source.Offset.Y / sourceRange;
            double targetY = ratio * targetRange;

            target.Offset = new Vector(0, targetY);
        }
        finally
        {
            _isSyncingScroll = false;
        }
    }

    // ============================================================
    // 拖放处理（无变化）
    // ============================================================

    private void OnDragEnter(object? sender, DragEventArgs e)
    {
        e.DragEffects = DragDropEffects.Copy;
    }

    private void OnDragOver(object? sender, DragEventArgs e)
    {
        e.DragEffects = DragDropEffects.Copy;
    }

    private void OnDrop(object? sender, DragEventArgs e)
    {
        ProcessDrop(e);
    }

    /// <summary>文件树拖放进入 — 高亮</summary>
    private void OnFileTreeDragEnter(object? sender, DragEventArgs e)
    {
        if (DataContext is MainViewModel vm)
            vm.DropHighlightBackground = "#2a2d35";
    }

    /// <summary>文件树拖放离开 — 取消高亮</summary>
    private void OnFileTreeDragLeave(object? sender, DragEventArgs e)
    {
        if (DataContext is MainViewModel vm)
            vm.DropHighlightBackground = "#252526";
    }

    /// <summary>文件树拖放放下</summary>
    private void OnFileTreeDrop(object? sender, DragEventArgs e)
    {
        if (DataContext is MainViewModel vm)
            vm.DropHighlightBackground = "#252526";
        ProcessDrop(e);
    }

    /// <summary>处理拖放 — 支持文件/文件夹/多选</summary>
    private void ProcessDrop(DragEventArgs e)
    {
        if (DataContext is not MainViewModel vm) return;
        if (e.Data is not IDataObject dataObj) return;

        var files = dataObj.GetFiles();
        if (files == null) return;

        System.Console.Error.WriteLine($"[DEBUG] ProcessDrop: {files.Count()} items");

        foreach (var file in files)
        {
            var path = file.Path.LocalPath;
            System.Console.Error.WriteLine($"[DEBUG]   item: {path} isDir={Directory.Exists(path)}");

            if (Directory.Exists(path))
            {
                vm.AddFolderToTree(path);
            }
            else if (path.EndsWith(".pyc") && File.Exists(path))
            {
                vm.AddFileToTree(path);
            }
        }

        // 选中最后添加的文件
        var lastRoot = vm.FileTree.LastOrDefault();
        if (lastRoot != null)
        {
            var lastChild = lastRoot.Children.Count > 0 ? lastRoot.Children.Last() : lastRoot;
            vm.SelectedNode = lastChild;
        }
    }
}
