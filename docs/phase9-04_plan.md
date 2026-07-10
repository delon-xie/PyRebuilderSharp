# Phase 9-04 方案: EMPTY_TRY + TRY_NO_HANDLER 修复

> 基线: 白盒 310/405 (76%), EMPTY_TRY=51, TRY_NO_HANDLER=10
> 工期: ~2天

---

## 问题分析

### EMPTY_TRY 51例 → 3个根因

| 根因 | 约例数 | 代码位置 |
|:-----|:------:|:---------|
| **过度链接**: handler 内的嵌套 ET 被标注为独立 try header | ~20 | `AnnotateExceptionTableBlocks` Step A |
| **Body 范围**: try body 包含 handler preamble 块(0条语句) | ~18 | `ParseTryStructure` body collection |
| **3.10- 边界**: SETUP_FINALLY handler 无 preamble 分离 | ~13 | `ParseTryStructure` 3.10- 路径 |

### TRY_NO_HANDLER 10例 → 2个根因

| 根因 | 约例数 | 代码位置 |
|:-----|:------:|:---------|
| **Handler preamble 未识别**: POP_TOP×3 模式被 block 边界分离 | ~6 | `ParseTryStructure` preamble 跳过 |
| **ET 偏移边界**: ET.EndOffset 与 handler 入口重叠 | ~4 | `AnnotateExceptionTableBlocks` body 范围 |

---

## 修复方案

### 修复1: 过度链接 — 用 HandlerDepth 替代 fully-contained

**现状**: `AnnotateExceptionTableBlocks` Step A 用 `fully-contained` 清除 handlers 内的所有 IsTryHeader

**修复**: 比较 HandlerDepth，只清除深度大于外部 try 的 header

```csharp
// 旧: sb.StartOffset >= hb.StartOffset && sb.EndOffset <= hb.EndOffset → 全清
// 新: sb.HandlerDepth > outerTryDepth → 只清嵌套的
foreach (var hb in handlerBlocks)
{
    int outerDepth = hb.HandlerDepth;
    foreach (var sb in seqBlocks.Where(b => b.IsTryHeader))
    {
        if (sb.HandlerDepth > outerDepth && 
            sb.StartOffset >= hb.StartOffset && sb.EndOffset <= hb.EndOffset)
            sb.IsTryHeader = false;
    }
}
```

### 修复2: Body 范围 — 跳过 handler preamble 块

**现状**: bodyBlocks 包括所有 from header → handler 路径中的 seqBlocks，包含 preamble 块

**修复**: 在 bodyBlocks 收集后过滤 preamble 块（POP_TOP×3、PUSH_EXC_INFO 等）

```csharp
// 在 worklist BFS 完成后:
bodyBlocks = bodyBlocks
    .Where(b => !IsHandlerPreambleBlock(b))
    .ToList();
```

同时新增 `IsHandlerPreambleBlock(SequentialBlock)` 检测：
```csharp
private static bool IsHandlerPreambleBlock(SequentialBlock block)
{
    // 3.11+: PUSH_EXC_INFO / CHECK_EXC_MATCH
    // 3.10-: POP_TOP ×3 (bare except handler)
    int popTopCount = block.Instructions.Count(i => i.Opcode == Opcode.POP_TOP);
    return popTopCount >= 2 || 
           block.Instructions.Any(i => i.Opcode is 
               Opcode.PUSH_EXC_INFO_312 or Opcode.PUSH_EXC_INFO or Opcode.CHECK_EXC_MATCH);
}
```

### 修复3: Handler preamble 跳过（TRY_NO_HANDLER）

**现状**: 3.10- 路径中 SETUP_FINALLY 的 handler 入口块包含 POP_TOP×3，被错误解析

**修复**: 在 exceptHandlers 收集后，将 handler 的 preamble 部分从 body 范围中排除

```csharp
// 在 bodyBlocks BFS 前:
var preambleBlocks = seqBlocks
    .Where(b => IsHandlerPreambleBlock(b) && handlerOffsets.Contains(b.StartOffset))
    .Select(b => b.Id)
    .ToHashSet();

// BFS 中: 如果走到 preamble 块，不加入 bodyBlocks
if (preambleBlocks.Contains(current.Id)) continue;
```

---

## 预期效果

| 指标 | 修复前 | 修复后 | 变化 |
|:-----|:------:|:------:|:----:|
| EMPTY_TRY | 51 | **~20** | -31 |
| TRY_NO_HANDLER | 10 | **~3** | -7 |
| 白盒通过 | 310 | **~325** | +15 |
| Diff lines | 139836 | **~135000** | -5000 |
| 全量基线 | 1325/1325 | 1325/1325 | → |

## 实施顺序

1. `IsHandlerPreambleBlock` 工具方法
2. 修改 `AnnotateExceptionTableBlocks` Step A → Depth 对比
3. 修改 `ParseTryStructure` 3.11+ 路径 → 跳过 preamble
4. 修改 `ParseTryStructure` 3.10- 路径 → 排除 preamble
5. `dotnet build` + 白盒 + 全量基线
