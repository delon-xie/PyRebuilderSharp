# Decompiled from: <module>

import asyncio
async def test_async():
    yield asyncio.asyncio(1)()
    return 'done'
async def worker():
    yield test_async()()
