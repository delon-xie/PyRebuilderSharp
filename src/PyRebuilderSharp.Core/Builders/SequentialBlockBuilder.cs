using System;
using System.Collections.Generic;
using System.Linq;
using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.CFG;
using PyRebuilderSharp.Core.Models.AST;
using PyRebuilderSharp.Core.Readers;
using PyRebuilderSharp.Core.Scanners;

namespace PyRebuilderSharp.Core.Builders;

public class SequentialBlockBuilder
{
    private readonly CodeObject _codeObject;
    private readonly BlockDecompiler _blockDecompiler;

    public SequentialBlockBuilder(CodeObject codeObject)
    {
        _codeObject = codeObject;
        _blockDecompiler = new BlockDecompiler();
    }

    public List<SequentialBlock> BuildSequentialBlocks(ControlFlowGraph cfg)
    {
        var sequentialBlocks = new List<SequentialBlock>();
        var processedBlockIds = new HashSet<int>();
        var sortedBlocks = cfg.Blocks
            .Where(b => b.Instructions.Count > 0)
            .OrderBy(b => b.StartOffset)
            .ToList();

        foreach (var block in sortedBlocks)
        {
            if (processedBlockIds.Contains(block.Id))
                continue;

            var seqBlock = MergeLinearChain(block, sortedBlocks, processedBlockIds);
            sequentialBlocks.Add(seqBlock);
        }

        foreach (var seqBlock in sequentialBlocks)
        {
            AnnotateSequentialBlock(seqBlock);
        }

        // Phase 2: ExceptionTable 标注扫描
        AnnotateExceptionTableBlocks(sequentialBlocks);

        // Phase 2a: Match/Case 标注扫描
        AnnotateMatchBlocks(sequentialBlocks);

        // Phase 2b: For/While 细分标注
        AnnotateForWhileSubtypes(sequentialBlocks);

        // Phase 2c: Handler 深度标注
        AnnotateHandlerDepths(sequentialBlocks);

        BuildSequentialBlockGraph(sequentialBlocks, cfg);

        // Phase 3b: 汇聚点/出口标注扫描
        AnnotateMergePointsAndExits(sequentialBlocks);

        // Phase 4: 回边标注扫描
        AnnotateBackEdges(sequentialBlocks);

        return sequentialBlocks;
    }

