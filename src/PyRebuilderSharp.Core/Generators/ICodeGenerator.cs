using PyRebuilderSharp.Core.Models.AST;

namespace PyRebuilderSharp.Core.Generators;

/// <summary>
/// 代码生成器接口。
/// </summary>
public interface ICodeGenerator
{
    string Generate(AstNode root);
}
