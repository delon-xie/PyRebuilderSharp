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

            var lastInstr = current.Instructions.LastOrDefault();
            if (lastInstr != null && JumpHelper.IsJump(lastInstr.Opcode))
            {
                seqBlock.EndsWithJump = true;
                seqBlock.JumpTarget = lastInstr.Argument;
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
