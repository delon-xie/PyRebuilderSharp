# Phase Fix 收尾总结 — PyRebuilderSharp

**版本**: v1.0
**日期**: 2026-06-14
**项目**: PyRebuilderSharp (.NET 10 + Avalonia GUI)

---

## 一、修复清单

### Phase 3 (marshal) — 全部 ✅ 关闭

| # | 问题 | 根因 | 修复 |
|:-:|:-----|:------|:------|
| 1 | co_names 为空 → `name_X` | `ReadRawMarshalBytes` 漏 TYPE_REF | 新增 `ReadRefAndReturnBytes` |
| 2 | abc.3.12 `from name_8` | TYPE_REF stream 偏移 | 同上 |
| 3 | `class __name__:` | co_names 错位 | 同上 |

### Phase 4 (语法) — 全部 ✅ 关闭

| # | 问题 | 根因 | 修复 |
|:-:|:-----|:------|:------|
| 4 | class 定义 → `Foo = 'Foo'` | Opcode 枚举 ROT_TWO=2 ↔ PUSH_NULL=2 冲突 | `case ROT_TWO` 检测 `_isPython312` |
| 5 | `x = f()` → `x = f` | `GetCacheCount312` 错表 | `ParseInstructions311Plus` 只跳过 `rawOp==0` |

### Phase 5 (测试) — 全部 ✅ 关闭

| # | 测试 | 修复 |
|:-:|:------|:------|
| 6 | StackMachineTests × 2 | 用例更新：UnknownOpcode→SilentlyIgnored, BinaryAdd→PopExpr |
| 7 | TokenDumperTests × 1 | 计数 5→4, 索引 4→3 |

---

## 二、三项关键架构修复

### 1. `ROT_TWO = 2` ↔ `PUSH_NULL = 2` 枚举冲突

Opcode 枚举中 `ROT_TWO = 2` (Python 3.10-) 与 `PUSH_NULL = 2` (Python 3.11+) 共享同一 C# 枚举值。StackMachine 的 default case 将 PUSH_NULL 吞掉 → null sentinel 缺失 → CALL 从错误位置弹栈 → `Call` AST 节点不产生。

**修复**：`case Opcode.ROT_TWO:` 中检查 `_isPython312`，是则推入 sentinel。

### 2. `GetCacheCount312` 错表

3.12 的 cache 条目数从 Python 源码 `Python/opcode_targets.h` 派生，但与实际 Python 3.12 编译输出不一致（`LOAD_CONST=1` 但实际 0 cache, `LOAD_NAME=4` 但实际 0 cache）。

**修复**：`ParseInstructions311Plus` 不再信任 cache 表，改为只跳过 `rawOp==0`（CACHE 标记）。

### 3. `ReadRawMarshalBytes` 漏 TYPE_REF

CPython 的 `r_object()` 处理所有 code object 字段为通用 marshal 对象，包括 TYPE_REF(0x72)。C# 的 `ReadRawMarshalBytes` 只处理 TYPE_STRING/BYTES/SHORT_ASCII，遗漏 TYPE_REF→stream 偏移 4 字节→co_names 为空。

**修复**：新增 `ReadRefAndReturnBytes` 处理 TYPE_REF。

---

## 三、经验教训

1. **CPython 源代码是最高权威** — 三个 bug 均可在 5 分钟内用 CPython `marshal.c` / `ceval.c` / `Include/opcode.h` 定位，各浪费 2-3 小时在第三方文档和推理猜测上。
2. **Opcode 枚举冲突预防** — 添加共享 raw byte 的 opcode 时，StackMachine switch 必须明确处理。
3. **Cache 表不可信** — Python 3.12 的 cache 条目数在不同微版本间可能变化，应只跳过 `rawOp==0` 而非预计算 cache 数。

---

## 四、剩余工作（Phase Fix 6 项）

| 项目 | 优先级 |
|:-----|:------|
| `match/case` (3.10+) | 🔴 高 |
| `except*` (3.11+) | 🔴 高 |
| walrus `:=` (3.8+) | 🟢 低 |
| AST 自动对比验证 | 🟡 中 |
| CrashCollector Dashboard | 🟡 中 |
| 批量反编译模式 | 🟢 低 |