    private SequentialBlock MergeLinearChain(
        BasicBlock startBlock,
        List<BasicBlock> allBlocks,
        HashSet<int> processedBlockIds)
    {
        var seqBlock = new SequentialBlock();
        var current = startBlock;

        while (current != null && !processedBlockIds.Contains(current.Id))
        {
            bool currentStartsWithWithHeader = false;
            if (current.Instructions.Count >= 3)
            {
                currentStartsWithWithHeader = current.Instructions[0].Opcode == Opcode.LOAD_FAST_BORROW_314 && 
                    current.Instructions[1].Opcode == Opcode.COPY && 
                    current.Instructions[2].Opcode == Opcode.LOAD_SPECIAL;
            }
            
            bool currentStartsWithBeforeWith = current.Instructions.Count > 0 && 
                (current.Instructions[0].Opcode == Opcode.BEFORE_WITH ||
                 current.Instructions[0].Opcode == Opcode.BEFORE_WITH_312 ||
                 current.Instructions[0].Opcode == Opcode.BEFORE_WITH_313);
            
            if ((currentStartsWithWithHeader || currentStartsWithBeforeWith) && seqBlock.Instructions.Count > 0)
            {
                break;
            }

            // 方案 A: SETUP_FINALLY/SETUP_EXCEPT 处停止合并 — handler block 保持独立
            if (seqBlock.Instructions.Count > 0 && current.Instructions.Count > 0 &&
                current.Instructions.Any(i =>
                    i.Opcode == Opcode.SETUP_FINALLY ||
                    i.Opcode == Opcode.SETUP_EXCEPT))
            {
                break;
            }

            bool prevBlockEndsWithBeforeWith = seqBlock.Instructions.Count > 0 &&
                (seqBlock.Instructions.Last().Opcode == Opcode.BEFORE_WITH ||
                 seqBlock.Instructions.Last().Opcode == Opcode.BEFORE_WITH_312 ||
                 seqBlock.Instructions.Last().Opcode == Opcode.BEFORE_WITH_313);
            bool currentStartsWithStoreFast = current.Instructions.Count > 0 &&
                current.Instructions[0].Opcode == Opcode.STORE_FAST;
            
            if (prevBlockEndsWithBeforeWith && currentStartsWithStoreFast)
            {
                seqBlock.Instructions.Add(current.Instructions[0]);
                seqBlock.SourceBlocks.Add(current);
                
                if (seqBlock.StartOffset == 0 || current.StartOffset < seqBlock.StartOffset)
                    seqBlock.StartOffset = current.StartOffset;
                
                int newEndOffset = current.Instructions[0].Offset + 2;
                if (newEndOffset > seqBlock.EndOffset)
                    seqBlock.EndOffset = newEndOffset;
                
                
                break;
            }

            processedBlockIds.Add(current.Id);
            seqBlock.SourceBlocks.Add(current);

            foreach (var instr in current.Instructions)
            {
                seqBlock.Instructions.Add(instr);
            }

            // 方案 A: 如果 seqBlock 包含 SETUP_FINALLY/EXCEPT，只合并 header 本身
            bool seqBlockHasSetupFinally = seqBlock.Instructions.Count > 0 &&
                seqBlock.Instructions.Any(i =>
                    i.Opcode == Opcode.SETUP_FINALLY ||
                    i.Opcode == Opcode.SETUP_EXCEPT);

            if (seqBlock.StartOffset == 0 || current.StartOffset < seqBlock.StartOffset)
                seqBlock.StartOffset = current.StartOffset;

            if (current.EndOffset > seqBlock.EndOffset)
                seqBlock.EndOffset = current.EndOffset;

            if (seqBlockHasSetupFinally)
                break;
            
            

            bool containsWithHeaderStart = false;
            int withHeaderStartIdx = -1;
            for (int i = 0; i < seqBlock.Instructions.Count - 2; i++)
            {
                if (seqBlock.Instructions[i].Opcode == Opcode.LOAD_FAST_BORROW_314 && 
                    seqBlock.Instructions[i + 1].Opcode == Opcode.COPY && 
                    seqBlock.Instructions[i + 2].Opcode == Opcode.LOAD_SPECIAL)
                {
                    containsWithHeaderStart = true;
                    withHeaderStartIdx = i;
                    break;
                }
            }
            
            if (containsWithHeaderStart && withHeaderStartIdx > 0)
            {
                break;
            }
            
            if (containsWithHeaderStart && withHeaderStartIdx == 0)
            {
                bool hasCompleteWithPattern = false;
                for (int i = 0; i < seqBlock.Instructions.Count - 4; i++)
                {
                    if (seqBlock.Instructions[i].Opcode == Opcode.LOAD_SPECIAL && 
                        seqBlock.Instructions[i + 1].Opcode == Opcode.SWAP && 
                        seqBlock.Instructions[i + 2].Opcode == Opcode.SWAP && 
                        seqBlock.Instructions[i + 3].Opcode == Opcode.LOAD_SPECIAL && 
                        seqBlock.Instructions[i + 4].Opcode == Opcode.CALL)
                    {
                        hasCompleteWithPattern = true;
                        break;
                    }
                }
                
                if (hasCompleteWithPattern)
                {
                    break;
                }
            }

            var lastInstr = current.Instructions.LastOrDefault();
            if (lastInstr != null && JumpHelper.IsJump(lastInstr.Opcode))
            {
                seqBlock.EndsWithJump = true;
                seqBlock.JumpTarget = lastInstr.Argument;
                break;
            }

            bool hasWithCleanup = false;
            for (int i = 0; i < current.Instructions.Count - 4; i++)
            {
                if (current.Instructions[i].Opcode == Opcode.LOAD_CONST && 
                    current.Instructions[i + 1].Opcode == Opcode.LOAD_CONST && 
                    current.Instructions[i + 2].Opcode == Opcode.LOAD_CONST && 
                    current.Instructions[i + 3].Opcode == Opcode.CALL && 
                    current.Instructions[i + 4].Opcode == Opcode.POP_TOP)
                {
                    hasWithCleanup = true;
                    break;
                }
            }
            
            if (hasWithCleanup)
                break;
            
            if (seqBlock.StartOffset == 0 && seqBlock.Instructions.Count > 0 && !current.Instructions.Any(i => 
                i.Opcode == Opcode.LOAD_SPECIAL || 
                i.Opcode == Opcode.SETUP_WITH ||
                i.Opcode is Opcode.BEFORE_WITH or Opcode.BEFORE_WITH_312 or Opcode.BEFORE_WITH_313))
            {
                if (!_codeObject.IsCoroutine)
                {
                    break;
                }
            }
            
            bool seqBlockHasBeforeWith = seqBlock.Instructions.Any(i => 
                i.Opcode == Opcode.BEFORE_WITH ||
                i.Opcode == Opcode.BEFORE_WITH_312 ||
                i.Opcode == Opcode.BEFORE_WITH_313);
            
            if (seqBlockHasBeforeWith)
            {
                int lastIdx = seqBlock.Instructions.Count - 1;
                if (seqBlock.Instructions[lastIdx].Opcode == Opcode.STORE_FAST)
                {
                    break;
                }
                if (seqBlock.Instructions[lastIdx].Opcode == Opcode.BEFORE_WITH ||
                    seqBlock.Instructions[lastIdx].Opcode == Opcode.BEFORE_WITH_312 ||
                    seqBlock.Instructions[lastIdx].Opcode == Opcode.BEFORE_WITH_313)
                {
                    bool nextBlockHasStoreFast = false;
                    if (current.Successors.Count == 1)
                    {
                        var succBlock = current.Successors.First();
                        nextBlockHasStoreFast = succBlock.Instructions.Count > 0 && 
                            succBlock.Instructions[0].Opcode == Opcode.STORE_FAST;
                    }
                    
                    if (!nextBlockHasStoreFast)
                    {
                        break;
                    }
                }
                else
                {
                    break;
                }
            }
        
        bool succHasWithInstruction = false;
        if (current.Successors.Count == 1)
        {
            var succBlock = current.Successors.First();
            succHasWithInstruction = succBlock.Instructions.Any(i => 
                i.Opcode == Opcode.LOAD_SPECIAL || 
                i.Opcode == Opcode.SETUP_WITH ||
                i.Opcode is Opcode.BEFORE_WITH or Opcode.BEFORE_WITH_312 or Opcode.BEFORE_WITH_313);
        }
        
        if (succHasWithInstruction)
        {
            break;
        }

        bool succHasExcInfo = false;
        if (current.Successors.Count == 1)
        {
            var succBlock = current.Successors.First();
            succHasExcInfo = succBlock.Instructions.Any(i => 
                i.Opcode == Opcode.PUSH_EXC_INFO_312 || 
                i.Opcode == Opcode.PUSH_EXC_INFO);
        }
        
        if (succHasExcInfo)
        {
            break;
        }

            if (current.Successors.Count != 1)
                break;

            var nextSuccBlock = current.Successors.First();
            if (processedBlockIds.Contains(nextSuccBlock.Id))
                break;

            bool isAwaitPattern = false;
            if (_codeObject.IsCoroutine && nextSuccBlock.Instructions.Count >= 2)
            {
                bool startsWithLoadConstNone = nextSuccBlock.Instructions[0].Opcode == Opcode.LOAD_CONST;
                if (startsWithLoadConstNone)
                {
                    var constVal = _codeObject.Constants.TryGetValue(nextSuccBlock.Instructions[0].Argument ?? 0, out var v) ? v : null;
                    if (constVal == null && nextSuccBlock.Instructions[1].Opcode == Opcode.SEND)
                    {
                        isAwaitPattern = true;
                    }
                }
            }

            if (!isAwaitPattern && nextSuccBlock.Predecessors.Count != 1)
                break;

            current = nextSuccBlock;
        }

        return seqBlock;
    }

