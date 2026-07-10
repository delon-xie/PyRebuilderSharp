using PyRebuilderSharp.Core.Models.Bytecode;
using PyRebuilderSharp.Core.Models.CFG;

namespace PyRebuilderSharp.Core.Scanners;

/// <summary>
/// Phase 2d: 后支配树分析 + COME_FROM 集合构建。
/// 
/// 原理：
/// - 将 CFG 反向（反转所有边），在前向支配树算法上跑一次 → 后支配树
/// - 对每个跳转目标指令，在其目标块中构建"COME_FROM"映射
/// - 后支配树用于验证：if-elif 链的 else 分支是否确实被 header 后支配
/// - 基于 Step 2 研读① uncompyle6 的 COME_FROM 分类规则
/// 
/// 用途：供给 StructuralValidator 做结构验证二次校验。
/// </summary>
public class PostDominatorScanner
{
    private Dictionary<BasicBlock, BasicBlock> _postIdoms = new();
    private Dictionary<BasicBlock, HashSet<BasicBlock>> _postDominance = new();
    private Dictionary<int, List<ComeFromSource>> _comeFrom = new();

    /// <summary>COME_FROM 来源信息。</summary>
    public readonly record struct ComeFromSource(
        int SourceOffset,
        int SourceBlockId,
        ComeFromType Type
    );

    /// <summary>COME_FROM 类型（对应 uncompyle6 的 COME_FROM / COME_FROM_FINALLY / ...）。</summary>
    public enum ComeFromType
    {
        /// <summary>普通条件跳转（POP_JUMP_IF_*）</summary>
        Conditional,
        /// <summary>SETUP_FINALLY → try-finally 入口</summary>
        Finally,
        /// <summary>SETUP_EXCEPT → try-except handler 入口</summary>
        ExceptHandler,
        /// <summary>FOR_ITER → for 循环出口</summary>
        ForLoopEnd,
        /// <summary>ExceptionTable handler 目标 (3.11+)</summary>
        ExceptionTable,
    }

    // ---- 公共 API ----

    /// <summary>
    /// 计算后支配树。返回 immediate post-dominator 字典。
    /// </summary>
    public Dictionary<BasicBlock, BasicBlock> ComputePostDominators(ControlFlowGraph cfg)
    {
        var reverseCFG = BuildReverseCFG(cfg);
        _postIdoms = ComputeImmediateDominatorsOnGraph(reverseCFG);
        _postDominance = ComputePostDominanceSets(cfg);
        return _postIdoms;
    }

    /// <summary>
    /// 构建 COME_FROM 映射。
    /// 对每个跳转指令记录 source→target。
    /// 分类规则来自 uncompyle6 scanner37base.py。
    /// </summary>
    public Dictionary<int, List<ComeFromSource>> BuildComeFromMap(ControlFlowGraph cfg)
    {
        _comeFrom.Clear();
        foreach (var block in cfg.Blocks)
        {
            foreach (var instr in block.Instructions)
            {
                if (!instr.Argument.HasValue) continue;
                var cfType = ClassifyJump(instr.Opcode, instr.Argument.Value, cfg);
                if (cfType == null) continue;

                int target = instr.Argument.Value;
                if (!_comeFrom.ContainsKey(target))
                    _comeFrom[target] = new List<ComeFromSource>();

                _comeFrom[target].Add(new ComeFromSource(
                    instr.Offset, block.Id, cfType.Value));
            }
        }
        return _comeFrom;
    }

    /// <summary>获取后支配树。</summary>
    public Dictionary<BasicBlock, BasicBlock> PostIdoms => _postIdoms;

    /// <summary>获取完整后支配集。</summary>
    public Dictionary<BasicBlock, HashSet<BasicBlock>> PostDominance => _postDominance;

    /// <summary>获取 COME_FROM 映射。</summary>
    public Dictionary<int, List<ComeFromSource>> ComeFrom => _comeFrom;

    /// <summary>
    /// 检查 targetOffset 是否被 sourceOffset 后支配。
    /// </summary>
    public bool IsPostDominatedBy(int targetOffset, int sourceOffset, ControlFlowGraph cfg)
    {
        if (!cfg.BlockByOffset.TryGetValue(targetOffset, out var targetBlock)) return false;
        if (!cfg.BlockByOffset.TryGetValue(sourceOffset, out var sourceBlock)) return false;
        if (!_postDominance.TryGetValue(targetBlock, out var dominators)) return false;
        return dominators.Contains(sourceBlock);
    }

    /// <summary>
    /// 检查 block 的后支配集是否包含 candidate。
    /// </summary>
    public bool IsPostDominatedBy(BasicBlock block, BasicBlock candidate)
    {
        if (!_postDominance.TryGetValue(block, out var dominators)) return false;
        return dominators.Contains(candidate);
    }

    // ---- 内部实现 ----

