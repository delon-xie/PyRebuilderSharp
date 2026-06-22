# try-except-else-finally 编译差异

> 基于 CPython 编译器源码分析（2.7 → 3.14）
> 来源：`Python/compile.c` (`compiler_try_except`, `compiler_try_finally`, `compiler_try`)

---

## 1. Python 2.7 — 3.10

### try/except/else

```
      │ SETUP_EXCEPT L1           // 设置异常处理，目标L1
      │ <try body>
      │ POP_BLOCK                 // try体结束
      │ JUMP_FORWARD orelse       // 无异常时跳向else体
      ├────────────────────────
L1:   │ DUP_TOP                   // 复制异常[tb, val, exc, exc]
      │ <evaluate E1>
      │ COMPARE_OP EXC_MATCH
      │ POP_JUMP_IF_FALSE L2      // 不匹配→下一handler
      │ POP                       // 移除exc
      │ <assign to V1> (or POP if no V1)
      │ POP                       // 移除tb
      │ <handler body>
      │ JUMP_FORWARD end          // 完成后跳向end
L2:   │ DUP_TOP ...
      │ ...
Ln+1: │ END_FINALLY               // 无handler匹配→重新抛出
orelse:│ <else body>               // ── else体在此 ──
end:   │ <next statement>
```

### try/finally

```
      │ SETUP_FINALLY end
      │ <try body>
      │ POP_BLOCK
      │ <finally body>            // 正常路径执行finally
      │ JUMP exit
end:  │                           // 异常或return时跳入
      │ <finally body>            // 异常路径执行finally
      │ END_FINALLY               // 恢复异常传播
exit: │
```

---

## 2. Python 3.5 — 3.10

### try/except/else

```
      │ SETUP_EXCEPT L1
      │ <try body>
      │ POP_BLOCK
      │ JUMP_FORWARD orelse      // 跳向else体
      ├────────────────────────
L1:   │ <evaluate E1>
      │ CHECK_EXC_MATCH
      │ POP_JUMP_IF_FALSE L2
      │ POP_TOP                  // 移除exc_value (2.7多了一层DUP)
      │ <store name> (if as V1)
      │ POP_TOP                  // 移除tb
      │ <handler body>
      │ POP_BLOCK                // 清理block stack
      │ POP_EXCEPT               // 清理异常状态
      │ JUMP_FORWARD end
L2:   │ ...
Ln+1: │ POP_EXCEPT               // handler链末尾清理
      │ RERAISE / END_FINALLY
orelse:│ <else body>              // ── else体在此 ──
end:   │
```

**变化 vs 2.7**：
- `CHECK_EXC_MATCH` 取代 `COMPARE_OP EXC_MATCH`
- `POP_EXCEPT` 新增（3.5专有，清理异常状态）
- 异常栈格式：`[exc, val, tb]` → `[exc, exc_info]`

### try/finally

```
      │ SETUP_FINALLY end
      │ <try body>
      │ POP_BLOCK
      │ <finally body>            // 正常路径
      │ LOAD_CONST None
      │ JUMP exit
end:  │
      │ <finally body>            // 异常路径
      │ END_FINALLY
exit: │
```

---

## 3. Python 3.11 (过渡版)

### try/except/else

```
      │ SETUP_FINALLY L1         // ← 3.11仍用SETUP
      │ <try body>
      │ POP_BLOCK
      │ <else body>              // ★ else体移入ET范围内 ★
      │ JUMP end
      ├────────────────────────
L1:   │ SETUP_CLEANUP cleanup    // ★ 新增: 异常路径用CLEANUP ★  
      │ PUSH_EXC_INFO            // ★ 新增: 推异常信息 ★
      │ <evaluate E1>
      │ CHECK_EXC_MATCH
      │ POP_JUMP_IF_FALSE L2
      │ STORE_NAME V1            // ★ 无POP_TOP层(3.11异常格式变化) ★
      │ <handler body>
      │ POP_BLOCK
      │ POP_EXCEPT
      │ LOAD_CONST None          // name = None; del name cleanup
      │ STORE_NAME V1
      │ DELETE_NAME V1
      │ JUMP end
L2:   │ ...
      │ RERAISE 0
cleanup:│ POP_EXCEPT_AND_RERAISE
end:   │
```

**关键变化**：
1. else 体从 handler 链后移至 POP_BLOCK 后（在 ET 范围内）
2. `SETUP_CLEANUP + PUSH_EXC_INFO` 标志异常路径入口
3. 异常栈格式简化（不再有 tb/val/exc 三层）
4. `SETUP_FINALLY` 仍存在（向后兼容，但 ET 已接管范围划分）

### try/finally

```
      │ SETUP_FINALLY end
      │ <try body>
      │ POP_BLOCK
      │ <finally body>           // 正常路径
      │ JUMP exit
end:  │ SETUP_CLEANUP cleanup
      │ PUSH_EXC_INFO
      │ <finally body>           // 异常路径
      │ RERAISE 0
cleanup:│ POP_EXCEPT_AND_RERAISE
exit:  │
```

**变化**：
- `END_FINALLY` → `RERAISE 0` / `POP_EXCEPT_AND_RERAISE`
- `SETUP_CLEANUP` 用于 finally 异常路径（与 `POP_EXCEPT_AND_RERAISE` 配对）

---

## 4. Python 3.12+ (ExceptionTable 原生)