    private void AnnotateSequentialBlock(SequentialBlock seqBlock)
    {
        // Phase 3: 控制块起始标注
        seqBlock.IsLoopHeader = seqBlock.Instructions.Any(i => 
            i.Opcode == Opcode.FOR_ITER ||
            i.Opcode is Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
                or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38);

        seqBlock.IsWithHeader = seqBlock.Instructions.Any(i =>
            i.Opcode == Opcode.SETUP_WITH);

        seqBlock.HasSetupWith = seqBlock.IsWithHeader;

        seqBlock.HasBeforeWith = seqBlock.Instructions.Any(i => 
            i.Opcode is Opcode.BEFORE_WITH or Opcode.BEFORE_WITH_312 or Opcode.BEFORE_WITH_313);

        seqBlock.HasLoadSpecial = seqBlock.Instructions.Any(i => 
            i.Opcode == Opcode.LOAD_SPECIAL);

        seqBlock.HasSetupFinally = seqBlock.Instructions.Any(i => 
            i.Opcode == Opcode.SETUP_FINALLY);

        seqBlock.HasSetupExcept = seqBlock.Instructions.Any(i => 
            i.Opcode == Opcode.SETUP_EXCEPT);

        seqBlock.IsConditionHeader = seqBlock.Instructions.Any(i => 
            i.Opcode is Opcode.JUMP_IF_FALSE_OR_POP or Opcode.JUMP_IF_TRUE_OR_POP
                or Opcode.JUMP_IF_NOT_EXC_MATCH);

        seqBlock.IsTryHeader = seqBlock.HasSetupFinally || seqBlock.HasSetupExcept;

        seqBlock.EndsWithJump = seqBlock.Instructions.Count > 0 &&
            JumpHelper.IsJump(seqBlock.Instructions[^1].Opcode);

        if (seqBlock.EndsWithJump && seqBlock.Instructions[^1].Argument.HasValue)
            seqBlock.JumpTarget = seqBlock.Instructions[^1].Argument.Value;

        // Phase 2: ExceptionTable 条目 + IsExceptBlock
        if (_codeObject.ExceptionTable != null)
        {
            foreach (var entry in _codeObject.ExceptionTable)
            {
                if (entry.StartOffset >= seqBlock.StartOffset && 
                    entry.StartOffset < seqBlock.EndOffset)
                {
                    seqBlock.ExceptionTableEntries.Add(entry);
                }
                if (entry.TargetOffset >= seqBlock.StartOffset &&
                    entry.TargetOffset < seqBlock.EndOffset)
                {
                    seqBlock.IsExceptBlock = true;
                }
            }
        }
    }

