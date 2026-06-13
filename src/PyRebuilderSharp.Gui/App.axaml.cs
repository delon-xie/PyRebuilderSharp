using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;
using PyRebuilderSharp.Gui.ViewModels;
using PyRebuilderSharp.Gui.Views;

namespace PyRebuilderSharp.Gui;

public partial class App : Application
{
    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            // 关键：先构造 Window 再设 DataContext，确保 DataContextChanged 被触发
            var vm = new MainViewModel();
            var window = new MainWindow();
            window.DataContext = vm;
            desktop.MainWindow = window;
        }

        base.OnFrameworkInitializationCompleted();
    }
}