### try/except/else

```
      │ NOP                      // ← 无SETUP_FINALLY
      │ <try body>
      │ <else body>              // ★ 同在ET范围内 ★
      │ JUMP end
      ├────────────────────────  // ExceptionTable: start~end → L1
L1:   │ SETUP_CLEANUP cleanup
      │ PUSH_EXC_INFO
      │ LOAD_GLOBAL E1
      │ CHECK_EXC_MATCH
      │ POP_JUMP_IF_FALSE L2
      │ STORE_NAME V1
      │ <handler body>
      │ POP_EXCEPT
      │ LOAD_CONST None
      │ STORE_NAME V1
      │ DELETE_NAME V1
      │ JUMP end
L2:   │ ...
      │ COPY 3 / POP_EXCEPT / RERAISE 1    // ★ 3.12 RERAISE模式 ★
cleanup:│ POP_EXCEPT_AND_RERAISE / COPY 3+POP_EXCEPT+RERAISE 1
end:   │
```

**关键变化**：
1. **无 SETUP_FINALLY/POP_BLOCK** — ExceptionTable 直接覆盖
2. `ET entry` = `{start, size → target, depth}` 取代 block stack
3. `RERAISE` 模式改为 `COPY 3, POP_EXCEPT, RERAISE 1`（3.12+）
4. `POP_EXCEPT_AND_RERAISE` 宏展开为相同模式

### try/finally

```
      │ <try body>
      │ <finally body>           // 正常路径（无POP_BLOCK）
      │ JUMP exit
      ├────────────────────────  // ExceptionTable覆盖
      │ SETUP_CLEANUP cleanup
      │ PUSH_EXC_INFO
      │ <finally body>
      │ RERAISE 0
cleanup:│ COPY 3 / POP_EXCEPT / RERAISE 1
exit:   │
```

---

## 5. else 体位置汇总

| 版本 | else 在 ET 范围内? | 检测方法 | 注意 |
|:-----|:-----------------:|:---------|:-----|
| 2.7-3.10 | ❌ 否，在 handler 链后 | 跟踪 try 体 `JUMP_FORWARD` → orelse | handler 链以 `END_FINALLY` / `POP_EXCEPT` + `RERAISE` 结尾 |
| 3.11 | ✅ 是，在 POP_BLOCK 后 | 在 tryBlocks 中找 `POP_BLOCK` 分界 | SETUP_FINALLY 仍存在作为辅助 |
| 3.12+ | ✅ 是，在 try 体后 | 在 tryBlocks 中找 `JUMP_FORWARD` 分界 | 无 POP_BLOCK，直接用 JUMP 标记边界 |

---

## 6. try/except/else/finally 嵌套检测规则

### 6.1 ET 条目过滤 (3.11+)

| 条目类型 | 特征 | 处理 |
|:---------|:-----|:------|
| try/except | handler 有 `CHECK_EXC_MATCH` | ✅ 构建 `Try` AST |
| with 条目 | entry 范围有 `BEFORE_WITH` | ❌ 跳过，with 独立构建 |
| for 循环体 | entry 范围匹配 `FOR_ITER` | ❌ 跳过，for 已处理 |
| finally-only | handler 无 `CHECK_EXC_MATCH` | ❌ 跳过，由 outer try 处理 |
| except handler 内部 | `STORE_NAME + SETUP_CLEANUP` | ❌ 跳过，是 name=cleanup 结构 |

### 6.2 else 检测流程

```
GetBlocksInRange(start, end) → tryBlocks
if version < 3.11:
    # else 在 handler 链后
    tryBody 末尾 JUMP_FORWARD → orelse_label
    handler 链末尾 JUMP_FORWARD → end_label
    blocks[orelse_label .. end_label] = else body
else:
    # else 在 tryBlocks 内
    find POP_BLOCK in tryBlocks (3.11)
    OR find JUMP_FORWARD in tryBlocks (3.12+)
    blocks before = try body
    blocks after = else body
```

### 6.3 finally 检测流程

```
if tryBlocks 尾部无 JUMP_FORWARD (fallthrough到finally):
    finally = True
    正常路径 = tryBlocks 后的代码
    异常路径 = handler 入口有 SETUP_CLEANUP+PUSH_EXC_INFO
```

---

## 7. 反编译实现策略

### `BuildTryFromExceptionTable` 修订

```
1. 获取 matchingEntry
2. 过滤非 try/except 条目
3. GetBlocksInRange(start, end) → rawBlocks
4. **分版本处理 else**:
   if version < 3.11:
       rawBlocks 只含 tryBody
       elseBody 从 handler 链后 JUMP_FORWARD 目标获取
   else:
       rawBlocks 含 tryBody + elseBody
       在 rawBlocks 中找 POP_BLOCK or JUMP_FORWARD 分界
5. 构建 handler（含 exceptType 提取）
6. 构建 elseBody
7. 构建 Try(tryBody, handlers, elseBody, finalBody)
```

### `BuildTryFromBlock` 修订（2.7-3.10）

```
1. 非 ET 模式：SETUP_EXCEPT → handler
2. 跟踪 try 体末尾 JUMP_FORWARD → orelse
3. 收集 handler 链后 blocks → elseBody
```

---

*分析基准：CPython v2.7, v3.5, v3.10, v3.11, v3.12, v3.13, v3.14 (main)*
