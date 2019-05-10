import os
import asyncio
import logging

from telegram import setup

from misc import disp


fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
logging.basicConfig(level=int(os.environ.get('LOG_LEVEL', 40)), format=fmt)


loop = asyncio.get_event_loop()


def run_bot():
    setup()

    async def main():
        await disp.skip_updates()
        await disp.start_polling()

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.close()
        os._exit(1)
