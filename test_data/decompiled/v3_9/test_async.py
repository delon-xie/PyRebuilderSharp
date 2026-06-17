# Decompiled from: <module>

import asyncio
async def test_async():
    yield from asyncio.sleep(1)
    return 'done'
async def worker():
    yield from test_async()
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 14 instr
