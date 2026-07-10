using PyRebuilderSharp.Core.Models.CFG;
using System.Collections;

namespace PyRebuilderSharp.Core.Scanners;

/// <summary>
/// Phase 8: 结构验证器。
/// 在模式目录匹配后，用后支配拓扑 + COME_FROM 进行二次校验。
/// 
/// Step 5: 同时支持 ControlStructure 和 ISequentialControlStructure 两种类型。
/// 
/// 校验规则：
///   R1 — if-elif 链验证
///   R2 — try-except handler 归属验证
///   R3 — loop-body vs break 验证
///   R4 — else-body 归属验证
///   R5 — ExceptionTable 异常边验证
/// </summary>
public class StructuralValidator
{
    private readonly PostDominatorScanner _pdom;
    private readonly ControlFlowGraph _cfg;
    private readonly List<ValidationFailure> _failures = new();

    /// <summary>验证失败记录。</summary>
    public readonly record struct ValidationFailure(
        string Rule,
        string Description,
        int BlockOffset,
        string? Detail = null
    );

    public StructuralValidator(PostDominatorScanner pdom, ControlFlowGraph cfg)
    {
        _pdom = pdom;
        _cfg = cfg;
    }

    /// <summary>对控制结构列表执行所有验证规则。</summary>
    public IReadOnlyList<ValidationFailure> Validate(IEnumerable structures)
    {
        _failures.Clear();

        foreach (var structure in structures)
        {
            switch (structure)
            {
                // CFG-level structures (from ControlFlowScanner)
                case IfElseStructure ifElse:
                    ValidateR1_IfElifChain(ifElse);
                    ValidateR4_ElseBody(ifElse);
                    break;
                case LoopStructure loop:
                    ValidateR3_LoopBreak(loop);
                    ValidateR4_ElseBody(loop);
                    break;
                case TryStructure trySt:
                    ValidateR2_TryExceptHandler(trySt);
                    ValidateR5_ExceptionTable(trySt);
                    break;

                // SeqBlock-level structures (from SequentialBlockBuilder)
                case IfElseControlStructure seqIf:
                    ValidateR1_SeqIfElse(seqIf);
                    break;
                case TryControlStructure seqTry:
                    ValidateR5_SeqExceptionTable(seqTry);
                    break;
                case ForLoopControlStructure seqFor:
                case WhileLoopControlStructure seqWhile:
                    ValidateR3_SeqLoop(structure as dynamic);
                    break;
            }
        }

        foreach (var f in _failures)
        {
            Console.Error.WriteLine(
                $"[STRUCT_VALIDATE] FAIL {f.Rule} @0x{f.BlockOffset:X4}: {f.Description}");
        }

        return _failures;
    }

    public bool HasFailures => _failures.Count > 0;
    public IReadOnlyList<ValidationFailure> Failures => _failures;

    // ---- CFG-level validation (from Step 4) ----

    private void ValidateR1_IfElifChain(IfElseStructure ifElse)
    {
        var header = ifElse.Header;
        if (!header.Flags.HasFlag(BlockFlags.ConditionHeader)) return;
        var falseBranch = ifElse.FalseBranch;
        if (falseBranch == null) return;
        var firstSucc = falseBranch.Successors.FirstOrDefault();
        if (firstSucc == null) return;
        if (firstSucc.Flags.HasFlag(BlockFlags.ConditionHeader))
        {
            if (!_pdom.IsPostDominatedBy(firstSucc, header))
                AddFail("R1", "if-elif: header does not post-dominate false-branch successor",
                    header.StartOffset);
        }
    }

    private void ValidateR2_TryExceptHandler(TryStructure trySt)
    {
        var header = trySt.Header;
        foreach (var (handler, _) in trySt.ExceptHandlers)
        {
            if (!_pdom.IsPostDominatedBy(handler, header))
                AddFail("R2", "try handler not post-dominated by try header",
                    handler.StartOffset);
        }
        if (trySt.FinallyBody != null && !_pdom.IsPostDominatedBy(trySt.FinallyBody, header))
            AddFail("R2", "finally body not post-dominated by try header",
                trySt.FinallyBody.StartOffset);
    }