    private void AnnotateExceptionTableBlocks(List<SequentialBlock> seqBlocks)
    {
        // Phase 2: 逐 ExceptionTable 条目标注 try 头
        if (_codeObject.ExceptionTable == null) return;

        var tryStartOffsets = new HashSet<int>();
        foreach (var seqBlock in seqBlocks)
        {
            foreach (var et in seqBlock.ExceptionTableEntries)
            {
                if (et.Depth == 0 && !et.Lasti && (et.IsExcept || et.IsFinally))
                    tryStartOffsets.Add(et.StartOffset);
            }
        }

        foreach (var tryStart in tryStartOffsets.OrderBy(x => x))
        {
            var headerBlock = seqBlocks.FirstOrDefault(sb =>
                sb.StartOffset <= tryStart && sb.EndOffset > tryStart);
            if (headerBlock != null)
            {
                headerBlock.IsTryHeader = true;
                headerBlock.ExceptionTryStartOffset = tryStart;
                var primaryEntry = headerBlock.ExceptionTableEntries
                    .FirstOrDefault(et => et.StartOffset == tryStart);
                if (primaryEntry != null)
                    headerBlock.ExceptionTryEndOffset = primaryEntry.EndOffset;
            }
        }

        // Step A: 防止过度链接 — 清除 handler 块范围内所有嵌套块的 IsTryHeader
        // 使用全包含检查（包含 handler body 内的所有 seqBlock）
        var handlerBlocks = new List<SequentialBlock>();
        foreach (var tryHeader in seqBlocks.Where(b => b.IsTryHeader))
        {
            foreach (var et in tryHeader.ExceptionTableEntries)
            {
                if (!et.IsExcept && !et.IsFinally) continue;
                var handlerBlock = FindSeqBlockByOffset(seqBlocks, et.TargetOffset);
                if (handlerBlock != null && !handlerBlocks.Contains(handlerBlock))
                    handlerBlocks.Add(handlerBlock);
            }
        }
        foreach (var hb in handlerBlocks)
        {
            foreach (var sb in seqBlocks)
            {
                // Phase 9-4: 不清理模块级 try header（偏移 0）
                // 也跳过 handler block 自身
                if (sb.StartOffset == 0 || sb == hb)
                    continue;
                if (sb.StartOffset >= hb.StartOffset && sb.EndOffset <= hb.EndOffset)
                    sb.IsTryHeader = false;
            }
        }
    }

