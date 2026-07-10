# Phase 9-01 修复计划 (基于基线报告)

> 基线: `docs/baseline_evaluate_report_20260710_085636.md`
> 命令: `python3 tools/baseline_evaluate_all.py` (--seq-blocks 模式)
> 日期: 2026-07-10
> 注: 从本阶段起，修复迭代编号为 Phase9-01、Phase9-02……每轮专注 2~3 个优先级最高的问题，
>     确保每轮完成后基线和白盒退化可追踪。

---

## 基线现状

```
1325/1325 (100%) 反编译成功 ✅
0 孤儿块 ✅
0 运行时崩溃 ✅
A+B 可接受输出: 52/1325 (4%)
白盒通过: 299/405 (74%)
```

## 修复优先级

按"影响面 > 控制块 > 指令缺失 > 孤儿块 > 语法错误"排序：

| 优先级 | 问题 | 影响 | 根因 |
|--------|------|------|------|
| **P0** | CFG handler→class edge 误分类 | **~50 文件** | BlockScanner 中 handler 后继块包含 class/func 定义 |
| **P0** | 3.13 abc.py 模块级折叠 | abc.py (关键库) | 3.13 ET+block scanning 交互异常 |
| **P0** | 3.14 abc.py `for scls in iterable` | abc.py (关键库) | ExtractIterExpression 未适配 3.14 字节码 |
| **P1** | BARE_EXPR 残留 | **82 例** | Step 3 CleanupBareExpr 保守，未覆盖所有模式 |
| **P1** | SYNTAX_ERROR (14 例) | 白盒 14 例 | 3.5-3.7 版本差异、大文件边界 |
| **P2** | EMPTY_TRY (56 例) | 白盒 56 例 | try body 范围 + handler 前导码检测 |
| **P2** | TRY_NO_HANDLER (19 例) | 白盒 19 例 | handler preamble 检测不完整 |
| **P3** | `# orphan @` / `# [SUMMARY]` 噪声 | 所有文件 | 默认开启调试信息 |
| **P3** | REDUNDANT_PASS/RAISE/RETURN (68 例) | 白盒 68 例 | 后处理过滤不完全 |
| **P4** | Docstring 格式 `'text'` vs `"""text"""` | 多数文件 | 代码生成器 docstring 检测 |
| **P4** | 空行丢失 | 多数文件 | 未跟踪 lnotab 行间隙 |
| **P4** | 默认参数值丢失 | 部分函数 | 栈模拟中未保存 |

---

## 迭代路线图

| 迭代 | 内容 | 影响面 | 工期 | 验收指标 | 依赖 |
|:----:|:-----|:------:|:----:|:---------|:----:|
| **9-01** | CFG handler→class edge 修复 | ~50 文件 | 4h | abc.py 改善+D降C | 无 |
| **9-02** | BARE_EXPR + SYNTAX_ERROR 修复 | 96 白盒例 | 2天 | BARE 82→40, SYNTAX 14→5 | step1 审计表 |
| **9-03** | EMPTY_TRY + TRY_NO_HANDLER 修复 | 75 白盒例 | 3天 | EMPTY 56→30, TNH 19→10 | docs/batch_a_fix_plan |
| **9-04** | 冗余消除 + 噪声屏蔽 | 全量 | 1天 | 无 orphan 行, REDUN 68→20 | 无 |
| **9-05** | 可读性改善 | 全量 | 2天 | A+B 52→200+ | 无 |

## Phase9-01 迭代: CFG handler→class edge 修复（~4h）

**影响面**：~50 文件（最大单类影响）
**问题级别**：控制块异常 + 影响面大

**修复方案**：
```
BlockScanner.Scan() 中 →
  在构建 CFG 边时，检查 successor 是否为 class/func 定义（LOAD_BUILD_CLASS / MAKE_FUNCTION）
  如果是，从 handler 的 successors 中移除
  将这些定义连接到上一级（模块级或外部函数）的 CFG 中
```

**验收**：50 个文件改善，abc.py 3.13/3.14 的 D 类降级

## Phase9-02 迭代: BARE_EXPR + SYNTAX_ERROR 批量修复（~2天）

**影响面**：白盒 82+14=96 例
**问题级别**：指令缺失 + 语法错误

