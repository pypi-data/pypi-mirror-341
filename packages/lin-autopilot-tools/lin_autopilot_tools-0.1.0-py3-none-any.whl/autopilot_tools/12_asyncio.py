import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f'start at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

    await say_after(1, "hello")
    await say_after(2, "world")

    print(f'finished at {time.strftime("%X")}')

asyncio.run(main())