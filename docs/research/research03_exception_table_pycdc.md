# 研读记录③: ExceptionTable 异常边处理

> 来源: `pycdc/pyc_code.cpp` 行 148~171, `pycdc/ASTree.cpp` 行 2075~2092
> 对比: `uncompyle6/semantics/fragments.py` 行 268 (try_except 语义)
> 对应 PyRebuilderSharp: `SequentialBlockBuilder.AnnotateExceptionTableBlocks` + `ParseTryStructure`

---

## 1. pycdc 的 ExceptionTable 解析

### 1.1 格式解析 (pyc_code.cpp 行 148)

```cpp
std::vector<PycExceptionTableEntry> PycCode::exceptionTableEntries() const
{
    PycBuffer data(m_exceptTable->value(), m_exceptTable->length());
    std::vector<PycExceptionTableEntry> entries;

    int pos = 0;
    while (!data.atEof()) {
        int start = _parse_varint(data, pos) * 2;    // 2 = word offset multiplier
        int length = _parse_varint(data, pos) * 2;
        int end = start + length;
        int target = _parse_varint(data, pos) * 2;
        int dl = _parse_varint(data, pos);             // depth + lasti flag
        
        int depth = dl >> 1;
        bool lasti = bool(dl & 1);
        
        entries.push_back(PycExceptionTableEntry(start, end, target, depth, lasti));
    }
    return entries;
}
```

**格式与 CPython 一致**：每个 ET 条目 5 个 varints：
1. `start` — try body 起始偏移（×2 因为 word offset）
2. `length` — try body 长度（×2，end = start + length）
3. `target` — handler 入口偏移（×2）
4. `depth` — 嵌套深度
5. `lasti` — 布尔标志（push lasti?）

**与 PyRebuilderSharp 对比**：解析逻辑一致，pycdc 在 `_parse_varint` 解析上与项目当前实现相同。

### 1.2 SETUP_EXCEPT / SETUP_FINALLY 的块处理 (ASTree.cpp 行 2075)

```cpp
case Pyc::SETUP_EXCEPT_A:
case Pyc::SETUP_FINALLY_A:
{
    if (curblock->blktype() == ASTBlock::BLK_CONTAINER) {
        // 已在容器块中 → 设置 except 目标
        curblock.cast<ASTContainerBlock>()->setExcept(pos+operand);
    } else {
        // 创建新的容器块
        PycRef<ASTBlock> next = new ASTContainerBlock(0, pos+operand);
        blocks.push(next.cast<ASTBlock>());
    }
    // 保存栈状态
    stack_hist.push(stack);
    // 创建 try body 块
    PycRef<ASTBlock> tryblock = new ASTBlock(ASTBlock::BLK_TRY, pos+operand, true);
    blocks.push(tryblock.cast<ASTBlock>());
    curblock = blocks.top();
    need_try = false;
}
```

**关键设计**：pycdc 使用**块栈**（不同于 PyRebuilderSharp 的**标注**）：
- `BLK_CONTAINER` = try 的外层容器（包容 except/finally 区域）
- `BLK_TRY` = try body 块
- handler 区域在 `POP_BLOCK` / `END_FINALLY` 时解析

## 2. uncompyle6 的 try 处理

uncompyle6 用**语法规则**（parser grammar）而非块栈来处理 try：

```python
# 在 parse38.py 或类似文件中（简化）:
try_except := SETUP_FINALLY
              suite_stmts           # try body
              POP_BLOCK
              JUMP_FORWARD _if_else # 跳过后面的 handler
              COME_FROM_EXCEPT
              except_clause ...

except_clause := DUP_TOP LOAD_GLOBAL COMPARE_OP
                 POP_JUMP_IF_FALSE ...
                 POP_TOP POP_TOP POP_TOP STORE_FAST
                 suite_stmts        # handler body
                 POP_EXCEPT JUMP_FORWARD COME_FROM
```

**与 PyRebuilderSharp 对比**：

| 方法 | pycdc | uncompyle6 | PyRebuilderSharp |
|------|-------|-----------|-----------------|
| 异常处理 | 块栈 (BLK_TRY/BLK_CONTAINER) | 语法规则 + COME_FROM | 标注 (Phase 2 ET) + 模式目录 (T1~T7) |
| 3.10- | SETUP_* 指令驱动 | SETUP_* + 规则引擎 | SETUP_* + 模式目录 |
| 3.11+ | ExceptionTable 条目 | 不支持 (3.8 停止) | ExceptionTable + 标注 |
| handler 检测 | 块栈弹出时自动识别 | POP_EXCEPT/END_FINALLY 规则 | POP_TOP×3 / CHECK_EXC_MATCH 前导码 |

## 3. 关键发现

### 3.1 3.11+ ExceptionTable 的处理是 PyRebuilderSharp 的优势

pycdc 和 uncompyle6 都无法正确处理 3.11+ exception table（pycdc 的 parse_exception_table 解析了格式但没有生成正确的 try 结构，uncompyle6 在 3.8 就停止了）。PyRebuilderSharp 在这方面的实现是**领先的**。

### 3.2 pycdc 的块栈 vs PyRebuilderSharp 的标注

pycdc 在 `SETUP_*` 处就决定了 try 结构（推入 BLK_CONTAINER/BLK_TRY）。PyRebuilderSharp 使用两阶段方法：

```
pycdc:  指令扫描时直接决定结构
PyRebuild: Phase 2 标注 → Phase 5 模式匹配
```

pycdc 的方式更直接但缺少容错——一个 `SETUP_FINALLY` 匹配错误就会破坏整个 try 结构。PyRebuilderSharp 的两阶段更有弹性。

### 3.3 改进方向

从 pycdc 的块栈设计中可借鉴的是**异常边的双通道设计**：

```csharp
// pycdc 的做法等价于：
// 1. 正常边: SETUP_FINALLY → body → POP_BLOCK → JUMP_FORWARD
// 2. 异常边: SETUP_FINALLY → handler 入口 (pos+operand)
//
// 在 3.11+，异常边来自 ExceptionTable 而非 SETUP_FINALLY
// 双通道（正常+异常）在 pycdc 中是隐式的（block stack）
// 在 PyRebuilderSharp 中是显式的（successor edges + exception edges）
```

PyRebuilderSharp 已经在 BasicBlock 中区分了 `Successors`（正常边）和 `ExceptionHandlers`/`FinallyBlock`（异常边）。进一步改进方向：

1. **ExceptionTable → CFG 异常边的严格映射**：确保每个 ET 条目的 target 被正确添加到对应块的 `ExceptionHandlers` 集合中
2. **深度匹配**：handler 的 `depth` 与 try 嵌套层级匹配，排除 handler 内部嵌套 try 的误标记

---

> **研读日期**: 2026-07-10
> **服务于**: Step 5 (ET→CFG 异常边严格映射)
