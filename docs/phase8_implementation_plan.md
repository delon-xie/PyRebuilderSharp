# Phase 8 实施方案（5 步落地）

> 基于 `docs/improvement_plan_phase8_v2.md` 的优先级排序
> 原则：低成本高回报优先 → 研读指导架构改动 → 高收益高成本最后
> 每步产出必须可验证（dotnet build + 白盒回归 + 全量基线）

---

## 路线图总览

```
Step 1 (0.5天)    Step 2 (2天)     Step 3 (2天)       Step 4 (3天)       Step 5 (3天)
┌──────────┐     ┌──────────┐     ┌──────────┐      ┌──────────┐       ┌──────────┐
│ Compile  │ ──→ │ 研读3次  │ ──→ │ BARE_EXPR│ ──→  │ 后支配树 │ ──→  │ COME_FROM│
│ 验证     │     │         │     │ 清理     │      │ + 验证器 │      │ 增强     │
│ BARE分类 │     │ pycdc   │     │ 表达式   │      │          │      │ CodeObj  │
│          │     │         │     │ 折叠     │      │          │      │ ET映射   │
└──────────┘     └──────────┘     └──────────┘      └──────────┘       └──────────┘
      ↓               ↓               ↓                  ↓                 ↓
  dotnet build   研读记录 ×3    dotnet build       dotnet build        whitebox回归
  + whitebox     (不跑测试)      + whitebox         + whitebox          全量基线
```

---

## Step 1: 快速反馈环（0.5 天）🥇

**目标**：建立 compile 语法验证 + 完成 BARE_EXPR 根因分类审计，为后续步骤提供数据基础。

### 1.1 CompileVerifier.cs

```csharp
// 新文件: tests/PyRebuilderSharp.Tests/CompileVerifier.cs
// 子进程调用 python3 -c "ast.parse(sys.stdin.read())"
public static class CompileVerifier
{
    /// <summary>
    /// 方式 A (必做): ast.parse — 轻量语法检查
    /// 方式 B (可选): version-specific compile — 版本匹配编译
    /// </summary>
    public static CompileResult VerifySyntax(string source, PythonVersion version)
    {
        // 1. 写入临时文件
        // 2. 子进程 python3 -c "
        //    import sys, ast
        //    code = open(sys.argv[1]).read()
        //    try:
        //        ast.parse(code)
        //        print('PASS')
        //    except SyntaxError as e:
        //        print(f'FAIL:{e.lineno}:{e.msg}')
        //    " temp.py
        // 3. 解析输出
    }
}
```

**集成目标**：在 `PycdcSuiteRunner.RunTestCase` 的 token 比较后追加。默认关闭，通过 `--verify-compile` 开启。

### 1.2 BARE_EXPR 分类审计

**不动代码，只分析**。从 83 例白盒失败点中提取分类：

```bash
# 运行 whitebox 测试，输出所有 BARE_EXPR 的上下文
dotnet test --filter "BARE_EXPR" --logger "console;verbosity=detailed" 
  > /tmp/bare_expr_audit.txt
```

逐例标注归属类别（填入下表）：

| ID | 源文件 | 表达式内容 | 分类 | 清理规则 |
|----|--------|-----------|------|---------|
| 1 | genexpr.3.12 | `list.append(x)` | comprehension | B1 |
| 2 | class_body.3.10 | `'__qualname__'` | class attr init | B5 |
| ... | ... | ... | ... | ... |

**产出物**：`docs/bare_expr_audit_20260710.md` — 完整 83 例分类表，作为 Step 3 的直接输入。

### 1.3 验收条件

```
✅ dotnet build 通过
✅ 白盒测试通过率 ≥ 73%（不变）
✅ CompileVerifier 输出 SYNTAX_WARN 不设严格阈值（仅报告）
✅ bare_expr_audit.md 完成 83 例全部归类
```

---

## Step 2: 架构研读（2 天）🥇

**目标**：从外部项目中提取可直接落地的算法，指导 Step 4-5 的代码实现。

### 2.1 研读顺序

| 次序 | 目标 | 来源 | 预计耗时 | 服务对象 |
|------|------|------|---------|---------|
| ① | COME_FROM 构建算法 + 跳转分类规则 | `uncompyle6/scanner.py` | 2h | Step 4 后支配树 + COME_FROM |
| ② | 嵌套 CodeObject 递归反编译 | `pycdc/src/ASTree.cpp` BuildFromCode | 2h | Step 5 CodeObject 递归 |
| ③ | ExceptionTable → CFG 异常边 | `pycdc/src/ASTree.cpp` try/finally 处理 + `uncompyle6/semantics/` try | 2h | Step 5 ET 映射 |
| ④ | LIST_APPEND / MAP_ADD → 推导式 | `uncompyle6/scanner.py` | 1h | Step 3 BARE_EXPR |
| ⑤ | MAKE_FUNCTION + CALL_FUNCTION → decorator | `pycdc/src/ASTree.cpp` | 1h | Step 3 表达式折叠 |

