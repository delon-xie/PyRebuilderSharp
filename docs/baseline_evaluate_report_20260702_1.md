# 白盒测试基线评估报告

**生成时间**: 2026-07-02
**测试文件总数**: 56

## 一、总体概览

### 1.1 版本分布

| Python 版本 | 文件数 | 完全通过 | 语法错误 | 运行时错误 | 控制块异常 | 孤儿块 | 反编译失败 |
|------------|--------|----------|----------|------------|------------|--------|------------|
| 3.10 | 2 | 1 | 1 | 0 | 0 | 0 | 0 |
| 3.11 | 8 | 1 | 6 | 1 | 0 | 0 | 0 |
| 3.12 | 14 | 2 | 8 | 2 | 2 | 0 | 0 |
| 3.13 | 16 | 2 | 9 | 2 | 3 | 0 | 0 |
| 3.14 | 16 | 2 | 10 | 2 | 2 | 0 | 0 |
| **总计** | 56 | - | - | - | - | - |

### 1.2 总体通过率

- **完全通过**: 8/56 (14.3%)
- **语法错误**: 34 (60.7%)
- **运行时错误**: 7 (12.5%)
- **控制块异常**: 7 (12.5%)
- **孤儿块**: 0 (0.0%)
- **反编译失败**: 0 (0.0%)

## 二、按优先级分类的问题分析

### 2.1 控制块异常（最高优先级）

**影响文件数**: 7

| 文件 | 版本 | 问题类型 |
|------|------|----------|
| reprlib.3.14.pyc | 3.14 | bare_elem, bare_list, empty_try, for_empty, stray_pass |
| reprlib.3.13.pyc | 3.13 | bare_elem, bare_list, empty_try, stray_pass |
| reprlib.3.12.pyc | 3.12 | bare_elem, bare_list, empty_try, for_empty, stray_pass |
| test_try.3.13.pyc | 3.13 | empty_try |
| mixed5_out.3.14.pyc | 3.14 | empty_try, stray_pass |
| mixed5_out.3.13.pyc | 3.13 | empty_try, stray_pass |
| mixed5_out.3.12.pyc | 3.12 | empty_try, stray_pass |

### 2.2 语法错误

**影响文件数**: 34

| 文件 | 版本 | 错误详情 |
|------|------|----------|
| reprlib.3.11.pyc | 3.11 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| reprlib.3.10.pyc | 3.10 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| pprint.3.14.pyc | 3.14 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_with_simple.3.14.pyc | 3.14 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_with_simple.3.13.pyc | 3.13 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_with_simple.3.12.pyc | 3.12 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_with_simple.3.11.pyc | 3.11 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_break_for.3.14.pyc | 3.14 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_break_for.3.13.pyc | 3.13 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_break_for.3.12.pyc | 3.12 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_break_for.3.11.pyc | 3.11 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_minimal_if.3.14.pyc | 3.14 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_minimal_if.3.13.pyc | 3.13 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_minimal_if.3.12.pyc | 3.12 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_minimal_if.3.11.pyc | 3.11 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_syntax.3.14.pyc | 3.14 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_syntax.3.13.pyc | 3.13 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_syntax.3.12.pyc | 3.12 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_syntax.3.11.pyc | 3.11 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| test_for_try.3.12.pyc | 3.12 |   File "/var/folders/sv/jvj1f_9j7s5650qqr4fy84x000 |
| ... | ... | 共 34 个文件 |

### 2.3 孤儿块

**影响文件数**: 0


### 2.4 运行时错误

**影响文件数**: 7

| 文件 | 版本 | 错误详情 |
|------|------|----------|
| expr_test.3.14.pyc | 3.14 | name 'x' is not defined |
| expr_test.3.13.pyc | 3.13 | name 'x' is not defined |
| expr_test.3.12.pyc | 3.12 | name 'x' is not defined |
| expr_test.3.11.pyc | 3.11 | name 'x' is not defined |
| compare_ast.3.14.pyc | 3.14 | [Errno 2] No such file or directory: '/tmp/actual_ |
| compare_ast.3.13.pyc | 3.13 | [Errno 2] No such file or directory: '/tmp/actual_ |
| compare_ast.3.12.pyc | 3.12 | [Errno 2] No such file or directory: '/tmp/actual_ |

