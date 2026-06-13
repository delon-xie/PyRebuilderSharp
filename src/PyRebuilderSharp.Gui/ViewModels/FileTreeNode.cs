using System.Collections.ObjectModel;

namespace PyRebuilderSharp.Gui.ViewModels;

public class FileTreeNode
{
    public string Name { get; set; } = "";
    public string? FullPath { get; set; }  // null = 目录节点
    public bool IsDirectory => FullPath == null;
    public string Icon => IsDirectory ? "📁" : "📄";
    public ObservableCollection<FileTreeNode> Children { get; set; } = new();
}
