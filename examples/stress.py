from toy_async import *


async def nop():
    await sleep(1)
    return 1


async def main():
    tasks = run_all(nop() for i in range(100000))
    print(sum(await join(tasks)))


s = Scheduler(debug=True)
s.mainloop(main())
