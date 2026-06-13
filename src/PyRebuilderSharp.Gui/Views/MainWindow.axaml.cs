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

        System.Console.Error.WriteLine($"[DEBUG] InitOK SourceBlock={(SourceBlock != null)} DisasmBlock={(DisasmBlock != null)}");

        // 拖放
        AddHandler(DragDrop.DropEvent, OnDrop);
        AddHandler(DragDrop.DragOverEvent, OnDragOver);

        // DataContextChanged → TopLevel + 事件
        DataContextChanged += (_, _) =>
        {
            if (DataContext is not MainViewModel vm) return;
            System.Console.Error.WriteLine("[DEBUG] DataContextChanged: wiring VM");
            vm.TopLevel = this;
            vm.OnCodeChanged += code =>
            {
                System.Console.Error.WriteLine($"[DEBUG] OnCodeChanged len={code?.Length ?? 0}");
                if (SourceBlock == null) return;
                if (string.IsNullOrEmpty(code))
                    SourceBlock.Inlines = null;
                else
                    SourceBlock.Inlines = PythonSyntaxHighlight.Highlight(code);
            };
            vm.OnDisasmChanged += code =>
            {
                System.Console.Error.WriteLine($"[DEBUG] OnDisasmChanged len={code?.Length ?? 0}");
                if (DisasmBlock == null) return;
                if (string.IsNullOrEmpty(code))
                    DisasmBlock.Inlines = null;
                else
                    DisasmBlock.Inlines = DisasmSyntaxHighlight.Highlight(code);
            };
        };
    }

    private void OnDragOver(object? sender, DragEventArgs e) { e.DragEffects = DragDropEffects.Copy; }
    private void OnDrop(object? sender, DragEventArgs e)
    {
        if (DataContext is not MainViewModel vm) return;
        if (e.Data is not IDataObject dataObj) return;
        var files = dataObj.GetFiles();
        if (files == null) return;
        foreach (var file in files)
        {
            var path = file.Path.LocalPath;
            if (Directory.Exists(path)) vm.AddFolderToTree(path);
            else if (path.EndsWith(".pyc") && File.Exists(path)) vm.AddFileToTree(path);
        }
        var lastRoot = vm.FileTree.LastOrDefault();
        if (lastRoot != null)
            vm.SelectedNode = lastRoot.Children.Count > 0 ? lastRoot.Children.Last() : lastRoot;
    }
}
