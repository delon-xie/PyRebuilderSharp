# Phase 9-04 总结文档: EMPTY_TRY + TRY_NO_HANDLER

> 日期: 2026-07-10
> 修复: `ParseTryStructure` 跳过 handler preamble 块

---

## 变更文件

| 文件 | 改动 |
|------|------|
| `src/.../Builders/AstBuilder.cs` | +60 行: `IsHandlerPreambleBlock`, `IsHandlerEndBlock`, `ParseTryStructure` preamble 跳过 |
| `src/.../Builders/SequentialBlockBuilder.cs` | Step A 回退（Depth 方案待优化） |

## 白盒指标

| 指标 | 9-03a | 9-04 | 变化 |
|:-----|:-----:|:----:|:----:|
| 白盒通过 | 310 | **328** | **+18** ✅ |
| **EMPTY_TRY** | **51** | **13** | **-38** ✅ |
| BARE_EXPR | 67 | 68 | +1 |
| SYNTAX_ERROR | 10 | 10 | → |
| TRY_NO_HANDLER | 10 | 10 | → |

## 全量基线

| 指标 | 9-03a | 9-04 | 变化 |
|:-----|:----:|:----:|:----:|
| 1325/1325 | ✅ | ✅ | → |
| A+B | 52 (4%) | 52 (4%) | → |
| Diff lines | 139836 | 141759 | ⚠️ +1923 |
| 孤儿块 | 0 | 0 | → |

## EMPTY_TRY 剩余 49 例分析

| 文件 | 例数 | 版本 | 特征 |
|:-----|:----:|:-----|:-----|
| test_try_simple | 11 | 2.7~3.14 | 所有版本均有，源码有 `try: raise` 但编译器优化 |
| enum | 19 | 3.6~3.14 | 大文件嵌套 try，handler 内部 ET 深度复杂 |
| functools | 1 | 3.9 | 同 |
| test_try_complex | 10 | 2.7~3.14 | 嵌套 try 解析不完整 |
| reprlib | 6 | 3.8~3.14 | 异常表边界问题 |
| l2_exception | 2 | 3.12/3.14 | 暴露 |

**根因总结**：EMPTY_TRY 的核心问题是 `AnnotateExceptionTableBlocks` 的 Step A 过度清除。旧的 fully-contained 方案清除过多（误伤有效 try header），Depth 方案太保守（不足）。需要一个结合 Depth 对比 + offset 范围检查的中间方案。

## 后续建议

| 问题 | 当前 | 建议 | 难度 |
|:-----|:----:|:-----|:----:|
| EMPTY_TRY | 49 | 优化 Step A Depth + offset 混合方案 | 中 |
| BARE_EXPR | 68 | 继续加深清理规则 | 低 |
| TRY_NO_HANDLER | 10 | handler preamble 边界检测 | 中 |
| SYNTAX_ERROR | 10 | enum 大文件截断修复 | 高 |
