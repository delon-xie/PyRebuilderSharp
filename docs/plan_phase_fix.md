# Phase Fix 计划 — 未完成任务清单

**日期**: 2026-06-14
**原则**: 优先修复/关闭 Phase 3/4/5 问题，其余移入 Phase Fix 待后续解决

---

## 一、Phase 3 遗留问题（已修复）

| # | 问题 | 难度 | 状态 |
|:-:|:-----|:-----|:------|
| P3-1 | module `co_names` 被 marshal TYPE_REF 耗尽 → `name_X` | 🔴 高 | ✅ **已修复** |
| P3-2 | abc.3.12 7个嵌套代码对象累积偏移 → `from name_8 import` | 🔴 高 | ✅ **已修复** |
| P3-3 | `class __name__:` 类名显示错误 | 🔴 高 | ✅ **已修复** |

## 二、Phase 4 遗留问题（语法覆盖）

| # | 问题 | 难度 | 决定 |
|:-:|:-----|:-----|:-----|
| P4-1 | `match/case` (3.10+) | 🔴 高 | **移入 Phase Fix** |
| P4-2 | `except*` (3.11+) | 🔴 高 | **移入 Phase Fix** |
| P4-3 | walrus `:=` (3.8+) | 🟢 低 | **移入 Phase Fix** |

## 三、Phase 5 遗留问题（工程增强）

| # | 问题 | 难度 | 决定 |
|:-:|:-----|:-----|:-----|
| P5-1 | AST 自动对比验证 | 🟡 中 | **移入 Phase Fix** |
| P5-2 | CrashCollector Dashboard (GUI) | 🟡 中 | **移入 Phase Fix** |
| P5-3 | 批量反编译模式 | 🟢 低 | **移入 Phase Fix** |

## 四、预存测试失败（立即修复）

| # | 测试 | 难度 | 决定 |
|:-:|:-----|:-----|:-----|
| T-1 | `StackMachineTests.Execute_UnknownOpcode_ThrowsNotSupported` | 🟢 低 | **立即修复** |
| T-2 | `StackMachineTests.Execute_BinaryAdd_ReturnsBinOpOnPop` | 🟢 低 | **立即修复** |
| T-3 | `TokenDumperTests.Tokenize_SimpleAssign_TokensAreCorrect` | 🟢 低 | **立即修复** |

---

## 五、执行计划

### ✅ 已修复

| 项目 | 来源 | 状态 |
|:-----|:-----|:------|
| marshal TYPE_REF 偏移 (P3-1/2/3) | Phase 3 | ✅ **已修复** — `ReadRawMarshalBytes` 新增 TYPE_REF 处理 |
| StackMachineTests (T-1/T-2) | 测试 | ✅ **已修复** |
| TokenDumperTests (T-3) | 测试 | ✅ **已修复** |

### 🔴 移入 Phase Fix（不阻塞关闭）

| 项目 | 来源 | 优先级 |
|:-----|:-----|:------|
| `match/case` (3.10+) | Phase 4 | 🔴 高 |
| `except*` (3.11+) | Phase 4 | 🔴 高 |
| walrus `:=` (3.8+) | Phase 4 | 🟢 低 |
| AST 自动对比验证 | Phase 5 | 🟡 中 |
| CrashCollector Dashboard | Phase 5 | 🟡 中 |
| 批量反编译模式 | Phase 5 | 🟢 低 |
