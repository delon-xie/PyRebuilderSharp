using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.CFG;

namespace PyRebuilderSharp.Core.Scanners;

/// <summary>
/// Phase 1: 分块扫描器接口。
/// </summary>
public interface IBlockScanner
{
    List<BasicBlock> Scan(CodeObject codeObj);
}
