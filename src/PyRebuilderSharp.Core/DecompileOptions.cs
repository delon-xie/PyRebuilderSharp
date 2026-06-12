namespace PyRebuilderSharp.Core;

/// <summary>反编译选项</summary>
public class DecompileOptions
{
    public bool PreserveComments { get; set; } = true;
    public bool UseTypeAnnotations { get; set; } = false;
    public int MaxLineWidth { get; set; } = 88;
    public bool VerboseErrors { get; set; } = false;
    public string IndentString { get; set; } = "    ";
}