### 2.2 每次研读的产出格式

```markdown
# 研读记录: [主题]

## 来源文件
- `uncompyle6/scanner.py:180-250` `build_come_from()`

## 关键算法
### 跳转分类规则（原文）
```python
# uncompyle6 源码片段 + 行号
```

### 在 PyRebuilderSharp 中的应用
```csharp
// 对应的 C# 实现思路
```
```

产出物存放在 `docs/research/` 目录下。

### 2.3 验收条件

```
✅ 5 份研读记录文档（docs/research/）
✅ 每份包含可执行的 C# 伪代码/设计思路
❌ 此步骤不修改任何 .cs 文件
```

---

## Step 3: BARE_EXPR 清理 + 表达式折叠（2 天）🥈

**目标**：基于 Step 1 的分类审计 + Step 2④⑤ 研读，实现 BARE_EXPR 从 83→~25。

### 3.1 实现 CleanupBareExpr pass

```csharp
// 在 AstBuilder.cs Build() 末尾追加：
// Step 3: 新增的后处理 pass
stmts = CleanupBareExpr(stmts);

private List<Stmt> CleanupBareExpr(List<Stmt> stmts)
{
    // 按 Step 1 分类审计的结果，逐类实现 B1-B9 规则
    // 只清理 "安全" 类别（可由研读 Step 2④ 证明可逆）
}
```

执行顺序（按安全度从高到低）：

| 优先级 | 规则 | 安全度 | 预期减量 |
|--------|------|--------|---------|
| 1 | B4/B6: FunctionRef(`<...>`) 删除 | 🟢 极高 | -15 |
| 2 | B8: 孤立 Name 删除 | 🟢 高 | -8 |
| 3 | B1/B2/B3: comprehension append/add 删除 | 🟡 中（需 IsInComprehensionContext） | -25 |
| 4 | B5: class `'__qualname__'` 删除 | 🟢 高 | -5 |
| 5 | B7: match guard 中间值 | 🟡 中 | -5 |
| 6 | B9: `.__ iter__()` 调用残留 | 🟡 中 | -5 |

### 3.2 实现 FoldDecoratorCalls pass

**基于 Step 2⑤ pycdc ASTree.cpp 研读**：

```csharp
// 在 CleanupBareExpr 之后：
stmts = FoldDecoratorCalls(stmts);

private List<Stmt> FoldDecoratorCalls(List<Stmt> stmts)
{
    // 从后向前扫描 ExprStmt(Call(func, args)) 的模式
    // 如果 args 包含 FunctionDef，将 func 移到 FunctionDef.Decorators
    // 删除 source ExprStmt
}
```

### 3.3 风险控制

- 每次加一条规则 → `dotnet build` → `whitebox test` 看影响
- 退化超过 2 个测试点 → 回退该规则
- 只删可明确判定为伪影的表达式

### 3.4 验收条件

```
✅ BARE_EXPR: 83 → ≤30
✅ FORMAT_ERROR: 3 → 0
✅ 白盒通过率: 73% → ≥76%
✅ 全量基线 1325/1325 不变
✅ dotnet build 无警告
```

---

## Step 4: 后支配树 + COME_FROM 结构验证（3 天）🥈

**目标**：新增后支配树分析 + COME_FROM 标注 + StructuralValidator，提升嵌套 try/if-elif 结构精度。

### 4.1 实现 PostDominatorScanner

**基于 Step 2① uncompyle6 COME_FROM 研读**。

```csharp
// 新文件: Scanners/PostDominatorScanner.cs
public class PostDominatorScanner
{
    // 1. ComputePostDominators(cfg) — 反转 CFG 边，复用现有支配树算法
    // 2. BuildComeFromMap(cfg) — 按 uncompyle6 分类规则
    //    生成 targetOffset → [sourceOffsets] 映射
    // 3. ShouldGenerateComeFrom(op) — 跳转分类决策
}
```

### 4.2 实现 StructuralValidator

```csharp
// 新文件: Scanners/StructuralValidator.cs
public class StructuralValidator
{
    // R1: if-elif 链验证（后支配）
    // R2: try-except handler 归属验证
    // R3: loop-body vs break 验证
    // R4: else-body 归属验证
    // R5: ET 异常边验证
}
```

### 4.3 集成到 Build() 流程

```csharp
// AstBuilder.cs Build() 中，在 ParseControlStructures 之后：
var validationResult = validator.Validate(stcf, postIdoms, comeFrom);
if (validationResult.HasFailures)
{
    // 输出诊断日志（不修改 AST，仅标记）
    foreach (var failure in validationResult.Failures)
        Console.Error.WriteLine($"[STRUCT_VALIDATE] FAIL {failure.Rule}: {failure.Description}");
}
```

