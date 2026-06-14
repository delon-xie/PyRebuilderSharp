using PyRebuilderSharp.Core.Models.AST;
using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.CFG;
using PyRebuilderSharp.Core.Scanners;

namespace PyRebuilderSharp.Core.Builders;

/// <summary>
/// 块级反编译器 — 每个基本块独立反编译，支持注释兜底。
/// 
/// 核心原则：
/// 1. 块隔离 — 一个块失败不影响其他块
/// 2. 注释兜底 — 失败块输出为格式化注释（含偏移、错误、原始字节码）
/// 3. 最大恢复 — 整体仍生成最大可读的 Python 源码
/// </summary>
public class BlockDecompiler
{
    /// <summary>
    /// 反编译单个基本块。
    /// </summary>
    public BlockResult DecompileBlock(
        List<Instruction> instructions,
        CodeObject codeObject,
        int blockId,
        HashSet<int> loopHeaderOffsets = null,
        bool isForLoop = false)
    {
        try
        {
            var stackMachine = new StackMachine(codeObject);
            stackMachine.SetIsForLoop(isForLoop);
            if (loopHeaderOffsets != null && loopHeaderOffsets.Count > 0)
                stackMachine.SetLoopHeaders(loopHeaderOffsets);
            var stmts = new List<Stmt>();
            bool seenTerminalJump = false;

            foreach (var instr in instructions)
            {
                var result = stackMachine.Execute(instr);
                if (result is Stmt stmt)
                {
                    if (seenTerminalJump && stmt is Continue or Break or Return or Raise)
                        continue;
                    stmts.Add(stmt);
                    if (stmt is Continue or Break or Return or Raise)
                        seenTerminalJump = true;
                }
            }

            // 处理栈上剩余表达式（作为表达式语句）
            while (stackMachine.HasResults)
            {
                stmts.Add(new ExprStmt(stackMachine.PopResult()));
            }

            // 死代码消除：移除 Continue/Break/Return 之后的语句
            stmts = EliminateDeadCode(stmts);

            return BlockResult.Success(stmts);
        }
        catch (Exception ex)
        {
            // ❗ 核心：捕获异常→生成注释块兜底
            // 记录到崩溃日志
            try
            {
                PyRebuilderSharp.Core.Services.CrashCollector.RecordCrash(
                    new PyRebuilderSharp.Core.Services.CrashContext
                    {
                        FileName = $"block_{blockId}",
                        SourceSnippet = instructions.Count > 0
                            ? $"{instructions[0].Opcode}..." : ""
                    },
                    ex);
            }
            catch { }
            return BlockResult.FallbackAsComment(instructions, ex, blockId);
        }
    }

    /// <summary>
    /// 批量反编译多个基本块。
    /// 每个块独立执行，失败不影响其他块。
    /// </summary>
    public Dictionary<int, BlockResult> DecompileBlocks(
        List<BasicBlock> blocks,
        CodeObject codeObject)
    {
        var results = new Dictionary<int, BlockResult>();

        // 标记循环头（FOR_ITER / while 条件）所在的块偏移
        var loopHeaders = new HashSet<int>();
        var forLoopBodyBlocks = new HashSet<int>(); // for 循环体块的 block id
        foreach (var block in blocks)
        {
            if (block.Flags.HasFlag(BlockFlags.LoopHeader))
                loopHeaders.Add(block.StartOffset);

            // 如果块包含 FOR_ITER，它的后续块（直到跳转目标）是 for 循环体
            if (block.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
            {
                foreach (var succ in block.Successors)
                {
                    MarkForLoopBody(succ, block, forLoopBodyBlocks, new HashSet<int>());
                }
            }
        }

        foreach (var block in blocks)
        {
            var instrs = block.Instructions;
            // 去掉块最后的跳转指令（由控制流处理）
            if (instrs.Count > 0 && JumpHelper.IsJump(instrs.Last().Opcode))
                instrs = instrs.Take(instrs.Count - 1).ToList();

            // 检测该块是否属于 for 循环体
            bool isForLoop = forLoopBodyBlocks.Contains(block.Id);

            // 检查块中的 JUMP_ABSOLUTE 是否跳转到循环头（continue）
            var continueInstrs = new List<int>(); // offsets of JUMP_ABSOLUTE to loop header
            for (int i = 0; i < instrs.Count; i++)
            {
                var instr = instrs[i];
                if (instr.Opcode == Opcode.JUMP_ABSOLUTE && instr.Argument.HasValue
                    && loopHeaders.Contains(instr.Argument.Value))
                {
                    continueInstrs.Add(i);
                }
            }

            var result = DecompileBlock(instrs, codeObject, block.Id, loopHeaders, isForLoop);
            results[block.Id] = result;
        }

        return results;
    }

    /// <summary>
    /// 移除 Continue/Break/Return 之后的死代码（同一基本块内不可达的语句）。
    /// </summary>
    private List<Stmt> EliminateDeadCode(List<Stmt> stmts)
    {
        for (int i = 0; i < stmts.Count; i++)
        {
            if (stmts[i] is Continue or Break or Return or Raise)
            {
                return stmts.Take(i + 1).ToList();
            }
        }
        return stmts;
    }

    /// <summary>
    /// 递归标记 for 循环体块（遍历后继，直到回到 header 或已访问）。
    /// </summary>
    private void MarkForLoopBody(BasicBlock entry, BasicBlock header, HashSet<int> bodyBlocks, HashSet<int> visited)
    {
        if (entry == null || entry == header || visited.Contains(entry.Id))
            return;
        visited.Add(entry.Id);
        bodyBlocks.Add(entry.Id);
        foreach (var succ in entry.Successors)
            MarkForLoopBody(succ, header, bodyBlocks, visited);
    }
}
