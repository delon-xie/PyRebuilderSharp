# Phase 9-2-04 总结: Comprehension 变量泄漏 + cleanup

> 白盒: 328→338 (+10), BARE_EXPR: 68→58 (-10)

## 变更

| 规则 | 影响 |
|:-----|:------|
| `Raise { Exc: null, Cause: null }` | 裸 raise 清理（for-else StopIteration 残留） |
| `Call(Name("range"/"iter"))` before `For` | GET_ITER 泄漏清理 |
| `Constant(string)` 短字符串 | `inheritance.` 等 f-string 片段 |

## 下一步

剩余 BARE_EXPR 58 例，主要是 abc 控制流分裂（~25）、enum 大文件（~15）、reprlib try→class（~10）。

继续 **9-2-03**（Handler preamble + TNH 修复）？
