# Decompiled from: <module>

import asyncio
def test_async():
    yield from asyncio.sleep(1)
    return 'done'
def worker():
    yield from test_async()
