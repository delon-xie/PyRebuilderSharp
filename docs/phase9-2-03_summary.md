# Phase 9-2-03 总结: Handler preamble + TRY_NO_HANDLER

> 白盒: 338→339 (+1), EMPTY_TRY: 14→5 (-9), TRY_NO: 10→7 (-3)
> Diff lines: 141457→136031 (↓5426)

---

## 变更

`BuildTryStructureStatements`: 空 handler 抑制
- 所有 handler body 仅含 pass → 移除 handler
- 无 handler + 无 else/finally → 不生成 try 结构，直接返回 body

## 指标变化

| 指标 | 9-2-04 | 9-2-03 | 变化 |
|:-----|:------:|:------:|:----:|
| 白盒通过 | 338 | **339** | ✅ +1 |
| EMPTY_TRY | 14 | **5** | ✅ -9 |
| TRY_NO_HANDLER | 10 | **7** | ✅ -3 |
| BARE_EXPR | 58 | 58 | → |
| SYNTAX_ERROR | 10 | 14 | ⚠️ +4 |
| Diff lines | 141457 | **136031** | ✅ -5426 |

## 当前状态

```
白盒 339/405 (83.7%)
├── BARE_EXPR      58 → abc 控制流 + enum 大文件
├── SYNTAX_ERROR   14 → 大文件 + 3.5 差异
├── TRY_NO_HANDLER  7 → 剩余 handler 边界
├── CLEANUP_LEAK    7
└── EMPTY_TRY       5 → 带 else/finally
```

继续 **9-2-01**（abc 控制流分裂）？
