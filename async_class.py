import asyncio
import time


class Test(object):
    def __init__(self, val):
        self._value = val
        self._loop = asyncio.get_event_loop()

    def get_value(self):
        async def _internal_get():
            await asyncio.sleep(1)
            return self._value

        tasks = [_internal_get() for _ in range(10)]
        return self._loop.run_until_complete(asyncio.wait(tasks))

    def set_value(self, val):
        async def _internal_set_value(_val):
            await asyncio.sleep(1)
            self._value = _val

        return self._loop.run_until_complete(_internal_set_value(val))


test = Test(1)
start = time.time()
test.get_value()
end = time.time()
print('Total time:', end - start)
