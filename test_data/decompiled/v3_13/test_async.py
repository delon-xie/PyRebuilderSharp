# Decompiled from: <module>

import asyncio
async def test_async():
    try:
        asyncio.sleep(1)
    except:
        pass
async def worker():
    try:
        test_async()
    except:
        pass
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 12 instr
