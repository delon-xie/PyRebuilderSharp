# 推导式修复进展（更新：2026-07-07）

## 已完成修复

### 查找列表推导式元素表达式修复

**LIST_APPEND 映射缺失** — 3.10 将 LIST_APPEND 从 opcode 18 移到 145，但 Opcode 枚举和 VersionStrategyPre311 未处理，导致指令被丢失。

修复：
1. `Opcode.cs`: 新增 `LIST_APPEND = 145` 枚举值
2. `StackMachine.cs`: 同步处理 `LIST_APPEND` 和 `LIST_APPEND_313`
3. `AstBuilder.cs`: 所有 `LIST_APPEND_313` 检查点增加 `LIST_APPEND` 检测（4 处）
4. `AstBuilder.cs`: 修正 `appendOpcode` 选择逻辑（根据 bodyBlocks 选择 313 或 310 变体）
5. `AstBuilder.cs`: 修正 elt 栈提取顺序（pop top 作为 elt，非第二个）
6. `AstBuilder.cs`: `BuildComprehensionFallback` 识别 Assign+ListComp 模式

### 效果

| 函数 | 之前 | 之后 | 状态 |
|:-----|:-----|:------|:----:|
| l6_2 生成器 | `(x for x in range(10))` | `(x * x for x in range(10))` | ✅ |
| l6_3 列表推导 | `[x for x in range(10)]` | `[x * x for x in range(10)]` | ✅ |
| l6_4 字典推导 | `{(k,v):(k,v) for _ in iterable}` | `{(k,v):(k,v) for _ in iterable}` | ❌ iterable/key |
| l6_5 嵌套推导 | `[_ for _ in iterable]` | `[_ for _ in iterable]` | ❌ |

**Level 6 diff**: 1196 → **1158** (↓38) 🎉

## 待修复（推导式）

| 问题 | 根因 | 估算 |
|:-----|:-----|:----:|
| 字典 key/value 错乱 | `BuildComprehensionFallback` 未正确处理 dict body 的 key/value 提取 | 2h |
| 推导式过滤条件 | `if x % 2 == 0` 在 elt 模拟中丢失 | 2h |
| 嵌套推导式 | 整体崩坏 | 3h |
