# Decompiled from: <module>

import asyncio
async def test_async():
    try:
        asyncio.sleep(1)()
    except:
        pass

async def worker():
    try:
        test_async()()
    except:
        pass
