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

        BuildSequentialBlockGraph(sequentialBlocks, cfg);

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

            if (seqBlock.StartOffset == 0 || current.StartOffset < seqBlock.StartOffset)
                seqBlock.StartOffset = current.StartOffset;

            if (current.EndOffset > seqBlock.EndOffset)
                seqBlock.EndOffset = current.EndOffset;
            
            

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
                break;
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

            var nextBlock = current.Successors.First();
            if (nextBlock.Predecessors.Count != 1)
                break;

            if (processedBlockIds.Contains(nextBlock.Id))
                break;

            current = nextBlock;
        }

        return seqBlock;
    }

    private void AnnotateSequentialBlock(SequentialBlock seqBlock)
    {
        seqBlock.IsLoopHeader = seqBlock.Instructions.Any(i => 
            i.Opcode == Opcode.FOR_ITER ||
            i.Opcode is Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
                or Opcode.POP_JUMP_IF_FALSE_PY38 or Opcode.POP_JUMP_IF_TRUE_PY38);

        seqBlock.HasSetupWith = seqBlock.Instructions.Any(i => 
            i.Opcode == Opcode.SETUP_WITH);

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

        if (_codeObject.ExceptionTable != null)
        {
            foreach (var entry in _codeObject.ExceptionTable)
            {
                if (entry.StartOffset >= seqBlock.StartOffset && 
                    entry.StartOffset < seqBlock.EndOffset)
                {
                    seqBlock.ExceptionTableEntries.Add(entry);
                }
            }
        }
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
