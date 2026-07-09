# 控制块字节码模式目录

## 设计目标

建立完整的控制块字节码模式→标注映射表，明确：
1. 每种模式的字节码指纹
2. 标注层面的识别点（哪些标注一锤定音，哪些需要多个标注联合判断）
3. 歧义处理（两种结构共享同一种字节码布局时如何区分）

---

## 1. Try/Except/Else/Finally 模式

### 1.1 原子模式

```
try-body:   SETUP_FINALLY / ExceptionTable entry → POP_BLOCK
handler:    [handler preamble] → [handler body] → POP_EXCEPT / RERAISE
else-body:  POP_BLOCK 后的平坦代码 → JUMP_FORWARD 跳过 handler
finally:    POP_EXCEPT / RERAISE → [finally body] → END_FINALLY / RERAISE
```

### 1.2 组合模式

| # | 源码模式 | 字节码序列 | 标注指纹 | 3.11+ 差异 |
|---|---------|-----------|---------|-----------|
| **T1** | try-except (bare) | `SETUP_FINALLY → body → POP_BLOCK → JUMP_FWD → handler: POP×4 → body → POP_EXCEPT` | `IsTryHeader=true, handler preamble=POP_TOP×4` | ExceptionTable 替代 SETUP_FINALLY |
| **T2** | try-except (typed) | `SETUP_FINALLY → body → POP_BLOCK → JUMP_FWD → handler: DUP_TOP → LOAD_GLOBAL → CMP_OP → POP_JUMP_IF_FALSE → next_handler → POP×3 → body → POP_EXCEPT` | `IsTryHeader=true, handler preamble=DUP_TOP+LOAD_GLOBAL` | CHECK_EXC_MATCH 替代 DUP_TOP+LOAD_GLOBAL |
| **T3** | try-except (named) | T2 + `STORE_FAST var` 在 POP×3 后 | 同 T2 + `bodyStartIdx 后移` | CHECK_EXC_MATCH 后 STORE_FAST |
| **T4** | try-except-else | T1 + else-body 在 POP_BLOCK 和 JUMP_FWD 之间 | `POP_BLOCK 后 → else-body → JUMP_FWD` | ET 的 try end 与 handler start 之间 |
| **T5** | try-except-finally | T1 + finally: `POP_EXCEPT → POP_BLOCK → finally-body → END_FINALLY` | `IsFinallyBlock=true, handler 后有 END_FINALLY` | ET 的 IsFinally 条目 |
| **T6** | try-except-else-finally | T4 + T5 组合 | 综合 T4+T5 | ET 多条目 |
| **T7** | try-finally | `SETUP_FINALLY → body → POP_BLOCK → LOAD_CONST None → JUMP_FWD → handler: [finally-body] → END_FINALLY` | `IsTryHeader=true, handler 无 POP_TOP×3 开头, 有 END_FINALLY` | ET IsFinally 条目 |

### 1.3 歧义与区分

| 歧义 | 两个候选 | 区分方法 |
|------|---------|---------|
| POP_TOP×3 是 handler preamble 还是普通语句 | handler body / 普通语句 | `DUP_TOP` 或 `PUSH_EXC_INFO` 在其前？如无，看是否在 SETUP_FINALLY target 之后 |
| POP_BLOCK 后是 else-body 还是 exit 代码 | T4 else / 普通 exit | handler 是否有 POP_EXCEPT？else-body 在 handler 跳转目标之前？ |
| END_FINALLY 是 finally 结束还是 except 结束 | T7 finally / T1 except | handler preamble 是 POP_TOP×3 还是直接 body？ |
| 多个 except handler 是同一 try 的还是嵌套 try 的 | 并列 except / 嵌套 try | ET Depth 值；SETUP_FINALLY 的目标块是否重叠 |

### 1.4 标注策略

```
Phase 2c HandlerDepth 标注:
  - IsFinallyBlock = true → 此块是 finally handler（不是 except）
  - HandlerDepth = 0/1/2 → 嵌套深度（用于区分并列 vs 嵌套）

Phase 2 ExceptionTryStart/EndOffset:
  - tryStart 到 tryEnd 之间的块是 try body
  - 第一个 handler 的 StartOffset = tryEnd → body 结束
  - handler 后、finally 前的块 → else 候选 (IsTryElseBlock)

Phase 3b 出口标注:
  - try body 后的 JUMP_FORWARD 目标 → try 出口
  - handler 后的 JUMP_FORWARD → try 出口（与上一个相同则为 else）
  - POP_EXCEPT 后紧接 JUMP_FORWARD → 无 else（跳转到函数结束）
```

---

## 2. For 循环模式

### 2.1 原子模式

```
for-header:  GET_ITER → FOR_ITER exit
for-body:    FOR_ITER 后继 → [body] → JUMP_ABSOLUTE (回 FOR_ITER)
for-else:    FOR_ITER 目标块 → [else-body]
```

### 2.2 组合模式

