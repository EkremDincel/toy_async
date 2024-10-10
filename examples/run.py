from toy_async import *


async def foo(x):
    await sleep(1)
    print(x)
    return x


async def multiple_tasks():
    t1 = run(foo("a"))
    t2 = run(foo("b"))
    print(await t1.wait(), await t2.wait())


s = Scheduler(debug=True)
s.mainloop(multiple_tasks())
