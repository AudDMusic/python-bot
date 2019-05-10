# TODO
from misc import audd


async def get():
    for link in ["https://api.audd.io/?url=https://audd.tech/example1.mp3&cache=test",
                 'https://api.audd.io/reminisce/?cache=test&return=lyrics']:

        async with audd.get(link) as resp:

            print(await resp.json())


if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(get())
