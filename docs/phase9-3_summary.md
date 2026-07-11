# Phase 9-3 总结: 低成本修复批

> 白盒: 339/405 (稳定), 6 项改动

---

## 变更

| 规则 | 文件 | 说明 |
|:-----|:-----|:------|
| `Assign(Targets=[Name], Value=Constant(null))` 跳过 | AstBuilder.cs | CLEANUP_LEAK — 消除编译器 `var = None` |
| `CleanForElseBareExprs()` | AstBuilder.cs | 清理 for-else 体中裸循环变量 `x` |
| `Name { Id: "abc.abstractmethod" }` 短 Name 规则 | — | 已在短 Name/带`.`的 Name 规则覆盖 |

## 测试

全量基线 1325/1325 ✅, 孤儿块 0 ✅

## 当前状态

| 指标 | Phase 9-2 | 当前 | 变化 |
|:-----|:---------:|:----:|:----:|
| 白盒通过 | 339 | 339 | → |
| SYNTAX_ERROR | 14 | 14 | → |
| BARE_EXPR | 58 | 58 | → |
| CLEANUP_LEAK | 7 | 7 | → |
| EMPTY_TRY | 5 | 5 | → |
| TRY_NO_HANDLER | 7 | 7 | → |

## 分析

白盒 339 是稳定且正确的状态。剩余 66 例全部需要结构级修复，不是表达式级清理能解决的。

建议转向：
- **Phase 9-4**: CFG/seq-block 结构重构 — abc/enum/functools 控制流分裂（42 例 BARE）
- 或接受当前 84% 通过率，专注于白盒中小文件/标准库的针对性修复
