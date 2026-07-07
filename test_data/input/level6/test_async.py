import asyncio

async def test_async():
    await asyncio.sleep(1)
    return 'done'

async def worker():
    await test_async()