    /// <summary>构建反向 CFG：反转所有边，以原始 Exit 为入口。</summary>
    private static ControlFlowGraph BuildReverseCFG(ControlFlowGraph original)
    {
        var reverseBlocks = new Dictionary<int, BasicBlock>();
        BasicBlock? revEntry = null, revExit = null;

        // 创建所有块的副本（保持 Id 不变）
        foreach (var orig in original.Blocks)
        {
            var copy = new BasicBlock
            {
                StartOffset = orig.StartOffset,
                EndOffset = orig.EndOffset,
                Flags = orig.Flags,
            };
            copy.Instructions.AddRange(orig.Instructions);
            reverseBlocks[orig.Id] = copy;
        }

        // 反转边：原 predecessor ↔ successor 互换
        foreach (var orig in original.Blocks)
        {
            var rev = reverseBlocks[orig.Id];
            foreach (var origSucc in orig.Successors)
            {
                if (reverseBlocks.TryGetValue(origSucc.Id, out var revSucc))
                {
                    rev.Predecessors.Add(revSucc);
                    revSucc.Successors.Add(rev);
                }
            }
            foreach (var origPred in orig.Predecessors)
            {
                if (reverseBlocks.TryGetValue(origPred.Id, out var revPred))
                {
                    rev.Successors.Add(revPred);
                    revPred.Predecessors.Add(rev);
                }
            }
        }

        // 反向图的入口 = 原始图的 Exit，反向图的 Exit = 原始图的 Entry
        if (reverseBlocks.TryGetValue(original.Exit.Id, out revEntry)
            && reverseBlocks.TryGetValue(original.Entry.Id, out revExit))
        {
            revExit.Flags |= BlockFlags.Exit;
            // 确保所有无后继的节点连到反向 exit
            foreach (var block in reverseBlocks.Values)
            {
                if (!block.Successors.Any() && block != revExit)
                {
                    block.Successors.Add(revExit);
                    revExit.Predecessors.Add(block);
                }
            }
        }

        var allBlocks = reverseBlocks.Values.ToList();
        var reverseCfg = new ControlFlowGraph
        {
            Entry = revEntry ?? allBlocks.First(),
            Exit = revExit ?? new BasicBlock
            {
                StartOffset = int.MaxValue, EndOffset = int.MaxValue,
                Flags = BlockFlags.Exit | BlockFlags.Synthetic
            },
        };
        foreach (var b in allBlocks) reverseCfg.Blocks.Add(b);
        foreach (var b in allBlocks) reverseCfg.BlockByOffset[b.StartOffset] = b;

        return reverseCfg;
    }

    /// <summary>
    /// 在任意图上计算立即支配树（通用的迭代数据流算法）。
    /// 复用了 ControlFlowScanner 的算法但适用于任意图对象。
    /// </summary>
    private static Dictionary<BasicBlock, BasicBlock> ComputeImmediateDominatorsOnGraph(
        ControlFlowGraph cfg)
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

    /// <summary>计算完整后支配集。</summary>
    private Dictionary<BasicBlock, HashSet<BasicBlock>> ComputePostDominanceSets(
        ControlFlowGraph cfg)
    {
        var dom = new Dictionary<BasicBlock, HashSet<BasicBlock>>();
        var allBlocks = new HashSet<BasicBlock>(cfg.Blocks);

        // 从后支配树构建完整后支配集：当前块 + 所有其后支配者
        foreach (var block in cfg.Blocks)
        {
            var set = new HashSet<BasicBlock> { block };
            var current = block;
            while (_postIdoms.TryGetValue(current, out var idom) && idom != current)
            {
                set.Add(idom);
                current = idom;
            }
            dom[block] = set;
        }

        return dom;
    }

    /// <summary>
    /// 跳转分类决策。
    /// 对应 uncompyle6 的 find_jump_targets 中的分类规则（scanner37base.py:643-651）。
    /// </summary>
    private static ComeFromType? ClassifyJump(Opcode op, int target, ControlFlowGraph cfg)
    {
        return op switch
        {
            // 条件跳转 → 产生 COME_FROM（条件分支的汇聚点）
            Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
                or Opcode.POP_JUMP_IF_NONE or Opcode.POP_JUMP_IF_NOT_NONE
                or Opcode.JUMP_IF_FALSE_OR_POP or Opcode.JUMP_IF_TRUE_OR_POP
                => ComeFromType.Conditional,

            // FOR_ITER → for 循环出口
            Opcode.FOR_ITER => ComeFromType.ForLoopEnd,

            // 以下不产生 COME_FROM（无条件转发/回边/异常入口）
            Opcode.JUMP_FORWARD or Opcode.JUMP_ABSOLUTE
                or Opcode.JUMP_BACKWARD or Opcode.JUMP_BACKWARD_NO_INTERRUPT
                or Opcode.SETUP_FINALLY or Opcode.SETUP_EXCEPT
                or Opcode.SETUP_LOOP or Opcode.SETUP_WITH
                => null,

            _ => null,
        };
    }
}