    private void ValidateR3_LoopBreak(LoopStructure loop)
    {
        var header = loop.Header;
        if (loop.BackEdge == null) return;
        if (!_pdom.IsPostDominatedBy(header, loop.BackEdge))
            AddFail("R3", "loop header does not post-dominate back-edge source (may be break)",
                header.StartOffset);
    }

    private void ValidateR4_ElseBody(ControlStructure structure)
    {
        var header = structure.Header;
        BasicBlock? elseBlock = structure switch
        {
            IfElseStructure ifs => ifs.FalseBranch,
            LoopStructure loop => loop.ElseBlock,
            _ => null,
        };
        if (elseBlock == null) return;
        if (!_pdom.IsPostDominatedBy(elseBlock, header))
            AddFail("R4", "else/false-branch not post-dominated by header",
                header.StartOffset);
    }

    private void ValidateR5_ExceptionTable(TryStructure trySt)
    {
        var header = trySt.Header;
        foreach (var (handler, _) in trySt.ExceptHandlers)
        {
            if (handler.StartOffset < header.StartOffset ||
                handler.StartOffset > header.EndOffset + 64)
                AddFail("R5", "ET handler offset outside expected try body range",
                    handler.StartOffset);
        }
        if (trySt.FinallyBody != null &&
            (trySt.FinallyBody.StartOffset < header.StartOffset ||
             trySt.FinallyBody.StartOffset > header.EndOffset + 64))
            AddFail("R5", "ET finally offset outside expected try body range",
                trySt.FinallyBody.StartOffset);
    }

    // ---- SeqBlock-level validation (Step 5) ----

    private void ValidateR1_SeqIfElse(IfElseControlStructure seqIf)
    {
        var headerOff = seqIf.Header.StartOffset;
        // 检查 false-branch 后是否紧跟另一个 IfElseControlStructure 的 header
        if (seqIf.FalseBranch != null)
        {
            var falseOff = seqIf.FalseBranch.StartOffset;
            if (!_pdom.IsPostDominatedBy(falseOff, headerOff, _cfg))
                AddFail("R1", "seq-if-else: header does not post-dominate false-branch",
                    headerOff);
        }
    }

    private void ValidateR3_SeqLoop(dynamic loop)
    {
        // 动态分发: for 和 while 的 BackEdge 检查
        SequentialBlock? backEdge = loop.BackEdge;
        if (backEdge == null) return;
        var headerOff = loop.Header.StartOffset;
        if (!_pdom.IsPostDominatedBy(headerOff, backEdge.StartOffset, _cfg))
            AddFail("R3", "seq-loop: header does not post-dominate back-edge",
                headerOff);
    }

    private void ValidateR5_SeqExceptionTable(TryControlStructure seqTry)
    {
        var headerOff = seqTry.Header.StartOffset;
        foreach (var (handler, _, _) in seqTry.ExceptHandlers)
        {
            var handlerOff = handler.StartOffset;
            if (handlerOff < headerOff || handlerOff > headerOff + 256)
                AddFail("R5", "seq-try: handler offset outside expected range",
                    handlerOff);
        }
        if (seqTry.FinallyBlock != null)
        {
            var finallyOff = seqTry.FinallyBlock.StartOffset;
            if (finallyOff < headerOff || finallyOff > headerOff + 256)
                AddFail("R5", "seq-try: finally offset outside expected range",
                    finallyOff);
        }
    }

    // ---- helpers ----

    private void AddFail(string rule, string desc, int offset, string? detail = null)
    {
        _failures.Add(new ValidationFailure(rule, desc, offset, detail));
    }
}