### 2.5 反编译失败

**影响文件数**: 0


## 三、问题模式统计

| 问题模式 | 出现次数 | 严重程度 |
|----------|----------|----------|
| empty_try | 277 | 高 |
| bare_list | 86 | 中 |
| stray_pass | 49 | 低 |
| try_no_except_finally | 42 | 高 |
| bare_elem | 12 | 中 |
| for_empty | 3 | 高 |

## 四、修复计划

### 4.1 P0 - 紧急修复（影响面大）

1. **修复 Python 3.13/3.14 列表推导式和 for 循环重构**
   - 问题: `_repr_iterable` 等函数出现 `elem`, `[]`, `for _ in []` 等异常输出
   - 原因: `LOAD_FAST_AND_CLEAR` 和超级指令处理不完整
   - 影响: 3.13/3.14 的 reprlib 等核心库函数

2. **修复 try 块无 except/finally 问题**
   - 问题: 反编译输出包含 `try:` 但没有 except/finally
   - 原因: 异常表解析和控制流图重建不完整
   - 影响: 所有版本的异常处理

### 4.2 P1 - 重要修复（控制块异常）

3. **修复 for 循环空迭代器问题**
   - 问题: `for _ in []:` 空循环
   - 原因: 列表推导式重构失败

4. **修复孤儿 raise 语句**
   - 问题: 独立的 `raise` 语句
   - 原因: 异常处理块重构不完整

### 4.3 P2 - 次要修复（孤儿块）

5. **清理裸表达式**
   - 问题: `elem`, `[]` 等裸表达式
   - 原因: 栈机状态管理问题

6. **清理多余 pass 语句**
   - 问题: 控制流语句前的多余 pass

### 4.4 P3 - 优化（反编译失败）

7. **处理特殊 .pyc 文件**
   - 问题: 部分文件反编译失败
   - 原因: 可能是 Python 2.5/2.6 等旧版本或特殊格式

## 五、详细问题列表

### 5.1 Python 3.14 问题

**问题文件数**: 14

| 文件 | 类别 |
|------|------|
| reprlib.3.14.pyc | control_block_anomaly |
| pprint.3.14.pyc | syntax_error |
| test_with_simple.3.14.pyc | syntax_error |
| test_break_for.3.14.pyc | syntax_error |
| test_minimal_if.3.14.pyc | syntax_error |
| test_syntax.3.14.pyc | syntax_error |
| abc.3.14.pyc | syntax_error |
| enum.3.14.pyc | syntax_error |
| mixed5_out.3.14.pyc | control_block_anomaly |
| expr_test.3.14.pyc | runtime_error |
| run_lv2.3.14.pyc | syntax_error |
| debug_blocks.3.14.pyc | syntax_error |
| compare_ast.3.14.pyc | runtime_error |
| test_with_deref.3.14.pyc | syntax_error |

### 5.2 Python 3.13 问题

**问题文件数**: 14

| 文件 | 类别 |
|------|------|
| reprlib.3.13.pyc | control_block_anomaly |
| test_with_simple.3.13.pyc | syntax_error |
| test_try.3.13.pyc | control_block_anomaly |
| test_break_for.3.13.pyc | syntax_error |
| test_minimal_if.3.13.pyc | syntax_error |
| test_syntax.3.13.pyc | syntax_error |
| abc.3.13.pyc | syntax_error |
| enum.3.13.pyc | syntax_error |
| mixed5_out.3.13.pyc | control_block_anomaly |
| expr_test.3.13.pyc | runtime_error |
| run_lv2.3.13.pyc | syntax_error |
| debug_blocks.3.13.pyc | syntax_error |
| compare_ast.3.13.pyc | runtime_error |
| test_with_deref.3.13.pyc | syntax_error |
