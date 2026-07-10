# 研读记录①: uncompyle6 COME_FROM 构建算法

> 来源: `python-uncompyle6/uncompyle6/scanners/scanner37base.py`
> 行号: 314~363 (COME_FROM 插入), 594~665 (find_jump_targets)
> 对应 PyRebuilderSharp: `Scanners/` 新增 PostDominatorScanner + ComeFromAnnotator

---

## 1. 核心算法

### 1.1 两步流程

uncompyle6 的 COME_FROM 构建分为**两步**：

```
Step A: find_jump_targets() → targets dict
Step B: 扫描 insts → 在 jump target 前插入 COME_FROM token
```

### 1.2 Step A: find_jump_targets (行 594~665)

```python
def find_jump_targets(self, debug: str) -> dict:
    targets = {}  # {target_offset: [source_offsets]}
    for i, inst in enumerate(self.insts):
        offset = inst.offset
        op = inst.opcode
        
        # 各种控制流检测
        self.detect_control_flow(offset, targets, i)
        
        if inst.has_arg:
            label = self.fixed_jumps.get(offset)
            oparg = inst.arg
            
            if label is None:
                if op in self.opc.hasjrel and op != self.opc.FOR_ITER:
                    label = next_offset + oparg  # 相对跳转
                elif op in self.opc.hasjabs:
                    if op in self.jump_if_pop:
                        if oparg > offset:
                            label = oparg  # 绝对跳转

            if label is not None and label != -1:
                targets[label] = targets.get(label, []) + [offset]
    
    return targets
```

**关键设计决策**：

| 决策 | 理由 |
|------|------|
| `op != FOR_ITER` 排除在外 | FOR_ITER 的跳转目标是循环出口，不是控制流汇聚点 |
| `hasjrel` vs `hasjabs` | 相对跳转（JUMP_FORWARD）和绝对跳转都追踪，但以 `jump_if_pop` 为条件 |
| `fixed_jumps` 覆盖 | END_FINALLY 也可能有 fixed jump → 异常处理路径也加入 |

### 1.3 Step B: COME_FROM 插入 (行 326~362)

```python
for i, inst in enumerate(self.insts):
    if inst.offset in jump_targets:
        # 按跳转来源 offset 倒序排列
        # 原因：更大的范围（外层结构）的 COME_FROM 应放最后，
        # 方便语法规则从外到内匹配
        for jump_offset in sorted(jump_targets[inst.offset], reverse=True):
            come_from_name = "COME_FROM"
            
            opname = self.opname_for_offset(jump_offset)
            if opname.startswith("SETUP_"):
                # SETUP_FINALLY → COME_FROM_FINALLY
                # SETUP_EXCEPT → COME_FROM_EXCEPT
                # SETUP_LOOP → COME_FROM_LOOP
                come_from_type = opname[len("SETUP_"):]
                come_from_name = "COME_FROM_%s" % come_from_type
            
            elif inst.offset in self.except_targets:
                come_from_name = "COME_FROM_EXCEPT_CLAUSE"
            
            # 插入 COME_FROM token
            tokens_append(Token(
                opname=come_from_name,
                attr=jump_offset,         # 跳转来源偏移
                offset="%s_%s" % (inst.offset, jump_idx),
            ))
```

**COME_FROM 名称分类规则**：

| 来源指令 | COME_FROM 名称 | 含义 |
|---------|---------------|------|
| 任意跳转 (无 SETUP_ 前缀) | `COME_FROM` | 普通条件跳转的汇聚点 |
| `SETUP_FINALLY` | `COME_FROM_FINALLY` | try-finally 的入口 |
| `SETUP_EXCEPT` | `COME_FROM_EXCEPT` | try-except 的 handler 入口 |
| `SETUP_LOOP` | `COME_FROM_LOOP` | 循环的入口 |
| (except target) | `COME_FROM_EXCEPT_CLAUSE` | except 子句内部的跳转汇聚 |

## 2. 对比 PyRebuilderSharp 现状

