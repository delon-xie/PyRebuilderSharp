namespace PyRebuilderSharp.Core.Generators;

/// <summary>
/// 代码生成选项。
/// </summary>
public class CodeGenOptions
{
    public bool AddLineNumbers { get; set; } = false;
    public bool FormatImports { get; set; } = true;
    public bool SortImports { get; set; } = true;
    public bool RemoveUnusedVariables { get; set; } = false;
}