**根因**：Step 3 的 CleanupBareExpr 只清理了已知的 9 类模式，仍有 82 例残留。SYNTAX_ERROR 14 例中大部分是 3.5-3.7 的版本兼容问题。

**修复方案**：
```
1. 分析剩余 82 例 BARE_EXPR 的根因（基于 step1_bare_expr_audit.md）
2. 增强 CleanupBareExpr 规则：
   - 孤立 .extend() / .add() 在 comprehension 外
   - yield 在 3.11+ 的 loop 外残留
   - 3.5-3.7 的 for-iter 变量在 for-else 体外的泄漏
3. 对 14 例 SYNTAX_ERROR 逐例分析：
   - 3.5/3.6 的 * unpack 语法差异
   - 大文件（enum/functools）的边界问题
```

**验收**：BARE_EXPR 82→40, SYNTAX_ERROR 14→5

## Phase9-03 迭代: EMPTY_TRY + TRY_NO_HANDLER 修复（~3天）

**影响面**：白盒 56+19=75 例
**问题级别**：控制块异常

**根因**：Batch A 计划已分析的三个独立根因（过度链接、preamble 检测缺失、body 范围边界）。

**修复方案**：
```
1. 过度链接：按 ET Depth 层级严格限制 — handler 内部嵌套 ET 不产生 IsTryHeader
2. Preamble 检测：对 3.10- 添加 POP_TOP×3 preamble 识别
3. Body 范围：try body 精确到第一个 handler 入口
```

**验收**：EMPTY_TRY 56→30, TRY_NO_HANDLER 19→10

## Phase9-04 迭代: 冗余消除 + 噪声屏蔽（~1天）

**影响面**：全量输出文件
**问题级别**：可读性

**根因**：
- `# orphan @` / `# [SUMMARY]` 调试信息默认开启
- `REDUNDANT_PASS/RAISE/RETURN` 后处理过滤不完全

**修复方案**：
```
1. ShowOrphanBlocks 默认改为 false（或 --no-orphan-summary CLI 选项）
2. 增强 CollapseRedundantPasses:
   - 连续 pass 合并为一个
   - try-except-finally 中的多余 pass 删除
   - 空 except: pass → except: ...
3. return None 在模块级和函数结尾的检测
```

**验收**：所有输出文件不再有 `# orphan @` 行，REDUNDANT 68→20

## Phase9-05 迭代: 可读性改善（~2天）

**影响面**：大部分输出文件
**问题级别**：可用性

**根因**：
- Docstring 格式 `'text'` vs `"""text"""`
- 空行未跟踪 lnotab 间隙
- 默认参数值丢失

**修复方案**：
```
1. PythonCodeGenerator 中添加 docstring 检测和格式转换
2. 通过 lnotab/linetable 的行号间隙恢复空行
3. StackMachine 的 MAKE_FUNCTION 中保存默认参数值
```

**验收**：A+B 从 52/1325 提升到 ≥200/1325（+15pp）

---

## 预期收益

```
当前:  A+B=52 (4%), BARE=82, EMPTY_TRY=56, SYNTAX=14, orphan=0
                       
9-01: A+B=52+20=72    (~50 文件改善, abc.py 降级)   ← 控制块修复
9-02: BARE=40~50, SYNTAX=5~8                         ← 指令缺失+语法修复
9-03: EMPTY=25~30, TRY_NO=8~10                       ← 控制块修复
9-04: REDUNDANT=15~20, 无 orphan 噪声                ← 可读性
9-05: A+B=200+                                        ← 大量文件提升至 A/B 类

最终:  A+B≥200 (15%+), BARE≤40, SYNTAX≤5, EMPTY≤30
```

## 风险登记

| # | 风险 | 影响 | 缓解 |
|---|------|------|------|
| 1 | CFG handler→class edge 修复可能引入新退化 | 中 | 逐步修，每步回归测试 |
| 2 | BARE_EXPR 清理误删语义表达式 | 高 | 只删可明确判定为伪影的表达式 |
| 3 | SyntaxError 修复需要逐例分析 | 中 | 从简单例开始（引号/缩进） |
| 4 | 空行恢复依赖 lnotab 精度 | 低 | 可选，可关闭 |
