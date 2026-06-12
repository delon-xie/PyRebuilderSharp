using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.CFG;

namespace PyRebuilderSharp.Core.Scanners;

/// <summary>
/// Phase 2: 控制流扫描器。
/// 负责识别高级控制结构（循环、条件）。
/// 核心算法：支配树分析 + 自然循环检测。
/// </summary>
public class ControlFlowScanner : IControlFlowScanner
{
    private ControlFlowGraph _cfg = null!;
    private Dictionary<BasicBlock, BasicBlock> _idoms = new();

    /// <summary>
    /// 分析控制流，识别高级结构。
    /// </summary>
    public StructuredCFG Analyze(List<BasicBlock> blocks)
    {
        _cfg = BuildCFG(blocks);
        _idoms = ComputeImmediateDominators(_cfg);
        var loops = DetectNaturalLoops(_cfg, _idoms);
        var structured = BuildStructuredCFG(_cfg, loops);
        return structured;
    }

    private ControlFlowGraph BuildCFG(List<BasicBlock> blocks)
    {
        if (blocks == null || blocks.Count == 0)
        {
            var emptyBlock = new BasicBlock { StartOffset = 0, EndOffset = 0, Flags = BlockFlags.Entry | BlockFlags.Synthetic };
            blocks = new List<BasicBlock> { emptyBlock };
        }

        var cfg = new ControlFlowGraph
        {
            Entry = blocks.First(),
            Exit = CreateSyntheticExit(blocks)
        };
        foreach (var b in blocks) cfg.Blocks.Add(b);

        foreach (var block in blocks)
            cfg.BlockByOffset[block.StartOffset] = block;

        return cfg;
    }

    private BasicBlock CreateSyntheticExit(List<BasicBlock> blocks)
    {
        var exit = new BasicBlock
        {
            StartOffset = int.MaxValue,
            EndOffset = int.MaxValue,
            Flags = BlockFlags.Exit | BlockFlags.Synthetic
        };

        foreach (var block in blocks.Where(b => !b.Successors.Any()))
        {
            block.Successors.Add(exit);
            exit.Predecessors.Add(block);
        }

        return exit;
    }

    private Dictionary<BasicBlock, BasicBlock> ComputeImmediateDominators(ControlFlowGraph cfg)
    {
        var dom = new Dictionary<BasicBlock, HashSet<BasicBlock>>();
        var allBlocks = new HashSet<BasicBlock>(cfg.Blocks);

        foreach (var block in cfg.Blocks)
        {
            dom[block] = block == cfg.Entry
                ? new HashSet<BasicBlock> { block }
                : new HashSet<BasicBlock>(allBlocks);
        }

        bool changed;
        do
        {
            changed = false;
            foreach (var block in cfg.Blocks.Skip(1))
            {
                var predecessors = block.Predecessors.ToList();
                if (predecessors.Count == 0) continue;

                var newDom = new HashSet<BasicBlock>(dom[predecessors[0]]);
                for (int i = 1; i < predecessors.Count; i++)
                    newDom.IntersectWith(dom[predecessors[i]]);
                newDom.Add(block);

                if (!dom[block].SetEquals(newDom))
                {
                    dom[block] = newDom;
                    changed = true;
                }
            }
        } while (changed);

        var idoms = new Dictionary<BasicBlock, BasicBlock>();
        foreach (var block in cfg.Blocks)
        {
            if (block == cfg.Entry) continue;
            var dominators = dom[block]
                .Where(d => d != block)
                .OrderByDescending(d => dom[d].Count)
                .ToList();
            idoms[block] = dominators.Count > 0 ? dominators.First() : cfg.Entry;
        }

        return idoms;
    }

