# Decompiled from: <module>

import asyncio
async def test_async():
    yield from asyncio.sleep(1)
    return 'done'

async def worker():
    yield from test_async()
