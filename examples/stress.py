def toy_async():
    from toy_async import Scheduler, gather, sleep

    async def nop():
        await sleep(1)
        return 1

    async def main():
        print(sum(await gather(nop() for i in range(100000))))

    s = Scheduler()
    s.mainloop(main())


def asyncio():
    import asyncio

    async def nop():
        await asyncio.sleep(1)
        return 1

    async def main():
        print(sum(await asyncio.gather(*(nop() for i in range(100000)))))

    asyncio.run(main())


from timeit import default_timer

now = default_timer()
toy_async()
print("toy_async", default_timer() - now)

now = default_timer()
asyncio()
print("asyncio", default_timer() - now)
