import asyncio
import time


async def greet(name, delay):
    await asyncio.sleep(delay)
    print(f'{name}: I waited {delay} seconds before saying "hello"')


async def main():
    task_1 = asyncio.create_task(greet("t1", 3))
    task_2 = asyncio.create_task(greet("t2", 2))
    task_3 = asyncio.create_task(greet("t3", 2))

    start_time = time.time()

    print("0.00s: Program Start")

    await task_1
    await task_2
    await task_3

    print(f"{time.time() - start_time:.2f}s: Program End")


asyncio.run(main())
