using Avalonia.Controls;
using Avalonia.Input;
using PyRebuilderSharp.Gui.ViewModels;
using System.IO;

namespace PyRebuilderSharp.Gui.Views;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        // 拖放支持
        AddHandler(DragDrop.DropEvent, OnDrop);
        AddHandler(DragDrop.DragOverEvent, OnDragOver);
    }

    protected override void OnInitialized()
    {
        base.OnInitialized();
        if (DataContext is MainViewModel vm)
            vm.TopLevel = this;
    }

    private void OnDragOver(object? sender, DragEventArgs e)
    {
        if (e.Data.Contains(DataFormats.Files))
            e.DragEffects = DragDropEffects.Copy;
    }

    private async void OnDrop(object? sender, DragEventArgs e)
    {
        if (!e.Data.Contains(DataFormats.Files)) return;
        var files = e.Data.GetFiles();
        if (files == null) return;

        if (DataContext is MainViewModel vm)
        {
            foreach (var file in files)
            {
                var path = file.Path.LocalPath;
                if (path.EndsWith(".pyc") && File.Exists(path))
                {
                    var pyVersion = MainViewModel.DetectPythonVersionPublic(path);
                    vm.Files.Add(new FileItem
                    {
                        Name = System.IO.Path.GetFileName(path),
                        FullPath = path,
                        PythonVersion = $"🐍 {pyVersion}"
                    });
                }
            }
            if (vm.Files.Count > 0)
                vm.SelectedFile = vm.Files[^1];
        }
    }
}
