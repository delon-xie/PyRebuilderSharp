# Phase 1: 单一控制块测试计划

## 目标
为每种控制块类型创建独立的测试文件，逐个验证。

## 控制块列表

| # | 控制块 | 测试文件 | 状态 | 说明 |
|---|--------|---------|------|------|
| 1 | if/else | test_if_base.py | ⏳ | if, if/else, if/elif/else |
| 2 | while | test_while_base.py | ✅ 已有 | test_control_flow.py 含基础 |
| 3 | for | test_for_base.py | ✅ 已有 | test_control_flow.py 含基础 |
| 4 | break/continue | test_break_continue.py | ⏳ | for/while 中断 |
| 5 | try/except/finally | test_try_base.py | ⏳ | try/except, try/finally, try/except/else/finally |
| 6 | raise | test_raise_base.py | ⏳ | raise, raise Exc, raise Exc from Cause |
| 7 | with | test_with_base.py | ⏳ | with, with as |
| 8 | def/return | test_def_base.py | ⏳ | def, args, return |
| 9 | class | test_class_base.py | ⏳ | class, init, methods |
| 10 | lambda | test_lambda_base.py | ⏳ | lambda, assignment |
| 11 | async def/await | test_async_base.py | ⏳ | async def, await |
| 12 | async for | test_async_for.py | ⏳ | async for |
| 13 | async with | test_async_with.py | ⏳ | async with |
| 14 | yield/yield from | test_yield_base.py | ⏳ | yield, yield from |
| 15 | import | test_import_base.py | ⏳ | import, from...import |
| 16 | global/nonlocal | test_global_base.py | ⏳ | global, nonlocal |
| 17 | match/case | test_match_base.py | ⏳ | Python 3.10+ |
