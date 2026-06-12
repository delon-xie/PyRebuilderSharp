namespace PyRebuilderSharp.Core.Models.AST;

/// <summary>
/// AST节点抽象基类。
/// 使用C# record类型实现值语义。
/// </summary>
public abstract record AstNode
{
    public SourceLocation Location { get; init; }
}

/// <summary>源码位置</summary>
public record SourceLocation(int Line, int Column, int EndLine, int EndColumn);