> **关键设计决策**：Step 4 只报告不修——验证器先运行积累数据，
> 统计哪些 R1-R5 规则高频触发，再在 Step 5 中实现自动修复。

### 4.4 验收条件

```
✅ 新增后支配树计算，在测试用例中正确识别循环头后支配关系
✅ COME_FROM 映射覆盖至少 90% 条件跳转
✅ StructuralValidator 输出诊断日志
✅ 白盒通过率 ≥ 73%（不变——只报告不修）
✅ dotnet build 无警告
```

---

## Step 5: COME_FROM 增强 + CodeObject 递归 + ET 映射（3 天）🥉

**目标**：基于 Step 4 的诊断数据 + Step 2②③ 的研读，实现自动修复 + 嵌套递归 + ET 严格映射。

### 5.1 COME_FROM 自动修复

**基于 Step 4 诊断数据**。对高频触发的 R1-R5 规则实现自动修复：

| 规则 | 高频阈值 | 修复策略 |
|------|---------|---------|
| R1 (if-elif) | >5 次 | 合并 IsConditionHeader 链为 IsElifChain |
| R2 (try handler) | >10 次 | 调整 handler 的 visited 范围 |
| R3 (loop/break) | >3 次 | 从 LoopBody 中移除 break 块 |
| R4 (else) | >5 次 | 从 else block 中分离独立块 |
| R5 (ET) | >5 次 | 调整 ExceptionTable body 边界到第一个 handler 入口 |

```csharp
// StructuralValidator 新增:
public class StructuralFixer
{
    public void ApplyFixes(StructuredCFG stcf, ValidationResult result)
    {
        // 对高频 FAIL 应用修复
    }
}
```

### 5.2 嵌套 CodeObject 递归

**基于 Step 2② pycdc ASTree.cpp 研读**。

```csharp
// 新方法: AstBuilder.DecompileNestedCodeObjects()
// 在 PostProcessFunctionDefs 之后调用
private List<Stmt> DecompileNestedCodeObjects(List<Stmt> stmts, CodeObject parentCode)
{
    // 1. 遍历 stmts 中的 FunctionDef
    // 2. 在 parentCode.ChildCodes 中查找匹配的 CodeObject
    // 3. 对 FunctionDef.Body 仅含 CommentBlock/pass 的，重新调用 Build()
    // 4. 递归深度 ≤ 10
    // 5. 使用 _processedCodeObjects HashSet 去重
}
```

### 5.3 ExceptionTable → CFG 异常边严格映射

**基于 Step 2③ 研读**。

```csharp
// 修改 SequentialBlockBuilder.AnnotateExceptionTableBlocks():
// 原：为每个 Depth==0 的 ET 条目设置 IsTryHeader=true
// 改：排除 handler block 内的嵌套 ET 条目
//    + body 范围精确到第一个 handler 入口
//    + 与后支配树 R5 交叉验证
```

### 5.4 验收条件

```
✅ COME_FROM 自动修复改善白盒测试至少 5 个点
✅ 嵌套 CodeObject 递归后闭包/嵌套 lambda 测试通过
✅ ET 严格映射后 EMPTY_TRY 减少至少 10 例
✅ 白盒通过率: ≥82%
✅ 全量基线 1325/1325 不变
✅ dotnet build 无警告
```

---

## 回退策略

每步结束后必须执行回归。如果某步导致退化：

```
退化类型                   处理方式
─────────────────────────────────────────────
dotnet build 失败          立即修复，不推进
全量基线 < 1325/1325       回退该步的所有代码变更
白盒通过率下降 < 2%         保留代码，标记为已知退化，下步修复
白盒通过率下降 ≥ 2%         回退该步，重新评估设计
```

---

## 时间线估算

| Step | 内容 | 预估工时 | 依赖 |
|------|------|---------|------|
| 1 | Compile 验证 + BARE 分类审计 | 0.5 天 | 无 |
| 2 | 5 次研读 | 2 天 | 无 |
| 3 | BARE_EXPR 清理 + 表达式折叠 | 2 天 | Step 1 分类表 + Step2④⑤ |
| 4 | 后支配树 + COME_FROM | 3 天 | Step2① 研读 |
| 5 | COME_FROM修复 + CodeObj + ET | 3 天 | Step 4 诊断 + Step2②③ |
| **合计** | | **10.5 天** | |

**预期白盒通过率收敛路径**：

```
Step 0 (当前):    73%
Step 1:          73% (仅验证，不修复)
Step 3:          ~78% (BARE_EXPR 83→25)
Step 4:          ~78% (只报告，不修)
Step 5:          ~85%+ (COME_FROM修复 + CodeObj + ET)
```

---

> **文档版本**: v1.0
> **日期**: 2026-07-10
> **下一步**: 确认 Step 1 开始