    private void AnnotateMatchBlocks(List<SequentialBlock> seqBlocks)
    {
        // Phase 2a: Match/Case 标注扫描
        foreach (var seqBlock in seqBlocks)
        {
            if (seqBlock.Instructions.Any(i =>
                i.Opcode is Opcode.MATCH_KEYS_312 or Opcode.MATCH_KEYS_313
                    or Opcode.MATCH_CLASS_312 or Opcode.MATCH_CLASS_313
                    or Opcode.MATCH_MAPPING_312 or Opcode.MATCH_MAPPING_313
                    or Opcode.MATCH_SEQUENCE_312 or Opcode.MATCH_SEQUENCE_313))
            {
                seqBlock.IsMatchHeader = true;
                foreach (var instr in seqBlock.Instructions)
                {
                    if (instr.Opcode == Opcode.JUMP_IF_NOT_EXC_MATCH && instr.Argument.HasValue)
                    {
                        var caseBlock = FindSeqBlockByOffset(seqBlocks, instr.Argument.Value);
                        if (caseBlock != null)
                            caseBlock.IsCaseEntry = true;
                    }
                }
            }
        }
    }

    private void AnnotateForWhileSubtypes(List<SequentialBlock> seqBlocks)
    {
        // Phase 2b: For/While 细分标注
        foreach (var seqBlock in seqBlocks.Where(b => b.IsLoopHeader))
        {
            if (seqBlock.Instructions.Any(i => i.Opcode == Opcode.FOR_ITER))
            {
                seqBlock.IsForLoopHeader = true;
                var forIter = seqBlock.Instructions.First(i => i.Opcode == Opcode.FOR_ITER);
                if (forIter.Argument.HasValue)
                    seqBlock.ForIterExitTarget = forIter.Argument.Value;
                if (seqBlock.Successors.Count > 0)
                    seqBlock.Successors[0].IsForIterBody = true;
            }
            else if (seqBlock.IsBackEdgeTarget)
            {
                seqBlock.IsWhileLoopHeader = true;
            }
        }
    }

    private void AnnotateHandlerDepths(List<SequentialBlock> seqBlocks)
    {
        // Phase 2c: Handler 深度标注
        if (_codeObject.ExceptionTable == null) return;

        foreach (var seqBlock in seqBlocks)
        {
            foreach (var et in seqBlock.ExceptionTableEntries)
            {
                if (et.IsExcept || et.IsFinally)
                {
                    seqBlock.HandlerDepth = et.Depth;
                    if (et.IsFinally)
                        seqBlock.IsFinallyBlock = true;
                }
            }
        }

        // else 候选块: handler 后、finally 前的 seqBlock
        foreach (var tryHeader in seqBlocks.Where(b => b.IsTryHeader))
        {
            int finallyStart = tryHeader.ExceptionTableEntries
                .Where(et => et.IsFinally)
                .Select(et => et.TargetOffset)
                .DefaultIfEmpty(-1)
                .FirstOrDefault();
            if (finallyStart <= 0) continue;

            int lastHandlerEnd = tryHeader.ExceptionTableEntries
                .Where(et => et.IsExcept)
                .Select(et => et.EndOffset)
                .DefaultIfEmpty(-1)
                .Max();
            if (lastHandlerEnd < 0) continue;

            foreach (var sb in seqBlocks)
            {
                if (sb.StartOffset >= lastHandlerEnd && sb.StartOffset < finallyStart)
                    sb.IsTryElseBlock = true;
            }
        }
    }

