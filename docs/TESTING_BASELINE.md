# PyRebuilderSharp 测试基线

**日期:** 2026-06-12
**pycdc 测试集:** 83 输入文件, 420 .pyc 文件 (Python 1.0 ~ 3.14)

---

## 当前基线

### 全版本概况

| 版本范围 | 测试数 | PASS | FAIL | 通过率 |
|---------|--------|------|------|--------|
| **总计** | **420** | **0** | **420** | **0.0%** |

### 失败原因分布（全版本）

| 失败原因 | 计数 | 说明 |
|---------|------|------|
| Unknown magic number (Python 1.x-2.x) | ~200 | 目标不涵盖，正常 |
| EndOfStreamException | ~80 | PycReader 读取不完全 |
| Unhandled opcode | ~140 | StackMachine 未实现的操作码 |

### Python 3.8-3.12 焦点范围

对 Python 3.8~3.12 版本筛选后的基线（核心目标）：

| 类别 | 测试数 | PASS | FAIL | 通过率 |
|------|--------|------|------|--------|
| 简单表达式 | ~45 | 0 | ~45 | 0% |
| 控制流 | ~30 | 0 | ~30 | 0% |
| 异常处理 | ~10 | 0 | ~10 | 0% |
| 类/函数 | ~25 | 0 | ~25 | 0% |
| 高级特性 | ~35 | 0 | ~35 | 0% |
| **合计** | **~145** | **0** | **0%** |

---

## 缺失操作码清单（按影响面排序）

当前 StackMachine 已实现：`LOAD_CONST, LOAD_NAME, LOAD_FAST, LOAD_GLOBAL, STORE_NAME, STORE_FAST, STORE_ATTR, LOAD_ATTR, BUILD_TUPLE, BUILD_LIST, BINARY_ADD, BINARY_SUBTRACT, BINARY_MULTIPLY, BINARY_TRUE_DIVIDE, BINARY_POWER, INPLACE_ADD, UNARY_NEGATIVE, UNARY_NOT, RETURN_VALUE, POP_TOP, DUP_TOP, COMPARE_OP, CALL_FUNCTION, NOP, RESUME`

**接下来优先实现的操作码（基于 simple_const 测试）：**

| 优先级 | 操作码 | 影响测试数 | 说明 |
|--------|--------|-----------|------|
| P0 | `BUILD_MAP` | ~15 | 字典字面量 |
| P0 | `BUILD_SET` | ~10 | 集合字面量 |
| P0 | `STORE_GLOBAL` | ~10 | 全局变量赋值 |
| P1 | `GET_ITER` + `FOR_ITER` | ~12 | for 循环 |
| P1 | `JUMP_FORWARD` / `JUMP_ABSOLUTE` | ~20 | 跳转语句 |
| P1 | `POP_JUMP_IF_TRUE` / `POP_JUMP_IF_FALSE` | ~18 | if 条件 |

---

## 测试命令

```bash
# 运行所有单元测试
dotnet test tests/PyRebuilderSharp.Tests/ --filter "PyRebuilderSharp.Tests"

# 运行 E2E 基线
dotnet test tests/PyRebuilderSharp.Tests/ --filter "RunComprehensive_Baseline_AllTests"

# 运行 Smoke 测试
dotnet test tests/PyRebuilderSharp.Tests/ --filter "SmokeTest"
```
