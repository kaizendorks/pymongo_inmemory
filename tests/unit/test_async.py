import asyncio
import threading
import sys


def test_init_module_in_loop():
    sys.modules.pop("pymongo_inmemory.mongod", None)

    async def main():
        import pymongo_inmemory.mongod  # noqa F401

        return True

    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=loop.run_forever, daemon=True)
    thread.start()
    result = asyncio.run_coroutine_threadsafe(main(), loop).result()
    loop.call_soon_threadsafe(loop.stop)
    thread.join()

    assert result