| # | 源码模式 | 字节码序列 | 标注指纹 |
|---|---------|-----------|---------|
| **F1** | for (基本) | `GET_ITER → FOR_ITER exit → body → JUMP_ABS → 头` → `exit:` | `IsForLoopHeader=true, ForIterExitTarget=exit` |
| **F2** | for-else | 同 F1 + `exit: [else-body]` | `ForIterExitTarget 的块后继是 else-body` |
| **F3** | for+break | F1 body 中包含 `POP_TOP → JUMP_ABS exit` | `IsBreakTarget=exit` |
| **F4** | for+continue | F1 body 中包含 `JUMP_ABS 循环头` | `IsContinueTarget=循环头` |

### 2.3 歧义与区分

| 歧义 | 区分方法 |
|------|---------|
| FOR_ITER 的 exit target 是 else 还是 end | exit 后的块是否有 SETUP_FINALLY/另一个控制结构头？无则为 end |
| for body 中的 POP_TOP 是 break 还是普通表达式 | body 中且目标为 FOR_ITER exit → break；否则 POP_TOP |
| 多层 for 嵌套（FOR_ITER × N） | 内层 FOR_ITER 先处理（offset 逆序） |

### 2.4 标注策略

```
Phase 2b For/While 细分:
  - FOR_ITER 存在 → IsForLoopHeader = true
  - FOR_ITER.Argument → ForIterExitTarget = exit offset
  - 第一个后继 → IsForIterBody = true

Phase 4 回边:
  - body 内的 JUMP_ABSOLUTE → 回边（指向 IsForLoopHeader）
  - body 内 JUMP_ABSOLUTE 指向 exit → break

Phase 3b:
  - ForIterExitTarget → IsBreakTarget
  - IsForLoopHeader → IsContinueTarget
```

---

## 3. While 循环模式

### 3.1 原子模式

```
while-header: POP_JUMP_IF_FALSE exit + 回边 → 循环头
while-body:   条件为真时的后继 → [body] → JUMP_ABSOLUTE 回边
```

### 3.2 组合模式

| # | 源码模式 | 字节码序列 | 标注指纹 |
|---|---------|-----------|---------|
| **W1** | while (基本) | `条件 → POP_JUMP_IF_FALSE exit → body → JUMP_ABS 头` | `IsLoopHeader=true, IsBackEdgeTarget=true` |
| **W2** | while-else | W1 + exit 后有 else-body | exit 后不是 RETURN/RAISE → else |
| **W3** | while+break | W1 body 含 `POP_TOP → JUMP_ABS exit` | `IsBreakTarget=exit` |
| **W4** | while+continue | W1 body 含 `JUMP_ABS 循环头` | `IsContinueTarget=循环头` |

### 3.3 歧义与区分

| 歧义 | 区分方法 |
|------|---------|
| POP_JUMP_IF_FALSE 是 while 还是 if | 是否有回边？`IsBackEdgeTarget=true` → while；否则 → if |
| while True:（无限循环） | 条件为 `LOAD_CONST True` 且无条件跳回 |
| while 条件含 and/or | 短路条件的 JUMP_IF 链需要整体作为条件表达式 |

### 3.4 标注策略

```
Phase 2b:
  - 非 FOR_ITER 的 IsLoopHeader + IsBackEdgeTarget → IsWhileLoopHeader

Phase 4:
  - IsBackEdgeTarget 的源头 block → 循环体
```

---

## 4. If/Elif/Else 模式

### 4.1 原子模式

```
if-header:   POP_JUMP_IF_FALSE else_/exit（无回边）
true-body:   条件为真时的后继 → [body] → JUMP_FORWARD exit
false-body:  else_/exit → [else/elif body]
```

### 4.2 组合模式

| # | 源码模式 | 字节码序列 | 标注指纹 |
|---|---------|-----------|---------|
| **I1** | if (无 else) | `条件 → POP_JUMP_IF_FALSE exit → [true-body] → exit:` | `IsConditionHeader=true, 无后继 JUMP_FORWARD` |
| **I2** | if-else | `条件 → POP_JUMP_IF_FALSE else → [true-body] → JUMP_FWD exit → else: [false-body] → exit:` | `IsConditionHeader=true, 有 JUMP_FWD, else 块存在` |
| **I3** | if-elif-else | I2 中 else-body 以另一个 POP_JUMP_IF_FALSE 开头 | `false-body 的首指令是 IsConditionHeader` |
| **I4** | 3.11+ inline-if | `JUMP_IF_FALSE_OR_POP → ... → JUMP_IF_TRUE_OR_POP` | `IsConditionHeader=true, OR_POP 变体` |

### 4.3 歧义与区分

| 歧义 | 区分方法 |
|------|---------|
| POP_JUMP_IF_FALSE 是 while 还是 if | `IsBackEdgeTarget` 检查——目标块是否在指令之前 |
| true-body 后的 JUMP_FORWARD 是否跳到 else 的结尾 | `FindMergePoint` 计算 true/false 分支的汇聚点 |
| if-elif-else 中的 elif 是嵌套 if 还是 elif | 如果 false-body 也以 POP_JUMP_IF_FALSE 开头 → elif |

