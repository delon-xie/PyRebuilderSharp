# pycdc 测试集吸收与评估体系 Implementation Plan

> **For AI Agent Implementer:** Required sub-skills: use subagent-driven-development or inline execution with checkpoints. Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将 pycdc 的 token-based 测试体系完整移植到 PyRebuilderSharp，建立可重复的自动化评估基线，每个轮次运行测试集报告 PASS/FAIL。

**Architecture:** 三层架构：
1. `TokenDumper` — C# 移植 pycdc 的 token_dump，将 Python 源码 token 化用于语义比较
2. `PycdcTestSuite` — 测试运行器，加载 compiled/*.pyc → decompile → tokenize → diff
3. `PyRebuilderSharp.Tests` — xUnit 测试项目，驱动一切

**Tech Stack:** xUnit 2.9+, FluentAssertions 7.x, .NET 10

**Constraints:** 每个文件 ≤ 300 行，TokenDumper ≤ 500 行（逻辑复杂）

---

## File Structure

```
PyRebuilderSharp/
├── src/
│   └── PyRebuilderSharp.Core/
│       └── Testing/
│           ├── TokenDumper.cs           # [NEW] pycdc token_dump C# 移植
│           └── TokenDiffResult.cs       # [NEW] diff 结果模型
├── tests/
│   └── PyRebuilderSharp.Tests/          # [NEW] xUnit 测试项目
│       ├── PyRebuilderSharp.Tests.csproj
│       ├── TokenDumperTests.cs           # TokenDumper 单元测试
│       ├── PycReaderTests.cs             # PycReader 单元测试
│       ├── StackMachineTests.cs          # StackMachine 单元测试
│       ├── PycdcSuiteTests.cs            # pycdc 完整测试集 E2E
│       └── TestData/
│           ├── input/                    # [SYMLINK → pycdc/tests/input/]
│           ├── compiled/                 # [SYMLINK → pycdc/tests/compiled/]
│           ├── tokenized/               # [SYMLINK → pycdc/tests/tokenized/]
│           └── xfail/                   # [SYMLINK → pycdc/tests/xfail/]
└── docs/
    └── TESTING_BASELINE.md              # [NEW] 基线报告文档
```

### Token 类型定义（移植自 pycdc/token_dump）

```csharp
public enum TokenType
{
    INDENT, OUTDENT, ENDLINE, WORD, INT, FLOAT, STRING, SYMBOL
}

// 数值 token 做语义比较（int 比值、float 比近似值）
// 字符串 token 做规范化比较（前缀排序、转义标准化）
```

---

## Implementation Tasks

### Task 1: 创建测试项目

**Files:**
- Create: `tests/PyRebuilderSharp.Tests/PyRebuilderSharp.Tests.csproj`
- Create: `tests/PyRebuilderSharp.Tests/TestData/` (symlinks)

- [ ] **Step 1: 创建测试项目目录和 csproj**

```bash
mkdir -p /Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests
```

- [ ] **Step 2: 编写 Tests.csproj**

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.13.0" />
    <PackageReference Include="xunit" Version="2.9.3" />
    <PackageReference Include="xunit.runner.visualstudio" Version="3.1.0" />
    <PackageReference Include="FluentAssertions" Version="7.2.0" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="..\..\src\PyRebuilderSharp.Core\PyRebuilderSharp.Core.csproj" />
  </ItemGroup>
</Project>
```

- [ ] **Step 3: 创建测试数据符号链接**

```bash
TEST_REF=/Users/admin/codes/tools/PyRebuild/ref/pycdc/tests
TEST_DST=/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData
mkdir -p $TEST_DST
ln -sf $TEST_REF/input $TEST_DST/input
ln -sf $TEST_REF/compiled $TEST_DST/compiled
ln -sf $TEST_REF/tokenized $TEST_DST/tokenized
ln -sf $TEST_REF/xfail $TEST_DST/xfail
```

- [ ] **Step 4: 添加测试项目到解决方案**

```bash
cd /Users/admin/codes/Tools/PyRebuilderSharp
dotnet sln add tests/PyRebuilderSharp.Tests/PyRebuilderSharp.Tests.csproj
```

- [ ] **Step 5: 验证构建通过**

```bash
dotnet build tests/PyRebuilderSharp.Tests/
```
Expected: Build succeeded, 0 errors

---

### Task 2: TokenDumper C# 移植

**Files:**
- Create: `src/PyRebuilderSharp.Core/Testing/TokenType.cs`
- Create: `src/PyRebuilderSharp.Core/Testing/PyToken.cs`
- Create: `src/PyRebuilderSharp.Core/Testing/TokenDumper.cs`
- Create: `src/PyRebuilderSharp.Core/Testing/TokenDiffResult.cs`

**pycdc token_dump 的关键行为：**
1. 过滤空行和注释
2. 追踪缩进级别（INDENT/OUTDENT）
3. 忽略括号上下文内的换行
4. 数值标准化：`0xFF` → `255`, `3.0` → `3.0`
5. 字符串前缀排序：`rb""` → `br""`
6. 特殊字符转义标准化

- [ ] **Step 1: 定义 TokenType 和 PyToken 模型**

```csharp
// TokenType.cs
public enum TokenType { INDENT, OUTDENT, ENDLINE, WORD, INT, FLOAT, STRING, SYMBOL }

// PyToken.cs
public abstract record PyToken(TokenType Type, int LineNumber);
public record WordToken(string Word, int LineNumber) : PyToken(TokenType.WORD, LineNumber);
public record IntToken(long Value, int LineNumber) : PyToken(TokenType.INT, LineNumber);
// ...
```

- [ ] **Step 2: 实现 TokenDumper 核心解析器**

核心方法：`List<PyToken> Tokenize(string sourceCode)`

实现要点：
- 逐行扫描，跟踪缩进栈
- 使用正则识别 WORD / INT / FLOAT / STRING / SYMBOL
- 括号上下文内不产生 EOL token
- 字符串跨行处理
- INT 支持 0x/0b/0o 前缀和 `_` 分隔符

- [ ] **Step 3: 实现 TokenDiffResult**

```csharp
public class TokenDiffResult
{
    public bool Match { get; init; }
    public List<string> DiffLines { get; init; } = new();
    public int ExpectedCount { get; init; }
    public int ActualCount { get; init; }
}
```

- [ ] **Step 4: 编写 TokenDumperTests 单元测试**

```csharp
[Theory]
[InlineData("x = 42", new[]{...})]
[InlineData("if True:\n    pass", new[]{...})]
public void Tokenize_BasicExpressions_ReturnsCorrectTokens(string source, TokenType[] expected)
```

- [ ] **Step 5: 运行并验证 TokenDumper 测试通过**

```bash
dotnet test tests/PyRebuilderSharp.Tests/ --filter "TokenDumperTests"
```

---

### Task 3: 编写基础单元测试

**Files:**
- Create: `tests/PyRebuilderSharp.Tests/PycReaderTests.cs` — 读一个已知 .pyc 检查 Magic 和指令数
- Create: `tests/PyRebuilderSharp.Tests/StackMachineTests.cs` — 模拟指令序列验证表达式树

- [ ] **Step 1: PycReaderTests — 读取 simple_const .pyc**

读取 `TestData/compiled/simple_const.3.8.pyc`：
```csharp
[Fact]
public void Read_SimpleConst38_ReturnsCorrectInstructions()
{
    var reader = new PycReader();
    var data = File.ReadAllBytes("TestData/compiled/simple_const.3.8.pyc");
    var code = reader.Read(data);
    code.Name.Should().Be("<module>");
    code.Instructions.Count.Should().BeGreaterThan(0);
}
```

- [ ] **Step 2: StackMachineTests — 测试 LOAD_CONST + STORE_NAME**

```csharp
[Fact]
public void Execute_LoadConstStoreName_ReturnsAssign()
{
    var code = new CodeObject
    {
        Constants = new() { [0] = 42 },
        Names = new() { "a" }
    };
    var sm = new StackMachine(code);
    var r1 = sm.Execute(new Instruction(0, Opcode.LOAD_CONST, 0)); // null
    var r2 = sm.Execute(new Instruction(2, Opcode.STORE_NAME, 0)); // Assign
    r2.Should().BeOfType<Assign>();
    var assign = (Assign)r2!;
    assign.Targets[0].Should().BeOfType<Name>();
    ((Name)assign.Targets[0]).Id.Should().Be("a");
}
```

- [ ] **Step 3: 运行并确认通过**

```bash
dotnet test tests/PyRebuilderSharp.Tests/ --filter "PycReaderTests|StackMachineTests" -v
```

---

### Task 4: pycdc 完整 E2E 测试套件

**Files:**
- Create: `tests/PyRebuilderSharp.Tests/PycdcSuiteTests.cs`

- [ ] **Step 1: 实现测试运行器类**

```csharp
public class PycdcSuiteRunner
{
    private readonly string _compiledDir;
    private readonly string _tokenizedDir;
    private readonly string _xfailDir;

    public record TestResult(string TestName, string PycFile, string PythonVersion, bool Passed, List<string> DiffLines);

    public List<TestResult> RunAll(string filter = "")
    {
        // 1. 扫描 compiled/*.pyc
        // 2. 按 test_name 分组
        // 3. 对每个 pyc：
        //    a. PycReader.Read(data)
        //    b. BlockScanner.Scan
        //    c. AstBuilder.Build
        //    d. PythonCodeGenerator.Generate
        //    e. TokenDumper.Tokenize
        //    f. 与 tokenized/{test_name}.txt 对比
        // 4. 返回所有 TestResult
    }
}
```

- [ ] **Step 2: 实现 [Theory] 数据驱动测试**

```csharp
public class PycdcSuiteTests
{
    public static IEnumerable<object[]> GetTestCases()
    {
        var runner = new PycdcSuiteRunner();
        return runner.GetAvailableTests().Select(t => new object[] { t.TestName, t.PycFile });
    }

    [Theory]
    [MemberData(nameof(GetTestCases))]
    public void DecompileAndCompare(string testName, string pycFile)
    {
        var runner = new PycdcSuiteRunner();
        var result = runner.RunSingle(testName, pycFile);
        Assert.True(result.Passed, string.Join("\n", result.DiffLines.Take(20)));
    }
}
```

- [ ] **Step 3: 运行基线测试并记录结果**

```bash
dotnet test tests/PyRebuilderSharp.Tests/ --filter "PycdcSuiteTests" -v 2>&1 | tee /tmp/baseline_run.txt
```

---

### Task 5: 基线评估报告

**Files:**
- Create: `docs/TESTING_BASELINE.md`

- [ ] **Step 1: 统计 baseline 结果**

从Task 4的输出中提取：
- 总测试数
- PASS 数 / FAIL 数
- 按测试类别分类（simple / control_flow / exceptions / class / etc.）
- 按 Python 版本分类

- [ ] **Step 2: 编写基线报告**

```markdown
# PyRebuilderSharp 测试基线

**日期:** 2026-06-12
**pycdc 测试集:** 83 输入文件 × 5 版本 ≈ 420 .pyc

## 当前基线

| 类别 | 总用例 | PASS | FAIL | 通过率 |
|------|--------|------|------|--------|
| 简单表达式 | ... | ... | ... | ...% |
| 控制流 | ... | ... | ... | ...% |
| 异常处理 | ... | ... | ... | ...% |
| 类/函数 | ... | ... | ... | ...% |
| **总计** | **...** | **...** | **...** | **...%** |
```

- [ ] **Step 3: 输出改进优先级**

基于 FAIL 测试的具体错误，生成操作码缺失清单：
```markdown
## 缺失操作码（按影响面排序）

| 操作码 | 影响测试数 | 优先级 |
|--------|-----------|--------|
| CALL_FUNCTION | 25 | P0 |
| BUILD_TUPLE | 18 | P0 |
| ... | ... | ... |
```

---

### Task 6: 快速修复 — 缩小差距

基于基线报告，优先实现缺失最多的操作码。

- [ ] **Step 1: 按 P0 缺失操作码修复 StackMachine**

每次添加 3-5 个操作码，然后重新运行测试看通过率提升。

```
当前 StackMachine 缺失的操作码（根据 simple_const 测试）:
- BUILD_TUPLE, BUILD_LIST, BUILD_MAP → 添加容器字面量支持
- COMPARE_OP → 添加比较运算（已有部分）
- CALL_FUNCTION → 添加函数调用支持
```

- [ ] **Step 2: 迭代循环**

每轮：修复 → 运行测试集 → 更新基线 → 下一轮

---

## 执行顺序

1. Task 1: 创建测试项目 ✅ (先决条件)
2. Task 2: TokenDumper 移植
3. Task 3: 基础单元测试
4. Task 4: pycdc E2E 测试套件
5. Task 5: 基线评估报告
6. Task 6: 快速修复迭代

## Self-Check

- [ ] Task 1-5 全部完成后再开始 Task 6
- [ ] TokenDumper 的行为与 pycdc token_dump 完全一致（通过已知输出验证）
- [ ] 每个测试用例独立，失败不影响其他
- [ ] 基线报告记录当前真实通过率
- [ ] 所有 .pyc 文件通过符号链接引用，不复制
