using Avalonia.Controls;
using Avalonia.Interactivity;
using PyRebuilderSharp.Gui.ViewModels;

namespace PyRebuilderSharp.Gui.Views;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    protected override void OnInitialized()
    {
        base.OnInitialized();

        if (DataContext is MainViewModel vm)
        {
            vm.TopLevel = this;
        }
    }
}
