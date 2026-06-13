# Phase 4 语法覆盖计划

**版本**: v1.0
**日期**: 2026-06-14
**前提**: Phase 3 ✅ — marshal 收敛 · 测试矩阵 · CrashCollector · GUI 稳定

---

## 一、目标

从"基本可读"到**完整可用** — 覆盖常见 Python 语法，使反编译输出可以通过 `python3 -c "compile(src, '', 'exec')"` 的语法检查。

## 二、优先级分级

```
P0 ──── 阻塞项（无此功能影响 ≥50% 测试文件）   ⏱ 4-6h
  ├── Assign + FunctionRef → FunctionDef (def 语句)
  ├── class 定义 (class statements)
  └── yield / yield from 表达式

P1 ──── 重要项（常见语法模式）                  ⏱ 3-5h
  ├── 装饰器 @decorator
  ├── async def / await
  ├── 展开赋值 a, b = ...
  └── for-else / while-else 正确输出

P2 ──── 增强项（较少见但提高输出完整性）          ⏱ 2-4h
  ├── match/case (3.10+)
  ├── 类型注解 def f(x: int) -> str:
  ├── walrus 运算符 :=
  └── starred assignment *args
```

## 三、任务拆解

### P0-1: Assign + FunctionRef → FunctionDef

**问题**：当前输出为 `name_0 = <lambda>`，应为 `def name_0(...):`

```
当前: name_0 = <lambda>
目标: def depth_5_if(x0, x1, x2, x3, x4):
           result = 0
           if x0 > 0:
               ...
```

**修复步骤**：
1. 检查 `PostProcessFunctionDefs` 的 `Assign + FunctionRef` 匹配逻辑
2. 确保 `BuildFunctionDef` 在调用 `DecompileChildCode` 时正确传入 `funcRef.Code`
3. 确保 `PythonCodeGenerator` 的 `Visit(FunctionDef)` 分支输出了完整 `def` 语句
4. 验证：反编译 `test_nested_depth_5.3.12.pyc` 输出包含 `def depth_5_if`

**验收**：Lv3 测试 33 个从 `known_issue` 变为 `ast_check_ok`

### P0-2: `class` 定义

**问题**：`class Foo(Base):` 不被识别为类定义

**修复步骤**：
1. 检查 `AstBuilder.PostProcessFunctionDefs` 中的 `ExtractClassDef` 调用
2. 确保 `Assign + Call(__build_class__)` 被正确转为 `ClassDef`
3. 测试：`data/test_input/class_simple.py` → 编译 → 反编译 → AST 对比
4. 处理类方法定义（嵌套 FunctionDef）

### P0-3: `yield` / `yield from`

**问题**：生成器函数中的 `yield` 被丢弃或解析为错误代码

**修复步骤**：
1. 检查 `Yield 指令 → AstNode` 的映射（当前 StackMachine 缺少 YIELD_VALUE × YIELD_FROM）
2. 添加 `AstNode.Yield` / `AstNode.YieldFrom` 节点
3. 在生成器中正确处理 `return` → `StopIteration`
4. 测试：`test_yield_simple` / `test_yieldfrom_simple`

### P1-1: 装饰器 `@decorator`

**问题**：`@property`、`@staticmethod` 等装饰器被丢弃

```
当前: def abstractmethod(f):
目标: @staticmethod
      def abstractmethod(f):
```

**修复步骤**：
1. 检查 `AstBuilder` 中 `CALL_FUNCTION` / `BUILD_MAP` 等指令是否识别装饰器模式
2. 在 `PostProcessFunctionDefs` 中检测 `Assign + Call + FunctionRef` 模式 → 提取装饰器列表
3. 将装饰器附加到 `FunctionDef.DecoratorList`
4. 在 `PythonCodeGenerator` 中输出 `@decorator` 行

### P1-2: 展开赋值

**问题**：`a, b = func()` 反编译为 `a = func()` 或更糟

**修复步骤**：
1. 检查 `UNPACK_SEQUENCE` / `UNPACK_EX` 指令处理
2. 生成 `Tuple (a, b) = func()` AST
3. 测试：多返回值赋值

### P2: 特殊语法

- **match/case**: 需要 3.10+ 操作码 `MATCH_KEYS` / `MATCH_CLASS` 等的支持
- **类型注解**: `LOAD_CONST` + `LOAD_NAME` 组合 → 注解 AST
- **walrus 运算符**: `:=` = `DUP_TOP` + `STORE_FAST` 组合

## 四、执行计划

```
Week 1: P0
  Day 1-2: Assign+FunctionRef → FunctionDef (def 语句)
  Day 2-3: class 定义
  Day 3-4: yield / yield from
  Daily: 构建验证 + 测试

Week 2: P1
  Day 1-2: 装饰器
  Day 2: async def / await
  Day 3: 展开赋值
  Daily: 测试回归 + manifest 更新

Week 3: P2
  Day 1-2: match/case
  Day 2: 类型注解
  Day 3: 收尾 + 新增 test_data 编译
```

## 五、验收标准

| 检查项 | 标准 |
|:-------|:-----|
| def 语句 | 33/33 Lv3 从 `known_issue` → `ast_check_ok` |
| class 语句 | ~21 个标准库测试通过 |
| yield | `test_yield_*` 全部通过 |
| 装饰器 | `test_decorator_*` 新增测试 >0 |
| 3.11/3.12 回归 | 182/182 基准测试不退化 |
| GUI 稳定 | 打开/拖放/反编译按钮无异常 |

## 六、回退机制

如果某个 P0 任务在 2 天内无法通过验收：
1. 保留现有 `known_issue` 标记
2. 将失败分析写入 `docs/phase4_blockers.md`
3. 跳过该任务继续后序
4. 在迭代末尾集中攻关