    private List<LoopStructure> DetectNaturalLoops(
        ControlFlowGraph cfg,
        Dictionary<BasicBlock, BasicBlock> idoms)
    {
        var loops = new List<LoopStructure>();
        var processedHeaders = new HashSet<BasicBlock>();

        // Build full dominator sets for proper dominance checking
        var dom = ComputeDominators(cfg);

        foreach (var block in cfg.Blocks)
        {
            foreach (var pred in block.Predecessors)
            {
                // 回边检测：block 支配 pred（不要求 immediate domination）
                if (dom.TryGetValue(pred, out var predDom) && predDom.Contains(block))
                {
                    // 真正的循环回边必须从高偏移指向低偏移（向后跳转）
                    // 自循环（pred == block）也是合法的循环
                    if (pred.StartOffset < block.StartOffset) continue;
                    
                    if (processedHeaders.Contains(block)) continue;
                    processedHeaders.Add(block);

                    var loopBody = CollectLoopBody(block, pred);
                    var type = DetermineLoopType(block);
                    var elseBlock = FindLoopElseBlock(block, loopBody);

                    var loop = new LoopStructure(
                        Header: block,
                        BodyEntry: FindBodyEntry(block, loopBody),
                        BackEdge: pred,
                        ElseBlock: elseBlock,
                        Type: type
                    );
                    loops.Add(loop);

                    foreach (var bodyBlock in loopBody)
                        bodyBlock.Flags |= BlockFlags.LoopBody;
                    block.Flags |= BlockFlags.LoopHeader;
                    pred.Flags |= BlockFlags.LoopBackEdge;
                }
            }
        }

        loops.Sort((a, b) => b.BodyBlocks.Count.CompareTo(a.BodyBlocks.Count));
        return loops;
    }

    private Dictionary<BasicBlock, HashSet<BasicBlock>> ComputeDominators(ControlFlowGraph cfg)
    {
        var dom = new Dictionary<BasicBlock, HashSet<BasicBlock>>();
        var allBlocks = new HashSet<BasicBlock>(cfg.Blocks);
        foreach (var block in cfg.Blocks)
        {
            dom[block] = block == cfg.Entry
                ? new HashSet<BasicBlock> { block }
                : new HashSet<BasicBlock>(allBlocks);
        }
        bool changed;
        do
        {
            changed = false;
            foreach (var block in cfg.Blocks.Skip(1))
            {
                var predecessors = block.Predecessors.ToList();
                if (predecessors.Count == 0) continue;
                var newDom = new HashSet<BasicBlock>(dom[predecessors[0]]);
                for (int i = 1; i < predecessors.Count; i++)
                    newDom.IntersectWith(dom[predecessors[i]]);
                newDom.Add(block);
                if (!dom[block].SetEquals(newDom))
                {
                    dom[block] = newDom;
                    changed = true;
                }
            }
        } while (changed);
        return dom;
    }

    public List<BasicBlock> CollectLoopBody(BasicBlock header, BasicBlock backEdge)
    {
        var body = new HashSet<BasicBlock> { header };
        var worklist = new Queue<BasicBlock>();
        worklist.Enqueue(backEdge);

        while (worklist.Count > 0)
        {
            var current = worklist.Dequeue();
            if (body.Contains(current)) continue;
            body.Add(current);
            foreach (var pred in current.Predecessors)
            {
                if (!body.Contains(pred) && pred != header)
                    worklist.Enqueue(pred);
            }
        }

        return body.ToList();
    }

    private LoopType DetermineLoopType(BasicBlock header)
    {
        bool hasForPattern = header.Instructions.Any(i =>
            i.Opcode == Opcode.GET_ITER || i.Opcode == Opcode.FOR_ITER);
        if (hasForPattern) return LoopType.For;

        bool hasCondition = header.Instructions.Any(i =>
            i.Opcode == Opcode.POP_JUMP_IF_TRUE ||
            i.Opcode == Opcode.POP_JUMP_IF_FALSE);
        return hasCondition ? LoopType.While : LoopType.Infinite;
    }

    private BasicBlock? FindBodyEntry(BasicBlock header, List<BasicBlock> loopBody)
        => header.Successors.FirstOrDefault(s => loopBody.Contains(s) && s != header);

    private BasicBlock? FindLoopElseBlock(BasicBlock header, List<BasicBlock> loopBody)
        => header.Successors.FirstOrDefault(s => !loopBody.Contains(s));

    private StructuredCFG BuildStructuredCFG(ControlFlowGraph cfg, List<LoopStructure> loops)
    {
        var structured = new StructuredCFG { RawCFG = cfg };
        foreach (var loop in loops)
        {
            structured.Structures.Add(loop);
            foreach (var block in loop.BodyBlocks)
                structured.BlockToStructure[block] = loop;
        }
        return structured;
    }
}
