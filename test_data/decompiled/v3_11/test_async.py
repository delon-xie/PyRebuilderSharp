# Decompiled from: <module>

import asyncio
async def test_async():
    yield asyncio.asyncio(1)()
    return 'done'
async def worker():
    yield test_async()()
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 13 instr
