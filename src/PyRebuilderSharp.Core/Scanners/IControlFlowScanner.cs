using PyRebuilderSharp.Core.Models.CFG;

namespace PyRebuilderSharp.Core.Scanners;

/// <summary>
/// Phase 2: 控制流扫描器接口。
/// </summary>
public interface IControlFlowScanner
{
    StructuredCFG Analyze(List<BasicBlock> blocks);
}
