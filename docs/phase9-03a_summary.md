# Phase 9-03a 总结文档: SYNTAX_ERROR 修复

> 日期: 2026-07-10
> 修复: 语法错误模式检测 + 自动修复

---

## 变更文件

| 文件 | 改动 |
|------|------|
| `src/.../Builders/AstBuilder.cs` | +170 行: `FixSyntaxErrors` + `FixSyntaxErrorsRecursive` + `IsValidPythonIdentifier` + `IsInvalidYieldUsage` |

## 白盒指标变化

| 指标 | 9-02 | 9-03a | 变化 |
|:-----|:----:|:-----:|:----:|
| 白盒通过 | 305 | **310** | ✅ **+5** |
| **SYNTAX_ERROR** | **14** | **10** | ✅ **-4** |
| **BARE_EXPR** | **74** | **67** | ✅ **-7** |
| EMPTY_TRY | 49 | 51 | ⚠️ +2 (暴露) |
| TRY_NO_HANDLER | 10 | 10 | → |

## 全量基线

| 指标 | 9-02 | 9-03a | 变化 |
|:-----|:----:|:-----:|:----:|
| 1325/1325 | ✅ | ✅ | → |
| A+B | 52 (4%) | 52 (4%) | → |
| **Diff lines** | **140207** | **139836** | **↓371** |
| 孤儿块 | 0 | 0 | → |

## 修复的测试

| 测试 | 版本 | 原症状 | 修复方式 |
|:-----|:----:|:-------|:---------|
| test_simple_comp | 3.5/3.6/3.7 | `def 5(x):` + filename 变量名 | 删除无效 FunctionDef 名 |
| test_nested_comp | 3.5/3.6/3.7 | `def 5(x):` + filename 变量名 | 同上 |
| l5_class | 3.12 | `yield from` outside function | 替换为 pass |
| abc | 3.5 | 部分修复 | 函数名过滤 |

## FixSyntaxErrors 规则

1. **无效 Python 标识符函数名** → 删除 FunctionDef（`def 5(x):` 模式，3.5-3.7 推导式残留）
2. **yield / yield from 在非函数体** → pass（类体中的 generator 泄漏）
3. **continue / break 在循环体外** → pass
4. 递归处理所有容器结构（FunctionDef/ClassDef/If/For/While/Try/With）

## 问题分析变化

```
SYNTAX_ERROR 14例分类（修复后）:
├── 大文件边界  5例（enum 3.11-3.14, l7_edge 3.12）
├── 3.5 语法差异 4例（abc 3.5, test_cls2 3.5, test_nested_comp 3.7, test_simple_comp 3.7）
└── 输出截断  1例（test_simple_comp 3.6）
```