| 方面 | uncompyle6 | PyRebuilderSharp 现状 | 差距 |
|------|-----------|----------------------|------|
| COME_FROM 产生 | 条件跳转 + SETUP_* + FOR_ITER 排除 | 无此机制 | 需新增 |
| 跳转分类 | 按 opname 自动分类 (SETUP_* 前缀) | 无 | 需实现 `ShouldGenerateComeFrom()` |
| 排序 | 倒序（外层最后） | 无关 | 在标注阶段做到 |
| 使用 | 语法规则引擎 consume COME_FROM | SequentialBlock + 模式目录 | 验证器用 |

## 3. 在 PyRebuilderSharp 中的应用

### 3.1 ShouldGenerateComeFrom (等效于 uncompyle6 的 `hasjrel` + `hasjabs` - FOR_ITER)

```csharp
// 直接对应 uncompyle6 find_jump_targets 中的判断
private bool ShouldGenerateComeFrom(Opcode op) => op switch
{
    // 条件跳转 → 产生 COME_FROM（条件分支的汇聚点）
    Opcode.POP_JUMP_IF_FALSE or Opcode.POP_JUMP_IF_TRUE
        or Opcode.POP_JUMP_IF_NONE or Opcode.POP_JUMP_IF_NOT_NONE
        or Opcode.JUMP_IF_FALSE_OR_POP or Opcode.JUMP_IF_TRUE_OR_POP => true,
    
    // 注意：与 uncompyle6 不同，FOR_ITER 在这里也要产生 COME_FROM
    // 因为 Phase 2d 需要用它区分 for 循环和 while 循环的出口
    Opcode.FOR_ITER => true,
    
    // 无条件转发/回边 → 不产生
    Opcode.JUMP_FORWARD or Opcode.JUMP_ABSOLUTE
        or Opcode.JUMP_BACKWARD or Opcode.JUMP_BACKWARD_NO_INTERRUPT => false,
    
    // 异常处理入口 → 不产生（由 ExceptionTable 处理）
    Opcode.SETUP_FINALLY or Opcode.SETUP_EXCEPT
        or Opcode.SETUP_LOOP or Opcode.SETUP_WITH => false,
    
    _ => false
};
```

### 3.2 ComeFromType 分类

```csharp
// 等效于 uncompyle6 的 COME_FROM / COME_FROM_FINALLY / COME_FROM_EXCEPT / ...
public enum ComeFromType
{
    /// <summary>普通条件跳转</summary>
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
```

### 3.3 COME_FROM 在结构验证中的使用

```csharp
// 对应 uncompyle6 语法规则中的 COME_FROM consume：
// 例如 try-except 规则：try_body + COME_FROM_EXCEPT → handler
//
// 在 PyRebuilderSharp 中，COME_FROM 用于 StructuralValidator 的 R1-R5 规则：
//
// R1 [if-elif]: 多个条件跳转到同一个 COME_FROM → 应为 elif 链
// R2 [try]: COME_FROM_EXCEPT 标记 handler 入口 → 验证 body→handler 的后支配关系
// R3 [loop]: COME_FROM(FOR_ITER) 区分 for vs while
// R4 [else]: COME_FROM 目标与 else-body 后支配关系验证
```

---

## 4. 关键发现

### 4.1 uncompyle6 的 COME_FROM 是一种"标注"，不是"伪指令"

COME_FROM token 不参与字节码模拟，只在语法规则匹配时作为**上下文标记**。与 PyRebuilderSharp 的 Phase 2~4 annotation 标注有同样的设计理念。

### 4.2 排序策略很重要

> "We want to process COME_FROMs to the same offset to be in **descending** offset order so we have the larger range or biggest instruction interval last."

倒序排列确保外层结构的 COME_FROM 最后被插入（语法规则从外到内匹配）。PyRebuilderSharp 的标注应该也按此排序。

### 4.3 SETUP_* 特化成不同 COME_FROM 变体

uncompyle6 利用 `SETUP_FINALLY`/`SETUP_EXCEPT`/`SETUP_LOOP` 指令名自动分类。3.11+ 没有 SETUP_* 指令，PyRebuilderSharp 需要用 ExceptionTable 条目实现等效分类。

---

> **研读日期**: 2026-07-10
> **服务于**: Step 4 (后支配树 + COME_FROM 结构验证)
