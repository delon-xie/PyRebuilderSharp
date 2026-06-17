# Decompiled from: <module>

import asyncio
async def test_async():
    try:
        asyncio.sleep(1)()
    except:
        pass
    # [WARN] 1 instructions not decompiled
    #   @0x0044: JUMP_BACKWARD arg=10
async def worker():
    try:
        test_async()()
    except:
        pass
    # [WARN] 1 instructions not decompiled
    #   @0x002E: JUMP_BACKWARD arg=10
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 12 instr