### 4.4 标注策略

```
Phase 3:
  - POP_JUMP_IF_* + 无回边 → IsConditionHeader

Phase 3b:
  - 条件分支的两条后继 → 计算汇聚点 IsMergePoint
  - true-body 的 JUMP_FORWARD 目标 = merge point
  - false-body 的结束 = merge point
```

---

## 5. With 语句模式

### 5.1 原子模式

```
with-header: LOAD_CONTEXT → SETUP_WITH/BEFORE_WITH/LOAD_SPECIAL → POP_TOP
with-body:   header 后继 → POP_BLOCK → [cleanup]
```

### 5.2 组合模式

| # | 源码模式 | 字节码序列 | 标注指纹 |
|---|---------|-----------|---------|
| **S1** | with（3.10-） | `LOAD_NAME ctx → SETUP_WITH → POP_TOP → body → POP_BLOCK → LOAD_CONST None → JUMP_FWD → handler: cleanup → END_FINALLY` | `HasSetupWith=true` |
| **S2** | with-as (3.10-) | S1 + `STORE_FAST var` 在 POP_TOP 后 | 同上 + POP_TOP 后的 STORE_FAST |
| **S3** | with（3.11+） | `LOAD_FAST_BORROW_314 → COPY → LOAD_SPECIAL → SWAP → SWAP → LOAD_SPECIAL → CALL → POP_TOP → body` | `HasBeforeWith/HasLoadSpecial` |
| **S4** | with-as (3.11+) | S3 + `STORE_FAST var` | `IsWithHeader=true` |

### 5.3 歧义与区分

| 歧义 | 区分方法 |
|------|---------|
| SETUP_WITH vs SETUP_FINALLY | 操作码本身不同（Opcode.SETUP_WITH vs Opcode.SETUP_FINALLY） |
| 3.11+ 的 LOAD_SPECIAL 序列是否是真 with | 需要 LOAD_FAST_BORROW_314 + COPY + LOAD_SPECIAL + SWAP×2 + LOAD_SPECIAL + CALL 完整 7 模式 |

---

## 6. Match/Case 模式（3.10+）

### 6.1 原子模式

```
match-header: MATCH_KEYS / MATCH_CLASS / MATCH_MAPPING → [subject 表达式]
case-entry:   JUMP_IF_NOT_EXC_MATCH 目标 → [preamble → body → POP_EXCEPT → JUMP_FWD end]
```

### 6.2 标注策略

```
Phase 2a:
  - MATCH_KEYS/CLASS/MAPPING → IsMatchHeader
  - JUMP_IF_NOT_EXC_MATCH 目标 → IsCaseEntry
```

---

## 7. 歧义优先级总表

| 歧义场景 | 优先规则 | 确认标注组合 |
|---------|---------|------------|
| POP_JUMP_IF_FALSE → while vs if | **回边优先** | `IsBackEdgeTarget=true → While; else → If` |
| POP_JUMP_IF_* → for-else exit vs if | **FOR_ITER 优先** | `IsForLoopHeader 已处理 → for-else exit 已被包含` |
| SETUP_FINALLY → except vs finally | **handler preamble 优先** | `POP_TOP×3/DUP_TOP → except; 直接 body → finally` |
| 多个 POP_JUMP_IF_* → elif vs 独立 if | **连续优先** | `false-body 首指令也是 IsConditionHeader → elif` |
| POP_BLOCK 后 → else vs exit | **handler 跳转优先** | `handler 的 JUMP_FORWARD 目标 = exit, else-body 在 exit 前` |

---

## 8. 对标注系统的总结

### 确定性标注（无需歧义判断）

| 标注 | 决定条件 | 一票否决 |
|------|---------|---------|
| `IsForLoopHeader` | 存在 FOR_ITER | ✅ |
| `IsWithHeader` | SETUP_WITH / LOAD_SPECIAL 7 模式 | ✅ |
| `IsMatchHeader` | MATCH_KEYS/CLASS/MAPPING | ✅ |
| `IsFinallyBlock` | ET IsFinally=true / handler 无 POP_TOP×3 | ✅ |
| `ForIterExitTarget` | FOR_ITER.Argument | ✅ |
| `IsBackEdgeTarget` | JUMP_ABSOLUTE 目标在之前 | ✅ |

### 条件性标注（需多个标注联合判断）

| 标注 | 依赖 | 歧义条件 |
|------|------|---------|
| `IsWhileLoopHeader` | `IsLoopHeader + !IsForLoopHeader + IsBackEdgeTarget` | 非 FOR_ITER 的 IsLoopHeader |
| `IsConditionHeader` | `POP_JUMP_IF_* + !IsLoopHeader` | while 和 if 共享此指令 |
| `IsTryElseBlock` | `handler 后 + finally 前 + handler 跳转目标 != exit` | 需确定 handler 的跳出点 |
| `IsBreakTarget` | `for/while body 内 JUMP_ABSOLUTE → exit` | 需 body 范围已标注 |
| `IsMergePoint` | `两个分支的后继汇聚` | 需两个分支均已链接 |
