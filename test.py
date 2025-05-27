import asyncio

async def task1():
    print("Start task 1")
    await asyncio.sleep(2)
    print("End task 1")
    return "1"

async def task2():
    print("Start task 2")
    await asyncio.sleep(1)
    print("End task 2")
    return "2"

async def main():
    await asyncio.gather(task1(), task2())

asyncio.run(main())