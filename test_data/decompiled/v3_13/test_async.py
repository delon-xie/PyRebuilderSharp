# Decompiled from: <module>

import asyncio

async def test_async():
    None
    asyncio.sleep(1)
    yield
    return 'done'
    raise

async def worker():
    None
    test_async()
    yield
    raise