    private void AnnotateBackEdges(List<SequentialBlock> seqBlocks)
    {
        // Phase 4: 回边标注扫描
        foreach (var seqBlock in seqBlocks)
        {
            foreach (var instr in seqBlock.Instructions)
            {
                if ((instr.Opcode == Opcode.JUMP_ABSOLUTE ||
                     instr.Opcode == Opcode.JUMP_FORWARD) && instr.Argument.HasValue)
                {
                    var target = FindSeqBlockByOffset(seqBlocks, instr.Argument.Value);
                    if (target != null && target.IsLoopHeader && target.StartOffset <= instr.Offset)
                    {
                        seqBlock.IsBackEdgeTarget = true;
                    }
                }
            }
        }

        // 标注循环体: 从 LoopHeader 的后继出发 BFS，直到回边目标
        foreach (var header in seqBlocks.Where(b => b.IsLoopHeader))
        {
            var visited = new HashSet<int>();
            var queue = new Queue<SequentialBlock>(header.Successors);
            while (queue.Count > 0)
            {
                var current = queue.Dequeue();
                if (current == null || current == header) continue;
                if (visited.Contains(current.Id)) continue;
                visited.Add(current.Id);
                if (current.IsBackEdgeTarget) continue;
                if (current.StartOffset < header.StartOffset) continue;

                current.IsLoopBody = true;

                foreach (var succ in current.Successors)
                {
                    if (!visited.Contains(succ.Id))
                        queue.Enqueue(succ);
                }
            }
        }
    }

    private void AnnotateMergePointsAndExits(List<SequentialBlock> seqBlocks)
    {
        // Phase 3b: 汇聚点/出口标注扫描
        foreach (var seqBlock in seqBlocks)
        {
            if (seqBlock.Successors.Count > 1)
                continue;
            if (seqBlock.PredecessorCount > 1)
                seqBlock.IsMergePoint = true;
        }

        foreach (var header in seqBlocks.Where(b => b.IsForLoopHeader))
        {
            if (header.ForIterExitTarget > 0)
            {
                var exitBlock = FindSeqBlockByOffset(seqBlocks, header.ForIterExitTarget);
                if (exitBlock != null)
                    exitBlock.IsBreakTarget = true;
            }
        }

        foreach (var header in seqBlocks.Where(b => b.IsLoopHeader))
        {
            header.IsContinueTarget = true;
        }

        foreach (var seqBlock in seqBlocks)
        {
            bool hasTerminal = seqBlock.Instructions.Any(i =>
                i.Opcode == Opcode.RETURN_VALUE ||
                i.Opcode == Opcode.RAISE_VARARGS);
            if (hasTerminal && seqBlock.Successors.Count > 0)
            {
                foreach (var succ in seqBlock.Successors)
                    succ.IsDeadCodeBlock = true;
            }
        }
    }

    private static SequentialBlock? FindSeqBlockByOffset(List<SequentialBlock> seqBlocks, int offset)
    {
        return seqBlocks.FirstOrDefault(sb =>
            sb.StartOffset <= offset && sb.EndOffset >= offset);
    }

    private void BuildSequentialBlockGraph(List<SequentialBlock> seqBlocks, ControlFlowGraph cfg)
    {
        var blockByOffset = seqBlocks.ToDictionary(b => b.StartOffset);

        foreach (var seqBlock in seqBlocks)
        {
            foreach (var sourceBlock in seqBlock.SourceBlocks)
            {
                foreach (var succ in sourceBlock.Successors)
                {
                    var targetSeqBlock = blockByOffset.Values
                        .FirstOrDefault(sb => sb.StartOffset <= succ.StartOffset && sb.EndOffset >= succ.StartOffset);
                    if (targetSeqBlock != null && !seqBlock.Successors.Contains(targetSeqBlock))
                    {
                        seqBlock.Successors.Add(targetSeqBlock);
                    }
                }
            }
        }
    }

    public bool VerifyNoOrphanBlocks(List<SequentialBlock> seqBlocks, ControlFlowGraph cfg)
    {
        var allBasicBlockIds = new HashSet<int>(cfg.Blocks.Where(b => b.Instructions.Count > 0).Select(b => b.Id));
        var processedBasicBlockIds = new HashSet<int>();

        foreach (var seqBlock in seqBlocks)
        {
            foreach (var sourceBlock in seqBlock.SourceBlocks)
            {
                processedBasicBlockIds.Add(sourceBlock.Id);
            }
        }

        var orphanIds = allBasicBlockIds.Except(processedBasicBlockIds).ToList();
        return orphanIds.Count == 0;
    }

    public void DecompileSequentialBlocks(List<SequentialBlock> seqBlocks)
    {
        foreach (var seqBlock in seqBlocks)
        {
            var result = _blockDecompiler.DecompileBlock(
                seqBlock.Instructions, 
                _codeObject, 
                seqBlock.Id);

            if (result.IsSuccess)
            {
                seqBlock.Statements = result.Statements;
            }
        }
    }
}
