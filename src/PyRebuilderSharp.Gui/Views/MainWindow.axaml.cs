using Avalonia.Controls;
using Avalonia.Input;
using PyRebuilderSharp.Gui.Services;
using PyRebuilderSharp.Gui.ViewModels;
using System.IO;
using System.Linq;

namespace PyRebuilderSharp.Gui.Views;

public partial class MainWindow : Window
{
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

        // DataContextChanged → TopLevel + 事件
        DataContextChanged += (_, _) =>
        {
            if (DataContext is not MainViewModel vm) return;
            System.Console.Error.WriteLine("[DEBUG] DataContextChanged: wiring VM");
            vm.TopLevel = this;

            // 源码面板：Highlight 直接在 UI 线程执行（反编译已在 Task.Run 中，UI 线程空闲）
            vm.OnCodeChanged += code =>
            {
                if (SourceBlock == null) return;
                if (string.IsNullOrEmpty(code))
                {
                    SourceBlock.Inlines = null;
                    return;
                }
                SourceBlock.Inlines = PythonSyntaxHighlight.Highlight(code);
            };

            // 字节码面板：同上
            vm.OnDisasmChanged += code =>
            {
                if (DisasmBlock == null) return;
                if (string.IsNullOrEmpty(code))
                {
                    DisasmBlock.Inlines = null;
                    return;
                }
                DisasmBlock.Inlines = DisasmSyntaxHighlight.Highlight(code);
            };
        };
    }

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

    /// <summary>
    /// 文件树拖放进入 — 高亮
    /// </summary>
    private void OnFileTreeDragEnter(object? sender, DragEventArgs e)
    {
        if (DataContext is MainViewModel vm)
            vm.DropHighlightBackground = "#2a2d35";
    }

    /// <summary>
    /// 文件树拖放离开 — 取消高亮
    /// </summary>
    private void OnFileTreeDragLeave(object? sender, DragEventArgs e)
    {
        if (DataContext is MainViewModel vm)
            vm.DropHighlightBackground = "#252526";
    }

    /// <summary>
    /// 文件树拖放放下
    /// </summary>
    private void OnFileTreeDrop(object? sender, DragEventArgs e)
    {
        if (DataContext is MainViewModel vm)
            vm.DropHighlightBackground = "#252526";
        ProcessDrop(e);
    }

    /// <summary>
    /// 处理拖放 — 支持文件/文件夹/多选
    /// </summary>
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
