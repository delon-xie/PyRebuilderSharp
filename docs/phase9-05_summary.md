# Phase 9-05 总结文档: BARE_EXPR 继续清理

> 日期: 2026-07-10

---

## 变更文件

| 文件 | 改动 |
|------|------|
| `src/.../Builders/AstBuilder.cs` | 新增 3 条规则：短字符串常量、Name 含`.`、AstAttribute 链(cls) |

## 白盒指标

| 指标 | 9-04 | 9-05 | 变化 |
|:-----|:----:|:----:|:----:|
| 白盒通过 | 328 | **328** | → |
| BARE_EXPR | 68 | **68** | → |
| EMPTY_TRY | 14 | 14 | → |
| SYNTAX_ERROR | 10 | 10 | → |

## 分析

BARE_EXPR 68 例中，大部分（~50+）是**控制流结构问题**导致的：

```python
# 示例: abc.py 3.10 update_abstractmethods
def update_abstractmethods(cls):
    if hasattr(cls, '__abstractmethods__'):
        return cls
        getattr(scls, '__abstractmethods__', [])  # ← BARE_EXPR (结构问题)
```

- 38 例来自 abc.py（2.7~3.14 各版本）— 控制流分裂产生的裸表达式
- 12 例来自 enum/functools（大文件边界）
- 10 例来自 comprehension 变量泄漏（test_comp, test_nested_comp）
- 8 例来自其他小文件

表达式级清理规则（`Constant string`, `Name with .`, `AstAttribute chain`）无法解决这些问题——需要结构级修复。

## 整体 Phase 9 总结

```
Phase      | 白盒   | BARE | EMPTY | SYNTAX | TNH   
───────────|────────|──────|───────|────────|──────
基线       |  299   |  82  |  56   |  14    |  19
9-01 CFG   |  299   |  82  |  49   |  14    |  10
9-02 BARE  |  305   |  74  |  49   |  14    |  10
9-03a SYN  |  310   |  67  |  51   |  10    |  10
9-04 TRY   |  328   |  68  |  13   |  10    |  10
9-05 BARE2 |  328   |  68  |  14   |  10    |  10
─────────────────────────────────────────────
净改善     |  +29   | -14  | -42   |  -4    |  -9
```
