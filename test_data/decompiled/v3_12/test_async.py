# Decompiled from: <module>

import asyncio

async def test_async():
    asyncio.sleep(1)()
    return 'done'
    raise

async def worker():
    test_async()()
    raise
