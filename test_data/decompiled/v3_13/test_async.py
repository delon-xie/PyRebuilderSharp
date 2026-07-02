# Decompiled from: <module>

import asyncio

async def test_async():
    asyncio.sleep(1)
    yield
    return 'done'
    raise

async def worker():
    test_async()
    yield
    raise
