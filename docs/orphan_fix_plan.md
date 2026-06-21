# 孤儿块成因分析与 Phase 12 修正计划

## 1. 数据全景

| 文件 | v3.6 | v3.7 | v3.8 | v3.9 | v3.10 | v3.11 | v3.12 | v3.13 | v3.14 |
|:-----|:----:|:----:|:----:|:----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| **enum.py** | 263 | 652 | 653 | 652 | 79 | 66 | 59 | 56 | 51 |
| **functools.py** | - | - | 160 | 149 | 4 | 44 | 18 | 19 | 15 |

**核心发现**: 孤儿块分布分成两个截然不同的群体：

## 2. 群体一：v3.7-3.9（SETUP_FINALLY 模式） ~652 per version

**特征**: 
- 全部来自 `BuildTryFromBlock` 路径（SETUP_FINALLY-based try/except）
- `ExtractExceptHandlerFromOffset` 执行 BFS 收集 handler 链
- BFS 在 `POP_EXCEPT`/`END_FINALLY` 处停止
- **Nested try/except**: 内层 handler 块的继承者链未被 BFS 覆盖

**示例**: `enum.py::__new__` 中：
```python
# 原始代码类似 (简化):
try:
    ...
    try:          ← 内层 try
        ...
    except A:    ← 内层 handler — BFS 可能遗漏
        ...
    except B:    ← 内层 handler 链 — 完全遗漏
        ...
except:
    ...
```

**根因**: `ExtractExceptHandlerFromOffset` 从 handler Entry 开始 BFS。对于 `try: ... except A: ... except B: ...`：
- Handler A 的入口块被 BFS 覆盖
- `JUMP_IF_NOT_EXC_MATCH` 的跳转目标（Handler B 入口）可能不在 BFS 路径中
- 因为 BFS 在 `POP_EXCEPT`/`END_FINALLY` 处停止，而 Handler A 的 `POP_EXCEPT` 块的后继不被跟踪

**解决思路**: 不再依赖 BFS，而是用 **SETUP_FINALLY 参数计算的 handler 范围** 来批量标记所有在 `[handlerAbs, handlerAbs + range)` 范围内的块为 `_processedBlockIds`。

## 3. 群体二：v3.10+（ExceptionTable 模式） ~50-80 per version

**特征**:
- 远少于群体一
- 集中在 `_test_simple_enum` (30-35 orphans/version)
- `FindBlocksFromOffset` 使用 BFS，受限于 Handler Life Range

**示例**: `_test_simple_enum` 中的异常处理链中包含 `END_FINALLY`/`POP_EXCEPT`，BFS 在此停止，遗漏了后面的 handler 块。

## 4. 修正计划

### 方案 A：范围标记法（高风险，收益大）

在 `BuildTryFromBlock` 和 `BuildTryFromExceptionTable` 完成 handler 处理后，额外标记 handler 范围内的所有块：

```csharp
// 1. 计算 handler 范围
int handlerStart = handlerAbs;
int handlerEnd = codeObject.GetHandlerEnd(handlerAbs);

// 2. 标记范围内所有未标记的块
foreach (var block in cfg.Blocks)
{
    if (block.StartOffset >= handlerStart && block.StartOffset < handlerEnd)
        _processedBlockIds.Add(block.Id);
}
```

**风险**: 可能错误标记本应属于正常 flow 的块（函数定义、类定义等），导致输出丢失内容。

**缓解**: 排除包含 `MAKE_FUNCTION`、`LOAD_BUILD_CLASS` 的块。

### 方案 B：增强 BFS（中风险，中收益）

改进 `ExtractExceptHandlerFromOffset` 的 BFS：
1. 不只在 `POP_EXCEPT`/`END_FINALLY` 处停止，而是继续跟踪这些块的后继
2. 但只跟踪到 handler 范围内的后继
3. 对 `JUMP_IF_NOT_EXC_MATCH` 的目标块也跟踪（正确处理多 except 链）

**风险**: BFS 可能过度跟踪到正常代码块。

### 方案 C：残余孤儿后处理（低风险，低收益）

在 orphan 恢复阶段，对不是 handler preamble 但内容看起来是 handler body 的孤儿块也跳过：
- 检查 orphan 块是否同时包含 `POP_EXCEPT` 或 `END_FINALLY` 以及赋值语句
- 内容看似 handler body（如 `pass`、`return`、常量）且被正常 flow 中的 try/except 覆盖

**风险**: 低，但收益也低（只能清除非 handler preamble 的 handler 块）。

## 5. 推荐方案

**方案 A + 安全的例外排除**：
1. 在 `BuildTryFromBlock` 返回后（即 caller 的 handler 标记前后），计算 handler 范围
2. 标记范围内所有非函数/类定义的块为 `_processedBlockIds`
3. 同时保留现有的 BFS 标记（`ExtractExceptHandlerFromOffset` 中的 `_processedBlockIds.Add`）

**预期收益**:
- v3.7-3.9 enum.py: ~1950 orphans → ~200（减 ~1750）
- v3.10+ enum.py: ~300 orphans → ~100（减 ~200）
- functools.py: ~300 orphans → ~50（减 ~250）
- 总计: ~3967 → ~1800（减 ~2200，约 55%）
