# Decompiled from: <module>

import asyncio

async def test_async():
    yield 1()
    return 'done'

async def worker():
    yield
