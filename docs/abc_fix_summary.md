# abc.py 修复总结

> 白盒: 339 (保留), TRY_NO_HANDLER: 7→4 (-3)
> 核心修复: 模块级 try 抑制 + IsTryHeader Step A 保护

---

## 变更

| 文件 | 改动 | 说明 |
|:-----|:------|:------|
| `SequentialBlockBuilder.cs` | `AnnotateExceptionTableBlocks` Step A | 保护偏移 0 的 IsTryHeader 不被清理 |
| `AstBuilder.cs` | `ParseTryStructure` | 检测模块级 try 并跳过（handler 偏移 >100 或覆盖 85%+ 代码） |

## 指标变化

| 指标 | 修复前 | 修复后 | 变化 |
|:-----|:------:|:------:|:----:|
| 白盒通过 | 339 | 339 | → |
| TRY_NO_HANDLER | 7 | **4** | ✅ **-3** |
| BARE_EXPR | 58 | 58 | → |

## abc.py 各版本输出对比

| 版本 | 修复前 | 修复后 |
|:----:|:-------|:-------|
| 3.8 | `try:\n    __doc__ = ...\n    def ...` | `__doc__ = ...\n    def ...` ✅ |
| 3.9 | 同上 | 同上 ✅ |
| 3.10 | 同上 | 同上 ✅ |

## 当前 abc.py 剩余问题

| 版本 | BARE_EXPR | TRY_NO | 问题 |
|:----:|:---------:|:------:|:------|
| 2.7 | 3 | 0 | 控制流分裂 |
| 3.5 | 4 | 0 | `def ABC()` + 片段 |
| 3.6 | 3 | 0 | 片段 |
| 3.7 | 3 | 0 | 片段 |
| 3.8 | 1 | 0 | `inheritance.` |
| 3.9 | 1 | 0 | `inheritance.` |
| 3.10 | 1 | 0 | `inheritance.` |
| 3.11+ | 1-2 | 0 | `inheritance.` + `update_abstractmethods` |
