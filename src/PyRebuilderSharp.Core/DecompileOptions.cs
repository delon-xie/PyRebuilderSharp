namespace PyRebuilderSharp.Core;

/// <summary>反编译选项</summary>
public class DecompileOptions
{
    public bool PreserveComments { get; set; } = true;
    public bool UseTypeAnnotations { get; set; } = false;
    public int MaxLineWidth { get; set; } = 88;
    public bool VerboseErrors { get; set; } = false;
    public string IndentString { get; set; } = "    ";
    
    /// <summary>是否在源码中输出孤儿块（已分块但未被正常流程处理的语句块）。</summary>
    public bool ShowOrphanBlocks { get; set; } = false;
    
    /// <summary>是否在源码末尾输出 # [SUMMARY] 统计信息。</summary>
    public bool ShowSummary { get; set; } = false;
    
    /// <summary>是否输出 # Decompiled from: 头部注释。默认为 false（抑制）。</summary>
    public bool ShowHeader { get; set; } = false;
}
