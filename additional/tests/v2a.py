import asyncio

from additional.audio import Process

loop = asyncio.get_event_loop()


async def main():
    proc = Process("videofilename.ext")
    assert proc
    base64 = await proc.convert_to_base64()
    assert base64
    assert isinstance(base64, bytes)


loop.run_until_complete(main())
