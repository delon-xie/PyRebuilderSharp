# 三大核心问题根因分析与解决方案（更新：2026-07-07）

---

## ✅ 问题 1：try/except 在 3.8-3.14 塌陷（部分修复）

### 当前状态

| 版本 | 路径 | 状态 |
|:----:|:-----|:-----|
| 3.5-3.7 | `BuildTryFromBlock` | ✅ 部分 |
| **3.8-3.10** | `BuildTryFromBlock` + `JUMP_IF_NOT_EXC_MATCH` | ✅ **已修复** |
| 3.11-3.14 | `BuildTryFromExceptionTable` | ❌ 待修复 |

---

## ✅ 问题 2：推导式元素/过滤/迭代器丢失（部分修复）

### 当前状态

| 路径 | 版本 | 状态 |
|:-----|:----:|:-----|
| 生成器表达式 | 3.10+ | ✅ `(x * x for x in range(10))` |
| 列表推导式 | 3.10+ | ✅ `[x * x for x in range(10) if x % 2 == 0]` |
| 字典推导式 | 3.10+ | ✅ `{k: v for (k, v) in items}` |
| 集合推导式 | 3.10+ | ✅ `{x for x in range(5)}` |
| 嵌套推导式 | 3.10+ | ❌ 完全崩坏 |
| lambda in comp | 3.10+ | ❌ 深层分析中 |

**Level 6 diff**: 1196 → **1114** (↓82), B-class = 8

### 剩余难点

| 问题 | 根因 | 估算 |
|:-----|:-----|:----:|
| 嵌套推导式 l6_5 | `<listcomp>` 内层通过 `BuildLambda` 回退，cell 变量和 iterable 丢失 | 3h+ |
| lambda in comp l6_15 | `BuildLambda` 子代码体为空，args/body/iterable 全部丢失 | 2h+ |

---

## ❌ 问题 3：`__build_class__` 模式匹配失败

未开始。

---

## 修复顺序（更新）

| 顺序 | 子任务 | 估算 | 状态 |
|:----:|:-------|:----:|:----:|
| 1 | try/except 3.8-3.10 handler 识别 | 2h | ✅ |
| 2 | 生成器表达式 `Yield` elt 提取 | 0.5h | ✅ |
| 3 | 列表推导式 LIST_APPEND + elt 模拟 | 3h | ✅ |
| 4 | 字典/集合推导式 MAP_ADD + iterable | 2h | ✅ |
| 5 | 过滤条件提取 | 1h | ✅ |
| 6 | def→class 误判 | 1h | ✅ |
| 7 | lambda in comprehension | 3h | ❌ |
| 8 | 嵌套推导式 | 3h | ❌ |
| 9 | try/except 3.11-3.14 ET | 2h | ❌ |

## 成果

- **l6_1/2/3/4**: 全部推导式类型通过 ✅
- **Level 6 diff**: 1196 → 1114 ↓82
- **Level 2**: try/except 3.8-3.10 结构正确
- **def→class**: l2_9 with 语句函数正确识别
