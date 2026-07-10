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
    
    /// <summary>是否启用顺序块三阶段架构。默认为 true（使用 Phase 7 新架构）。</summary>
    public bool EnableSequentialBlocks { get; set; } = true;

    /// <summary>Phase 8 Step 4: 是否显示后支配树 + 结构验证诊断信息。默认为 false。</summary>
    public bool ShowStructuralValidation { get; set; } = false;
}
